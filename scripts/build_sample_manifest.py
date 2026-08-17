"""Build the deterministic integrity manifest for raw-MRI/mask/PLY triples."""

from __future__ import annotations

import gzip
import hashlib
import json
import struct
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RAW_MRI_DIR = ROOT / "data" / "samples" / "raw_mri"
MASK_DIR = ROOT / "data" / "samples" / "nifti"
POINT_CLOUD_DIR = ROOT / "data" / "samples" / "point_clouds"
OUTPUT = ROOT / "data" / "samples" / "sample_manifest.json"

NIFTI_DTYPES = {
    2: "u1",
    4: "i2",
    8: "i4",
    16: "f4",
    64: "f8",
    256: "i1",
    512: "u2",
    768: "u4",
    1024: "i8",
    1280: "u8",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_nifti_bytes(path: Path) -> bytes:
    if path.name.lower().endswith(".nii.gz"):
        with gzip.open(path, "rb") as handle:
            return handle.read()
    return path.read_bytes()


def inspect_nifti(path: Path, content_kind: str) -> dict:
    """Inspect NIfTI-1 bytes without loading them through an external service."""

    content = _read_nifti_bytes(path)
    little_endian = struct.unpack("<i", content[:4])[0] == 348
    endian = "<" if little_endian else ">"
    if struct.unpack(endian + "i", content[:4])[0] != 348:
        raise ValueError(f"Unsupported NIfTI header: {path.name}")

    dimensions = struct.unpack(endian + "8h", content[40:56])
    ndim = dimensions[0]
    shape = tuple(int(value) for value in dimensions[1 : ndim + 1])
    if ndim != 3:
        raise ValueError(f"Expected one 3D volume: {path.name}")
    datatype_code = struct.unpack(endian + "h", content[70:72])[0]
    if datatype_code not in NIFTI_DTYPES:
        raise ValueError(f"Unsupported NIfTI datatype {datatype_code}: {path.name}")
    bitpix = struct.unpack(endian + "h", content[72:74])[0]
    pixdim = struct.unpack(endian + "8f", content[76:108])
    voxel_offset = int(struct.unpack(endian + "f", content[108:112])[0])
    slope, intercept = struct.unpack(endian + "2f", content[112:120])
    qform_code = struct.unpack(endian + "h", content[252:254])[0]
    sform_code = struct.unpack(endian + "h", content[254:256])[0]
    qform_signature = struct.unpack(endian + "6f", content[256:280])
    dtype = np.dtype(endian + NIFTI_DTYPES[datatype_code])
    values = np.frombuffer(content, dtype=dtype, count=int(np.prod(shape)), offset=voxel_offset)
    if values.size != int(np.prod(shape)):
        raise ValueError(f"NIfTI payload is incomplete: {path.name}")

    scaled = values.astype(np.float32, copy=False)
    if slope not in (0.0, 1.0):
        scaled = scaled * slope
    if intercept != 0.0:
        scaled = scaled + intercept

    record = {
        "relative_path": path.relative_to(ROOT).as_posix(),
        "filename": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "format": "NIfTI-1 gzip" if path.name.lower().endswith(".gz") else "NIfTI-1",
        "content_kind": content_kind,
        "shape": list(shape),
        "datatype_code": int(datatype_code),
        "datatype": str(dtype),
        "bitpix": int(bitpix),
        "voxel_spacing": [round(float(value), 7) for value in pixdim[1 : ndim + 1]],
        "qform_code": int(qform_code),
        "sform_code": int(sform_code),
        "qform_signature": [round(float(value), 7) for value in qform_signature],
    }

    if content_kind == "raw_intensity_mri":
        finite = np.isfinite(scaled)
        nonzero = scaled[finite & (scaled != 0)]
        if not finite.all() or not nonzero.size:
            raise ValueError(f"Raw MRI contains invalid or empty intensity data: {path.name}")
        percentile_levels = [0.1, 1.0, 5.0, 50.0, 95.0, 99.0, 99.9]
        percentiles = np.percentile(nonzero, percentile_levels)
        record["intensity"] = {
            "minimum": round(float(scaled.min()), 6),
            "maximum": round(float(scaled.max()), 6),
            "mean": round(float(scaled.mean()), 6),
            "standard_deviation": round(float(scaled.std()), 6),
            "zero_fraction": round(float(np.count_nonzero(scaled == 0) / scaled.size), 8),
            "finite_fraction": round(float(finite.mean()), 8),
            "nonzero_percentiles": {
                str(level): round(float(value), 6)
                for level, value in zip(percentile_levels, percentiles)
            },
        }
    else:
        labels, counts = np.unique(scaled, return_counts=True)
        label_counts = {
            str(int(label) if float(label).is_integer() else float(label)): int(count)
            for label, count in zip(labels, counts)
        }
        nonzero_mask = scaled.reshape(shape, order="F") != 0
        coordinates = np.argwhere(nonzero_mask)
        bounds = None
        if coordinates.size:
            bounds = {
                "minimum_index": coordinates.min(axis=0).astype(int).tolist(),
                "maximum_index": coordinates.max(axis=0).astype(int).tolist(),
            }
        record.update({
            "label_counts": label_counts,
            "nonzero_voxels": int(np.count_nonzero(scaled)),
            "nonzero_bounds": bounds,
        })
    return record


def inspect_ply(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    try:
        header_end = lines.index("end_header")
    except ValueError as error:
        raise ValueError(f"PLY header is incomplete: {path.name}") from error
    header = lines[: header_end + 1]
    if "format ascii 1.0" not in header:
        raise ValueError(f"Only ASCII PLY 1.0 is supported: {path.name}")
    declared_vertices = int(next(line.split()[-1] for line in header if line.startswith("element vertex ")))
    properties = [line.split()[-1] for line in header if line.startswith("property ")]
    required = {"x", "y", "z", "label", "branch", "reliability", "red", "green", "blue"}
    if not required.issubset(properties):
        raise ValueError(f"PLY properties are incomplete: {path.name}")
    points = np.loadtxt(lines[header_end + 1 :], dtype=float)
    if points.ndim != 2 or len(points) != declared_vertices or points.shape[1] != len(properties):
        raise ValueError(f"PLY vertex table does not match its header: {path.name}")
    columns = {name: points[:, index] for index, name in enumerate(properties)}

    label_values, label_counts = np.unique(columns["label"].astype(int), return_counts=True)
    branch_values, branch_counts = np.unique(columns["branch"].astype(int), return_counts=True)
    color_map: dict[str, list[int]] = {}
    for label in label_values:
        subset = points[columns["label"].astype(int) == label]
        colors = np.unique(
            subset[:, [properties.index("red"), properties.index("green"), properties.index("blue")]].astype(int),
            axis=0,
        )
        if len(colors) == 1:
            color_map[str(int(label))] = colors[0].tolist()

    reliability = columns["reliability"]
    return {
        "relative_path": path.relative_to(ROOT).as_posix(),
        "filename": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "format": "PLY ASCII 1.0",
        "vertex_count": int(declared_vertices),
        "properties": properties,
        "coordinate_bounds": {
            "minimum": [round(float(value), 6) for value in points[:, :3].min(axis=0)],
            "maximum": [round(float(value), 6) for value in points[:, :3].max(axis=0)],
        },
        "label_counts": {str(int(label)): int(count) for label, count in zip(label_values, label_counts)},
        "branch_counts": {str(int(branch)): int(count) for branch, count in zip(branch_values, branch_counts)},
        "label_rgb": color_map,
        "reliability": {
            "minimum": round(float(reliability.min()), 6),
            "mean": round(float(reliability.mean()), 6),
            "maximum": round(float(reliability.max()), 6),
        },
    }


def geometry_alignment(raw_mri: dict, mask: dict) -> dict:
    shape_match = raw_mri["shape"] == mask["shape"]
    spacing_difference = float(np.max(np.abs(
        np.asarray(raw_mri["voxel_spacing"]) - np.asarray(mask["voxel_spacing"])
    )))
    qform_difference = float(np.max(np.abs(
        np.asarray(raw_mri["qform_signature"]) - np.asarray(mask["qform_signature"])
    )))
    qform_match = (
        raw_mri["qform_code"] == mask["qform_code"]
        and qform_difference <= 1e-5
    )
    validated = shape_match and spacing_difference <= 1e-5 and qform_match
    return {
        "validated": validated,
        "shape_match": shape_match,
        "voxel_spacing_max_abs_difference": round(spacing_difference, 9),
        "qform_match": qform_match,
        "qform_signature_max_abs_difference": round(qform_difference, 9),
        "overlay_permitted": validated,
    }


def main() -> None:
    subjects = []
    for index in range(1, 11):
        subject_id = f"AD{index}"
        raw_path = RAW_MRI_DIR / f"{subject_id}.nii"
        mask_path = MASK_DIR / f"{subject_id}_mask4.nii.gz"
        point_cloud_path = POINT_CLOUD_DIR / f"ADPC_BEST_{subject_id}_mask4.ply"
        if not raw_path.is_file() or not mask_path.is_file() or not point_cloud_path.is_file():
            raise FileNotFoundError(f"Missing raw-MRI/mask/PLY artifact for {subject_id}")
        raw_mri = inspect_nifti(raw_path, "raw_intensity_mri")
        mask = inspect_nifti(mask_path, "discrete_label_mask")
        alignment = geometry_alignment(raw_mri, mask)
        if not alignment["validated"]:
            raise ValueError(f"Raw MRI and mask geometry do not align for {subject_id}")
        subjects.append({
            "subject_id": subject_id,
            "cohort_label": "AD",
            "triple_status": "validated",
            "raw_mri": raw_mri,
            "segmentation_mask": mask,
            "point_cloud": inspect_ply(point_cloud_path),
            "alignment": alignment,
        })

    manifest = {
        "schema_version": "2.0",
        "generated_on": "2026-08-11",
        "sample_count": len(subjects),
        "triple_count": len(subjects),
        "artifact_count": len(subjects) * 3,
        "data_boundary": "User-supplied local research samples; never sent to the external LLM path.",
        "interpretation_note": (
            "Each subject has one raw intensity MRI, one aligned discrete label mask, and one lightweight PLY. "
            "Anatomical meanings for mask and PLY label codes were not supplied and are not inferred."
        ),
        "subjects": subjects,
    }
    OUTPUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Validated {len(subjects)} raw-MRI/mask/PLY triples and wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

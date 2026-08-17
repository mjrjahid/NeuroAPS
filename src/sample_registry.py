"""Validated access to the local raw-MRI/mask/PLY demonstration cohort."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


REQUIRED_SUBJECT_KEYS = {
    "subject_id",
    "cohort_label",
    "triple_status",
    "raw_mri",
    "segmentation_mask",
    "point_cloud",
    "alignment",
}


def load_sample_manifest(path: str | Path) -> dict[str, Any]:
    """Load and validate the inspectable sample manifest."""

    manifest_path = Path(path)
    with manifest_path.open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)

    if manifest.get("schema_version") != "2.0":
        raise ValueError("Unsupported sample-manifest schema")
    subjects = manifest.get("subjects")
    if not isinstance(subjects, list) or not subjects:
        raise ValueError("Sample manifest must contain at least one subject")
    if manifest.get("sample_count") != len(subjects):
        raise ValueError("Sample count does not match the subject records")

    seen: set[str] = set()
    for subject in subjects:
        if not isinstance(subject, dict) or not REQUIRED_SUBJECT_KEYS.issubset(subject):
            raise ValueError("A subject record is missing required fields")
        subject_id = str(subject["subject_id"])
        if subject_id in seen:
            raise ValueError(f"Duplicate subject ID: {subject_id}")
        seen.add(subject_id)
        if subject["triple_status"] != "validated":
            raise ValueError(f"Unvalidated sample triple: {subject_id}")
        if not subject["alignment"].get("validated") or not subject["alignment"].get("overlay_permitted"):
            raise ValueError(f"Unvalidated raw-MRI/mask alignment: {subject_id}")
        for artifact_key in ("raw_mri", "segmentation_mask", "point_cloud"):
            artifact = subject[artifact_key]
            if not isinstance(artifact, dict):
                raise ValueError(f"Invalid {artifact_key} metadata for {subject_id}")
            if not {"relative_path", "sha256", "bytes"}.issubset(artifact):
                raise ValueError(f"Incomplete {artifact_key} metadata for {subject_id}")
            if len(str(artifact["sha256"])) != 64:
                raise ValueError(f"Invalid checksum for {subject_id} {artifact_key}")
    return manifest


def resolve_sample_path(project_root: str | Path, relative_path: str) -> Path:
    """Resolve a manifest path without permitting traversal outside the project."""

    root = Path(project_root).resolve()
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise ValueError("Sample path escapes the project directory") from error
    if not candidate.is_file():
        raise FileNotFoundError(f"Registered sample file is unavailable: {relative_path}")
    return candidate


def validate_manifest_files(manifest: dict[str, Any], project_root: str | Path, verify_hashes: bool = False) -> list[str]:
    """Return validation errors for all registered local artifacts."""

    errors: list[str] = []
    for subject in manifest["subjects"]:
        for artifact_key in ("raw_mri", "segmentation_mask", "point_cloud"):
            artifact = subject[artifact_key]
            try:
                path = resolve_sample_path(project_root, artifact["relative_path"])
            except (OSError, ValueError) as error:
                errors.append(f"{subject['subject_id']} {artifact_key}: {error}")
                continue
            if path.stat().st_size != int(artifact["bytes"]):
                errors.append(f"{subject['subject_id']} {artifact_key}: byte count mismatch")
            if verify_hashes:
                checksum = hashlib.sha256(path.read_bytes()).hexdigest()
                if checksum != artifact["sha256"]:
                    errors.append(f"{subject['subject_id']} {artifact_key}: SHA-256 mismatch")
    return errors


def subject_lookup(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Index manifest subject records by stable subject identifier."""

    return {str(subject["subject_id"]): subject for subject in manifest["subjects"]}

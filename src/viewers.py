"""Synthetic and registered-data viewers with bounded point-cloud parsing."""

from __future__ import annotations

from io import BytesIO, StringIO

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from src.project_data import POINT_LABELS


def synthetic_mri_slice(diagnosis: str = "CN", size: int = 160, slice_index: int = 80) -> np.ndarray:
    """Create a deterministic teaching phantom, never a patient scan."""

    sample_step = complex(0, size)
    y, x = np.mgrid[-1:1:sample_step, -1:1:sample_step]
    depth = (slice_index - size / 2) / (size / 2)
    brain = ((x / 0.82) ** 2 + (y / 0.68) ** 2) <= max(0.25, 1 - 0.35 * depth**2)
    cortex = np.exp(-3.2 * (x**2 + 1.15 * y**2))
    folds = 0.10 * np.sin(18 * x + 2 * np.sin(7 * y)) * np.cos(15 * y)
    image = (0.30 + 0.60 * cortex + folds) * brain

    vent_scale = 1.35 if diagnosis == "AD" else 0.78
    for center_x in (-0.13, 0.13):
        ventricle = (((x - center_x) / (0.095 * vent_scale)) ** 2 + (y / (0.23 * vent_scale)) ** 2) <= 1
        image[ventricle] = 0.05

    if diagnosis == "AD":
        outer = ((x / 0.77) ** 2 + (y / 0.63) ** 2) <= 1
        image *= outer
    return np.clip(image, 0, 1)


def synthetic_point_cloud(diagnosis: str = "CN", count: int = 3000, seed: int = 3172) -> pd.DataFrame:
    """Return a deterministic, region-labelled teaching point cloud."""

    rng = np.random.default_rng(seed + (1 if diagnosis == "AD" else 0))
    count = int(np.clip(count, 400, 12000))
    allocations = {
        "Cortex": int(count * 0.40),
        "Ventricles": int(count * 0.25),
        "Hippocampus": int(count * 0.35),
    }
    allocations["Hippocampus"] += count - sum(allocations.values())
    frames = []

    n = allocations["Cortex"]
    theta = rng.uniform(0, 2 * np.pi, n)
    phi = np.arccos(rng.uniform(-1, 1, n))
    radius = 0.93 + rng.normal(0, 0.025 if diagnosis == "CN" else 0.04, n)
    cortical_scale = 0.88 if diagnosis == "AD" else 1.0
    frames.append(pd.DataFrame({
        "x": 1.10 * cortical_scale * radius * np.sin(phi) * np.cos(theta),
        "y": 0.83 * cortical_scale * radius * np.sin(phi) * np.sin(theta),
        "z": 0.76 * radius * np.cos(phi),
        "region": "Cortex",
    }))

    n = allocations["Ventricles"]
    side = rng.choice([-1.0, 1.0], n)
    vent_scale = 1.45 if diagnosis == "AD" else 0.85
    frames.append(pd.DataFrame({
        "x": side * 0.16 + rng.normal(0, 0.075 * vent_scale, n),
        "y": rng.normal(0, 0.15 * vent_scale, n),
        "z": rng.normal(0, 0.23 * vent_scale, n),
        "region": "Ventricles",
    }))

    n = allocations["Hippocampus"]
    side = rng.choice([-1.0, 1.0], n)
    hip_scale = 0.68 if diagnosis == "AD" else 1.0
    frames.append(pd.DataFrame({
        "x": side * 0.46 + rng.normal(0, 0.13 * hip_scale, n),
        "y": -0.24 + rng.normal(0, 0.085 * hip_scale, n),
        "z": -0.16 + rng.normal(0, 0.075 * hip_scale, n),
        "region": "Hippocampus",
    }))
    return pd.concat(frames, ignore_index=True)


def point_cloud_figure(
    frame: pd.DataFrame,
    point_size: int = 3,
    opacity: float = 0.72,
    color_mode: str = "Region",
    show_axes: bool = True,
) -> go.Figure:
    """Create an interactive point-cloud figure with the supplied anatomical labels."""

    colors = {
        "Cortex": "#7C5CE5",
        "Cortical area": "#7C5CE5",
        "Ventricles": "#16A6B6",
        "Hippocampus": "#E04F6F",
        "Other brain tissue": "#E7A83E",
        "Uploaded": "#6B5DD3",
    }
    frame = frame.copy()
    if "label" in frame and "anatomy" not in frame:
        frame["anatomy"] = frame["label"].astype(int).map(POINT_LABELS).fillna("Unmapped region")
    figure = go.Figure()
    if color_mode == "File RGB" and {"red", "green", "blue"}.issubset(frame.columns):
        rgb = [f"rgb({red},{green},{blue})" for red, green, blue in frame[["red", "green", "blue"]].astype(int).itertuples(index=False, name=None)]
        figure.add_trace(go.Scatter3d(
            x=frame["x"], y=frame["y"], z=frame["z"], mode="markers", name="File RGB",
            marker={"size": point_size, "color": rgb, "opacity": opacity},
            customdata=np.column_stack([frame.get("anatomy", pd.Series([""] * len(frame))), frame.get("reliability", pd.Series([np.nan] * len(frame)))]),
            hovertemplate="x=%{x:.3f}<br>y=%{y:.3f}<br>z=%{z:.3f}<br>region=%{customdata[0]}<br>reliability=%{customdata[1]:.3f}<extra></extra>",
        ))
    elif color_mode == "Reliability" and "reliability" in frame:
        figure.add_trace(go.Scatter3d(
            x=frame["x"], y=frame["y"], z=frame["z"], mode="markers", name="Reliability",
            marker={
                "size": point_size,
                "color": frame["reliability"],
                "colorscale": "Viridis",
                "cmin": 0,
                "cmax": 1,
                "opacity": opacity,
                "colorbar": {"title": "Reliability", "thickness": 14},
            },
            customdata=frame.get("anatomy", pd.Series([""] * len(frame))),
            hovertemplate="x=%{x:.3f}<br>y=%{y:.3f}<br>z=%{z:.3f}<br>region=%{customdata}<br>reliability=%{marker.color:.3f}<extra></extra>",
        ))
    else:
        requested = color_mode.lower()
        group_column = "anatomy" if color_mode == "Anatomical region" and "anatomy" in frame else requested
        group_column = group_column if group_column in frame.columns else "region"
        for value in frame[group_column].astype(str).unique():
            subset = frame[frame[group_column].astype(str) == value]
            if group_column == "label" and {"red", "green", "blue"}.issubset(subset.columns):
                red, green, blue = subset[["red", "green", "blue"]].iloc[0].astype(int)
                color = f"rgb({red},{green},{blue})"
                display_name = f"Label {value}"
            elif group_column == "branch":
                branch_colors = {"1": "#6B5DD3", "2": "#E59F3A"}
                color = branch_colors.get(value, "#657788")
                display_name = f"Branch {value}"
            else:
                color = colors.get(value, "#6B5DD3")
                display_name = value
            figure.add_trace(go.Scatter3d(
                x=subset["x"], y=subset["y"], z=subset["z"],
                mode="markers", name=display_name,
                marker={"size": point_size, "color": color, "opacity": opacity},
                customdata=subset.get("reliability", pd.Series([np.nan] * len(subset))),
                hovertemplate="x=%{x:.3f}<br>y=%{y:.3f}<br>z=%{z:.3f}<br>reliability=%{customdata:.3f}<extra>" + display_name + "</extra>",
            ))
    figure.update_layout(
        height=540,
        margin={"l": 0, "r": 0, "t": 12, "b": 0},
        legend={"orientation": "h", "y": 1.04, "x": 0, "title": {"text": ""}},
        paper_bgcolor="rgba(0,0,0,0)",
        scene={
            "aspectmode": "data",
            "xaxis": {"title": "X", "showbackground": False, "visible": show_axes},
            "yaxis": {"title": "Y", "showbackground": False, "visible": show_axes},
            "zaxis": {"title": "Z", "showbackground": False, "visible": show_axes},
        },
    )
    return figure


def mask_slice_figure(volume: np.ndarray, axis: str, index: int) -> go.Figure:
    """Render a discrete 3D label-mask slice using explicit numeric codes."""

    axis_index = {"Sagittal": 0, "Coronal": 1, "Axial": 2}[axis]
    view = np.rot90(np.take(volume, index, axis=axis_index))
    colors = ["#090B10", "#DC143C", "#0066FF", "#228B22", "#A0522D"]
    colorscale = []
    for color_index, color in enumerate(colors):
        lower = color_index / len(colors)
        upper = (color_index + 1) / len(colors)
        colorscale.extend([[lower, color], [max(lower, upper - 1e-6), color]])
    figure = go.Figure(go.Heatmap(
        z=view,
        zmin=-0.5,
        zmax=4.5,
        colorscale=colorscale,
        colorbar={"title": "Mask code", "tickmode": "array", "tickvals": [0, 1, 2, 3, 4]},
        hovertemplate="row=%{y}<br>column=%{x}<br>mask code=%{z}<extra></extra>",
    ))
    figure.update_layout(
        height=540,
        margin={"l": 0, "r": 0, "t": 12, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis={"visible": False, "scaleanchor": "y"},
        yaxis={"visible": False, "autorange": "reversed"},
    )
    return figure


def raw_mri_slice_figure(
    raw_volume: np.ndarray,
    mask_volume: np.ndarray,
    axis: str,
    index: int,
    display_mode: str = "Raw MRI",
    window_lower: float | None = None,
    window_upper: float | None = None,
    overlay_opacity: float = 0.45,
) -> go.Figure:
    """Render an aligned raw-intensity MRI, mask, or transparent overlay."""

    if raw_volume.shape != mask_volume.shape:
        raise ValueError("Raw MRI and mask shapes must match before synchronized viewing")
    if display_mode == "Mask only":
        return mask_slice_figure(mask_volume, axis, index)
    if display_mode not in {"Raw MRI", "Raw + mask overlay", "Brain-only MRI", "Brain + region overlay"}:
        raise ValueError(f"Unsupported MRI display mode: {display_mode}")

    axis_index = {"Sagittal": 0, "Coronal": 1, "Axial": 2}[axis]
    raw_view = np.rot90(np.take(raw_volume, index, axis=axis_index)).astype(np.float32, copy=False)
    mask_view = np.rot90(np.take(mask_volume, index, axis=axis_index))
    if display_mode in {"Brain-only MRI", "Brain + region overlay"}:
        raw_view = np.where(mask_view > 0, raw_view, np.nan)
    finite = raw_view[np.isfinite(raw_view)]
    if not finite.size:
        raise ValueError("MRI slice contains no finite intensities")
    lower = float(np.percentile(finite, 1)) if window_lower is None else float(window_lower)
    upper = float(np.percentile(finite, 99)) if window_upper is None else float(window_upper)
    if upper <= lower:
        upper = lower + 1e-7

    figure = go.Figure()
    figure.add_trace(go.Heatmap(
        z=raw_view,
        zmin=lower,
        zmax=upper,
        colorscale="Gray",
        showscale=True,
        colorbar={"title": "MRI intensity", "thickness": 13, "x": 1.01},
        customdata=mask_view,
        hovertemplate="row=%{y}<br>column=%{x}<br>intensity=%{z:.3f}<br>mask code=%{customdata}<extra></extra>",
    ))
    if display_mode in {"Raw + mask overlay", "Brain + region overlay"}:
        overlay = mask_view.astype(float)
        overlay[overlay == 0] = np.nan
        overlay_colorscale = [
            [0.0, "rgba(220,20,60,1)"],
            [0.249999, "rgba(220,20,60,1)"],
            [0.25, "rgba(0,102,255,1)"],
            [0.499999, "rgba(0,102,255,1)"],
            [0.50, "rgba(34,139,34,1)"],
            [0.749999, "rgba(34,139,34,1)"],
            [0.75, "rgba(160,82,45,1)"],
            [1.0, "rgba(160,82,45,1)"],
        ]
        figure.add_trace(go.Heatmap(
            z=overlay,
            zmin=1,
            zmax=4,
            colorscale=overlay_colorscale,
            opacity=float(np.clip(overlay_opacity, 0.0, 1.0)),
            colorbar={
                "title": "Mask code",
                "tickmode": "array",
                "tickvals": [1, 2, 3, 4],
                "thickness": 13,
                "x": 1.13,
            },
            hovertemplate="mask code=%{z}<extra>aligned overlay</extra>",
        ))
    figure.update_layout(
        height=560,
        margin={"l": 0, "r": 78 if display_mode in {"Raw + mask overlay", "Brain + region overlay"} else 48, "t": 12, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis={"visible": False, "scaleanchor": "y"},
        yaxis={"visible": False, "autorange": "reversed"},
    )
    return figure


def parse_point_cloud(name: str, content: bytes, max_points: int = 20000) -> pd.DataFrame:
    """Parse CSV, NPY, or ASCII PLY data; reject ambiguous or oversized inputs."""

    lower = name.lower()
    if lower.endswith(".csv"):
        frame = pd.read_csv(BytesIO(content))
        normalized = {str(column).strip().lower(): column for column in frame.columns}
        if not all(axis in normalized for axis in ("x", "y", "z")):
            raise ValueError("CSV must contain x, y, and z columns")
        frame = frame.rename(columns={normalized[axis]: axis for axis in ("x", "y", "z")})
        frame = frame[["x", "y", "z"]].apply(pd.to_numeric, errors="coerce").dropna()
    elif lower.endswith(".npy"):
        array = np.load(BytesIO(content), allow_pickle=False)
        if array.ndim != 2 or array.shape[1] < 3:
            raise ValueError("NPY must be a numeric N x 3 (or wider) array")
        frame = pd.DataFrame(array[:, :3], columns=["x", "y", "z"])
    elif lower.endswith(".ply"):
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("This build supports ASCII PLY, not binary PLY") from error
        lines = text.splitlines()
        if "end_header" not in lines or "format ascii 1.0" not in lines[:20]:
            raise ValueError("PLY must use the ASCII 1.0 format")
        header_end = lines.index("end_header")
        header = lines[: header_end + 1]
        try:
            declared_vertices = int(next(line.split()[-1] for line in header if line.startswith("element vertex ")))
        except (StopIteration, ValueError) as error:
            raise ValueError("PLY header must declare its vertex count") from error
        properties = [line.split()[-1] for line in header if line.startswith("property ")]
        if not all(axis in properties for axis in ("x", "y", "z")):
            raise ValueError("PLY must contain x, y, and z vertex properties")
        array = np.loadtxt(StringIO("\n".join(lines[header_end + 1 :])), dtype=float)
        if array.ndim != 2 or len(array) != declared_vertices or array.shape[1] != len(properties):
            raise ValueError("PLY vertex data do not match the header")
        frame = pd.DataFrame(array, columns=properties)
        for integer_column in ("red", "green", "blue", "label", "branch"):
            if integer_column in frame:
                frame[integer_column] = frame[integer_column].round().astype(int)
    else:
        raise ValueError("Supported point-cloud formats in this build: CSV, NPY, and ASCII PLY")
    if frame.empty:
        raise ValueError("No valid points were found")
    if len(frame) > max_points:
        positions = np.linspace(0, len(frame) - 1, max_points, dtype=int)
        frame = frame.iloc[positions].copy()
    if "region" not in frame:
        frame["region"] = "Uploaded"
    return frame

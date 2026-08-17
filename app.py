"""NeuroAPS Clinical Research Workspace."""

from __future__ import annotations

import json
from pathlib import Path

import nibabel as nib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.knowledge_base import KnowledgeBase, build_extractive_answer, build_manifest, load_records
from src.llm import external_llm_available, synthesize_public_evidence
from src.project_data import (
    BASELINE_COMPARISON,
    FACTORS,
    PIPELINE,
    POINT_LABELS,
    POLICY_COVERAGE,
    POLICY_SOURCES,
    PUBLIC_DOMAIN_SOURCES,
    READINESS_DIMENSIONS,
    SCENARIO,
    SCORE_LABEL,
)
from src.sample_registry import load_sample_manifest, resolve_sample_path, subject_lookup, validate_manifest_files
from src.viewers import (
    parse_point_cloud,
    point_cloud_figure,
    raw_mri_slice_figure,
)


BASE = Path(__file__).resolve().parent
RECORDS_PATH = BASE / "data" / "knowledge_records.json"
READINESS_IMAGE_PATH = BASE / "assets" / "readiness_efficiency.svg"
PIPELINE_IMAGE_PATH = BASE / "assets" / "y3172_pipeline.svg"
POLICY_IMAGE_PATH = BASE / "assets" / "policy_alignment.svg"
KNOWLEDGE_IMAGE_PATH = BASE / "assets" / "knowledge_rag.svg"
PLATFORM_VISION_IMAGE_PATH = BASE / "assets" / "neurocloud_platform_vision.png"
HACKATHON_BOARD_IMAGE_PATH = BASE / "assets" / "hackathon_storyboard.png"
CONTEXT_IMAGE_PATHS = {
    "The problem: fragmented data and delayed diagnosis": BASE / "assets" / "problem_inefficient_neuroimaging.png",
    "Current workflow: manual analysis": BASE / "assets" / "current_manual_analysis.png",
    "Root causes of delayed diagnosis": BASE / "assets" / "root_cause_delayed_diagnosis.png",
    "Why it matters in Saudi Arabia": BASE / "assets" / "saudi_neurological_impact.png",
}
SAMPLES_MANIFEST_PATH = BASE / "data" / "samples" / "sample_manifest.json"

st.set_page_config(
    page_title="NeuroAPS | AI-Ready Neuroimaging",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root { --navy:#10243A; --teal:#167C86; --green:#0B7A5C; --red:#C8405B; --gold:#D7952B; --line:#DDE6EC; }
    html, body, [class*="css"] {font-family:Inter,Segoe UI,Arial,sans-serif;}
    .block-container {padding-top: 1.35rem; padding-bottom: 3rem; max-width: 1480px;}
    [data-testid="stSidebar"] {border-right:1px solid var(--line);background:#F7FAFC;}
    .hero {padding:1.45rem 1.65rem;border:1px solid #D6E3E8;border-radius:20px;
           background:linear-gradient(120deg,#FFFFFF 0%,#EAF6F5 54%,#EEF2FB 100%);margin-bottom:1rem;
           box-shadow:0 10px 28px rgba(16,36,58,.06);}
    .hero h1 {color:var(--navy);margin:.12rem 0 .35rem;font-size:2.15rem;line-height:1.12;letter-spacing:-.02em;}
    .eyebrow {color:var(--teal);font-weight:800;letter-spacing:.09em;font-size:.74rem;}
    .subtle {color:#536A78;font-size:.95rem;margin:.15rem 0 .65rem;}
    .guardrail {padding:.8rem 1rem;border-left:5px solid #C43B51;background:#FFF2F4;border-radius:8px;}
    .status-chip {display:inline-block;padding:.24rem .68rem;border-radius:999px;background:#E7F4F1;
                  color:#09644D;font-size:.76rem;font-weight:750;margin:.15rem .28rem .05rem 0;}
    .source-card {border:1px solid #DCE4EC;border-radius:12px;padding:.8rem 1rem;background:white;margin:.4rem 0;}
    .smallcaps {font-size:.72rem;letter-spacing:.07em;text-transform:uppercase;color:#657788;font-weight:700;}
    div[data-testid="stMetric"] {background:#FFFFFF;border:1px solid var(--line);padding:.82rem 1rem;border-radius:14px;
                                  box-shadow:0 4px 14px rgba(16,36,58,.035);}
    div[data-testid="stTabs"] button {font-weight:700;padding-left:.8rem;padding-right:.8rem;}
    .section-banner {border:1px solid var(--line);border-radius:16px;padding:1rem 1.1rem;background:#FFFFFF;
                     box-shadow:0 5px 18px rgba(16,36,58,.04);margin:.25rem 0 .85rem;}
    .section-banner h3 {color:var(--navy);margin:0 0 .25rem;font-size:1.15rem;}
    .section-banner p {color:#5C707D;margin:0;font-size:.9rem;}
    .comparison-card {height:100%;padding:1rem 1.05rem;border:1px solid var(--line);border-radius:15px;background:#FFFFFF;}
    .comparison-card.cnn {border-top:4px solid #778797;}
    .comparison-card.ours {border-top:4px solid var(--teal);background:linear-gradient(180deg,#FFFFFF,#F2FAF9);}
    .comparison-card h4 {color:var(--navy);margin:0 0 .5rem;}
    .comparison-card ul {margin:.35rem 0 0;padding-left:1.15rem;color:#4F6471;font-size:.9rem;}
    .comparison-card li {margin:.35rem 0;}
    .step-card {min-height:145px;padding:.85rem .9rem;border:1px solid var(--line);border-radius:14px;background:#FFFFFF;}
    .step-no {display:inline-flex;width:28px;height:28px;align-items:center;justify-content:center;border-radius:50%;
              background:#DDF1EE;color:#0A6A54;font-weight:800;margin-bottom:.4rem;}
    .step-card h4 {margin:.1rem 0 .3rem;color:var(--navy);font-size:.93rem;}
    .step-card p {margin:0;color:#5A6D78;font-size:.82rem;line-height:1.38;}
    .arrow-flow {display:flex;align-items:center;justify-content:center;height:500px;font-size:2.1rem;color:var(--teal);font-weight:900;}
    .region-row {display:flex;gap:.55rem;flex-wrap:wrap;margin:.25rem 0 .8rem;}
    .region-chip {padding:.42rem .7rem;border:1px solid var(--line);border-radius:999px;background:#FFFFFF;
                  color:#324D5E;font-size:.8rem;font-weight:700;}
    .dot {display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:.4rem;}
    .policy-card {padding:.9rem 1rem;border:1px solid var(--line);border-radius:14px;background:#FFFFFF;margin:.45rem 0;}
    .policy-card h4 {margin:0 0 .25rem;color:var(--navy);font-size:1rem;}
    .policy-card p {margin:.22rem 0;color:#566B77;font-size:.86rem;}
    .verified {color:#0B7A5C;font-weight:800;font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;}
    .context-card {padding:1rem 1.1rem;border:1px solid var(--line);border-radius:15px;background:#FFFFFF;
                   box-shadow:0 5px 18px rgba(16,36,58,.04);}
    .context-card h3 {margin:0 0 .45rem;color:var(--navy);font-size:1.2rem;}
    .context-card p {margin:.25rem 0;color:#536A78;font-size:.91rem;line-height:1.5;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def get_knowledge_base() -> tuple[list[dict], KnowledgeBase]:
    loaded = load_records(RECORDS_PATH)
    return loaded, KnowledgeBase(loaded)


def readiness_radar() -> go.Figure:
    labels = [factor["name"] for factor in FACTORS]
    values = [factor["score"] for factor in FACTORS]
    figure = go.Figure(go.Scatterpolar(
        r=values + values[:1],
        theta=labels + labels[:1],
        fill="toself",
        line={"color": "#2E6C7C", "width": 3},
        fillcolor="rgba(46,108,124,.20)",
        hovertemplate="%{theta}: %{r}/3<extra></extra>",
    ))
    figure.update_layout(
        height=470,
        margin={"l": 55, "r": 55, "t": 35, "b": 35},
        paper_bgcolor="rgba(0,0,0,0)",
        polar={"radialaxis": {"range": [0, 3], "tickvals": [0, 1, 2, 3]}, "bgcolor": "rgba(0,0,0,0)"},
        showlegend=False,
    )
    return figure


def baseline_chart(metric_index: int, title: str, suffix: str) -> go.Figure:
    """Render one published benchmark metric without mixing incompatible scales."""

    names = [row[0] for row in BASELINE_COMPARISON]
    values = [row[metric_index] for row in BASELINE_COMPARISON]
    colors = ["#A7B5C0" if name != "NeuroAPS-Net" else "#167C86" for name in names]
    figure = go.Figure(go.Bar(
        x=values,
        y=names,
        orientation="h",
        marker_color=colors,
        text=[f"{value:,.2f}{suffix}" for value in values],
        textposition="outside",
        hovertemplate=f"%{{y}}<br>{title}: %{{x:,.2f}}{suffix}<extra></extra>",
    ))
    figure.update_layout(
        height=285,
        margin={"l": 15, "r": 65, "t": 42, "b": 20},
        title={"text": title, "font": {"size": 15, "color": "#10243A"}},
        xaxis={"visible": False},
        yaxis={"autorange": "reversed", "title": ""},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    return figure


def policy_heatmap() -> go.Figure:
    factor_names = [factor["name"] for factor in FACTORS]
    documents = list(POLICY_COVERAGE)
    values = [POLICY_COVERAGE[document] for document in documents]
    labels = [[SCORE_LABEL[value] for value in row] for row in values]
    figure = go.Figure(go.Heatmap(
        z=values,
        x=factor_names,
        y=documents,
        zmin=0,
        zmax=3,
        colorscale=[[0, "#B4233A"], [0.33, "#C77B17"], [0.67, "#2E6C7C"], [1, "#0B6E4F"]],
        text=labels,
        texttemplate="%{text}",
        hovertemplate="%{y}<br>%{x}<br>%{text}<extra></extra>",
        showscale=False,
    ))
    figure.update_layout(
        height=420,
        margin={"l": 30, "r": 20, "t": 20, "b": 90},
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis={"tickangle": -25},
    )
    return figure


@st.cache_data(show_spinner=False)
def get_sample_registry() -> tuple[dict, dict[str, dict]]:
    manifest = load_sample_manifest(SAMPLES_MANIFEST_PATH)
    errors = validate_manifest_files(manifest, BASE)
    if errors:
        raise ValueError("; ".join(errors))
    return manifest, subject_lookup(manifest)


@st.cache_data(show_spinner=False)
def load_registered_nifti(relative_path: str) -> np.ndarray:
    path = resolve_sample_path(BASE, relative_path)
    image = nib.load(str(path))
    data = np.asanyarray(image.dataobj)
    if data.ndim != 3:
        raise ValueError("Registered NIfTI mask must contain one 3D volume")
    if max(data.shape) > 1024:
        raise ValueError("Registered volume dimensions exceed the viewer safety limit")
    return data


@st.cache_data(show_spinner=False)
def load_registered_point_cloud(relative_path: str) -> pd.DataFrame:
    path = resolve_sample_path(BASE, relative_path)
    frame = parse_point_cloud(path.name, path.read_bytes(), max_points=20000)
    frame["anatomy"] = frame["label"].astype(int).map(POINT_LABELS).fillna("Unmapped region")
    return frame


try:
    records, kb = get_knowledge_base()
except (OSError, ValueError, json.JSONDecodeError) as error:
    st.error(f"The characterized knowledge base could not be loaded: {error}")
    st.stop()

try:
    sample_manifest, paired_subjects = get_sample_registry()
    sample_registry_error = None
except (OSError, ValueError, json.JSONDecodeError) as error:
    sample_manifest, paired_subjects = None, {}
    sample_registry_error = str(error)


with st.sidebar:
    st.markdown("## 🧠 NeuroAPS Workspace")
    st.caption("Resource-efficient Alzheimer’s neuroimaging research")
    st.divider()
    with st.popover("Evidence mode", use_container_width=True):
        st.success(f"Offline retrieval active · {len(records)} records · {len(kb.chunks)} chunks")
        if sample_registry_error:
            st.error("Paired-sample registry unavailable")
        else:
            st.success(f"Imaging workspace · {sample_manifest['triple_count']} subject sets")
        if external_llm_available():
            use_external_llm = st.toggle(
                "Use external LLM synthesis",
                value=False,
                help="Only public retrieved KB excerpts are sent. Uploaded scans and point clouds are never sent.",
            )
            st.warning("External mode is locally enabled. Review the evidence panel for every answer.")
        else:
            use_external_llm = False
            st.info("External LLM disabled. The complete KB workflow remains functional offline.")
    st.divider()
    st.markdown("**Research boundary**")
    st.caption("Published evidence supports the assistant. Imaging data and local uploads remain separate from the evidence index.")
    st.divider()
    st.caption("For research use only. This output is not a clinical diagnosis.")


st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">AI READINESS · NEUROIMAGING · SAUDI ARABIA</div>
      <h1>NeuroAPS Clinical Research Workspace</h1>
      <p class="subtle">From brain MRI to an anatomically labelled point cloud, with deployment evidence, standards mapping, and policy-grounded research support.</p>
      <span class="status-chip">7 characterized records</span>
      <span class="status-chip">10 real subject examples</span>
      <span class="status-chip">Offline evidence assistant</span>
      <span class="status-chip">Y.3172 mapped</span>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_columns = st.columns(5)
metric_columns[0].metric("Reported accuracy", "84.85%", help="Published experiment evidence supplied in the knowledge records")
metric_columns[1].metric("Inference latency", "1.48 ms", help="Reported on one NVIDIA RTX 3060")
metric_columns[2].metric("Peak GPU memory", "234.6 MB", help="Reported deployment evidence")
metric_columns[3].metric("ADNI-2DPC cohort", "1,000", help="500 AD and 500 CN subjects in the supplied project record")
metric_columns[4].metric(
    "Local subject triples",
    "10",
    help="AD1–AD10 raw intensity MRI, aligned NIfTI label mask, and matching 8,192-point PLY",
)

tabs = st.tabs([
    "Context & Impact",
    "Readiness",
    "Y.3172 Workflow",
    "MRI → Point Cloud",
    "Policy Alignment",
    "Evidence Library",
    "Research Assistant",
    "Deployment",
])


with tabs[0]:
    vision_column, message_column = st.columns([1.25, 0.75], gap="large", vertical_alignment="center")
    with vision_column:
        if PLATFORM_VISION_IMAGE_PATH.exists():
            st.image(str(PLATFORM_VISION_IMAGE_PATH), width="stretch")
        st.caption("NeuroCloud AI is the hackathon platform concept; NeuroAPS is the research workflow demonstrated in this build.")
    with message_column:
        st.markdown(
            """
            <div class="context-card">
              <div class="smallcaps">Application story</div>
              <h3>From fragmented imaging to a research-ready workflow</h3>
              <p>The workspace connects brain-only MRI viewing, an anatomical point cloud, readiness evidence, Saudi public sources, and human review in one interface.</p>
              <p>The current release is a research demonstrator. It does not claim clinical deployment, regulatory approval, or a hospital partnership.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("#### Explore the problem context")
    selected_context = st.selectbox(
        "Concept visual",
        list(CONTEXT_IMAGE_PATHS),
        key="context_story",
        label_visibility="collapsed",
    )
    selected_context_path = CONTEXT_IMAGE_PATHS[selected_context]
    if selected_context_path.exists():
        st.image(str(selected_context_path), width="stretch")
    st.caption(
        "ITU Hackathon concept visual supplied for this application. It supports the problem narrative; "
        "quantitative and policy claims are governed by the validated sources in Policy Alignment."
    )


with tabs[1]:
    st.subheader("Application readiness")
    st.caption("Coverage combines the two published studies with functions implemented in this demonstrator.")
    chart_left, chart_column, chart_right = st.columns([0.18, 0.64, 0.18])
    with chart_column:
        st.plotly_chart(readiness_radar(), width="stretch", config={"displayModeBar": False})

    for factor in FACTORS:
        with st.expander(f"{factor['name']} — {SCORE_LABEL[factor['score']]}"):
            st.markdown(f"**Coverage:** {factor['coverage']}")
            st.markdown(f"**Evidence:** {factor['evidence']}")

    st.divider()
    st.subheader("Why the proposed representation fits constrained clinical settings")
    image_column, comparison_column = st.columns([0.9, 1.35], gap="large", vertical_alignment="center")
    with image_column:
        if READINESS_IMAGE_PATH.exists():
            st.image(str(READINESS_IMAGE_PATH), width="stretch")
    with comparison_column:
        cnn_column, ours_column = st.columns(2, gap="medium")
        cnn_column.markdown(
            """
            <div class="comparison-card cnn">
              <h4>Dense 3D CNN constraint</h4>
              <ul>
                <li>Processes the full voxel grid rather than a compact anatomical representation.</li>
                <li>Higher memory and compute demand can limit smaller-clinic deployment.</li>
                <li>The supplied records describe this limitation qualitatively; no harmonized 3D-CNN benchmark is claimed here.</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        ours_column.markdown(
            """
            <div class="comparison-card ours">
              <h4>NeuroAPS-Net finding</h4>
              <ul>
                <li><b>84.85%</b> reported accuracy using 8,192 anatomically selected points.</li>
                <li><b>1.48 ms</b> inference and <b>234.6 MB</b> peak GPU memory.</li>
                <li>Measured on a single consumer NVIDIA RTX 3060, supporting resource-conscious deployment planning.</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("#### Published comparison at 8,192 points")
    accuracy_column, latency_column, memory_column = st.columns(3, gap="medium")
    accuracy_column.plotly_chart(baseline_chart(1, "Accuracy", "%"), width="stretch", config={"displayModeBar": False})
    latency_column.plotly_chart(baseline_chart(2, "Inference latency", " ms"), width="stretch", config={"displayModeBar": False})
    memory_column.plotly_chart(baseline_chart(3, "Peak GPU memory", " MB"), width="stretch", config={"displayModeBar": False})
    st.caption("Values are the supplied paper results for point-cloud baselines. They are not a fabricated voxel-CNN comparison.")

    st.divider()
    st.subheader("Thirteen readiness dimensions: research baseline and application coverage")
    dimension_frame = pd.DataFrame(
        READINESS_DIMENSIONS,
        columns=["Dimension", "Papers-only rating", "Application coverage", "Evidence in this build", "Next evaluation"],
    )
    rating_filter = st.multiselect(
        "Filter application coverage",
        sorted(dimension_frame["Application coverage"].unique()),
        default=[],
        placeholder="Show all dimensions",
    )
    if rating_filter:
        dimension_frame = dimension_frame[dimension_frame["Application coverage"].isin(rating_filter)]
    st.dataframe(dimension_frame, hide_index=True, width="stretch", height=540)

    st.divider()
    st.subheader("Human-in-the-loop evaluation scenario")
    for row_start in (0, 3):
        scenario_columns = st.columns(3, gap="medium")
        for column, (number, title, description) in zip(scenario_columns, SCENARIO[row_start:row_start + 3]):
            column.markdown(
                f'<div class="step-card"><span class="step-no">{number}</span><h4>{title}</h4><p>{description}</p></div>',
                unsafe_allow_html=True,
            )


with tabs[2]:
    intro_column, image_column = st.columns([1.25, 0.75], gap="large", vertical_alignment="center")
    with intro_column:
        st.subheader("ITU-T Y.3172-aligned workflow")
        st.caption("Every node is mapped to a concrete function, current evidence, and application state.")
    with image_column:
        if PIPELINE_IMAGE_PATH.exists():
            st.image(str(PIPELINE_IMAGE_PATH), width="stretch")
    status_options = sorted({row[2] for row in PIPELINE})
    selected_status = st.multiselect("Status", status_options, default=status_options)
    pipeline_frame = pd.DataFrame(PIPELINE, columns=["Y.3172 node", "Application function", "Status", "Evidence in this build"])
    pipeline_frame = pipeline_frame[pipeline_frame["Status"].isin(selected_status)]
    st.dataframe(pipeline_frame, hide_index=True, width="stretch", height=500)

    st.markdown("#### Operational sequence")
    flow_columns = st.columns(4)
    flow = [
        ("SRC + C", "Register the MRI case and connect its representations"),
        ("PP + M", "Create the anatomical point cloud and produce model evidence"),
        ("P + D", "Apply review rules and present traceable evidence"),
        ("SINK", "Clinician reviews, escalates, and records the decision"),
    ]
    for column, (node, action) in zip(flow_columns, flow):
        column.info(f"**{node}**\n\n{action}")


with tabs[3]:
    st.subheader("Brain MRI → anatomically labelled point cloud")
    st.caption("Select a subject, inspect the brain-only MRI, and explore the corresponding lightweight point-cloud representation.")

    if sample_registry_error:
        st.error(f"The imaging workspace could not be loaded: {sample_registry_error}")
    else:
        subject_ids = sorted(paired_subjects, key=lambda value: int(value.removeprefix("AD")))
        selector_column, color_column, size_column, opacity_column = st.columns([1.1, 1.15, 0.75, 0.75])
        selected_subject = selector_column.selectbox("Subject", subject_ids, key="registered_subject")
        color_mode = color_column.selectbox("Point-cloud view", ["Anatomical region", "Reliability", "File RGB"])
        point_size = size_column.slider("Point size", 1, 7, 3)
        point_opacity = opacity_column.slider("Opacity", 0.25, 1.00, 0.78, 0.05)

        subject_record = paired_subjects[selected_subject]
        try:
            registered_raw = load_registered_nifti(subject_record["raw_mri"]["relative_path"])
            registered_mask = load_registered_nifti(subject_record["segmentation_mask"]["relative_path"])
            registered_cloud = load_registered_point_cloud(subject_record["point_cloud"]["relative_path"])
            if registered_raw.shape != registered_mask.shape:
                raise ValueError("MRI and brain mask shapes differ")
        except Exception as error:
            st.error(f"The selected subject could not be opened: {error}")
            registered_raw = registered_mask = registered_cloud = None

        if registered_raw is not None and registered_mask is not None and registered_cloud is not None:
            raw_metadata = subject_record["raw_mri"]
            intensity = raw_metadata["intensity"]
            spacing = raw_metadata["voxel_spacing"]
            summary_columns = st.columns(5)
            summary_columns[0].metric("Subject", selected_subject)
            summary_columns[1].metric("Volume", " × ".join(map(str, registered_raw.shape)))
            summary_columns[2].metric("Voxel spacing", " × ".join(f"{value:.2f}" for value in spacing) + " mm")
            summary_columns[3].metric("Brain voxels", f"{np.count_nonzero(registered_mask):,}")
            summary_columns[4].metric("Point cloud", f"{len(registered_cloud):,} points")

            axis_column, slice_column, contrast_column, region_column, reliability_column = st.columns([0.8, 1.3, 1.15, 1.55, 1.15])
            view_axis = axis_column.selectbox("Plane", ["Axial", "Coronal", "Sagittal"])
            axis_index = {"Sagittal": 0, "Coronal": 1, "Axial": 2}[view_axis]
            slice_number = slice_column.slider(
                "Slice",
                0,
                registered_raw.shape[axis_index] - 1,
                registered_raw.shape[axis_index] // 2,
                key=f"slice_{selected_subject}_{view_axis}",
            )
            contrast = contrast_column.selectbox("MRI contrast", ["Balanced", "Tissue focus", "Full range"])
            available_regions = [
                POINT_LABELS[label]
                for label in sorted(registered_cloud["label"].astype(int).unique())
                if label in POINT_LABELS
            ]
            selected_regions = region_column.multiselect("Anatomical regions", available_regions, default=available_regions)
            reliability_threshold = reliability_column.slider("Minimum reliability", 0.0, 1.0, 0.0, 0.05)

            percentiles = intensity["nonzero_percentiles"]
            if contrast == "Balanced":
                window_lower, window_upper = percentiles["1.0"], percentiles["99.0"]
            elif contrast == "Tissue focus":
                window_lower, window_upper = percentiles["5.0"], percentiles["95.0"]
            else:
                window_lower, window_upper = intensity["minimum"], intensity["maximum"]

            filtered_cloud = registered_cloud[
                registered_cloud["anatomy"].isin(selected_regions)
                & (registered_cloud["reliability"] >= reliability_threshold)
            ].copy()

            st.markdown(
                """
                <div class="region-row">
                  <span class="region-chip"><span class="dot" style="background:#E04F6F"></span>Label 1 · Hippocampus</span>
                  <span class="region-chip"><span class="dot" style="background:#16A6B6"></span>Label 3 · Ventricles</span>
                  <span class="region-chip"><span class="dot" style="background:#7C5CE5"></span>Label 5 · Cortical area</span>
                  <span class="region-chip"><span class="dot" style="background:#E7A83E"></span>Label 7 · Other brain tissue</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            mri_column, arrow_column, point_column = st.columns([1.0, 0.10, 1.30], gap="medium")
            with mri_column:
                st.markdown(f"#### {selected_subject} brain MRI")
                st.plotly_chart(
                    raw_mri_slice_figure(
                        registered_raw,
                        registered_mask,
                        view_axis,
                        slice_number,
                        display_mode="Brain-only MRI",
                        window_lower=window_lower,
                        window_upper=window_upper,
                    ),
                    width="stretch",
                    config={"displaylogo": False, "scrollZoom": True},
                    key=f"brain_mri_{selected_subject}_{view_axis}_{contrast}",
                )
                st.caption(f"{view_axis} slice {slice_number} · brain portion only")
            with arrow_column:
                st.markdown('<div class="arrow-flow">→</div>', unsafe_allow_html=True)
            with point_column:
                st.markdown(f"#### {selected_subject} point-cloud version")
                if filtered_cloud.empty:
                    st.warning("Choose at least one region or lower the reliability threshold.")
                else:
                    st.plotly_chart(
                        point_cloud_figure(
                            filtered_cloud,
                            point_size=point_size,
                            opacity=point_opacity,
                            color_mode=color_mode,
                            show_axes=True,
                        ),
                        width="stretch",
                        config={"displaylogo": False, "scrollZoom": True},
                        key=f"point_cloud_{selected_subject}_{color_mode}",
                    )
                    st.caption(f"{len(filtered_cloud):,} of {len(registered_cloud):,} points displayed")


with tabs[4]:
    intro_column, image_column = st.columns([1.25, 0.75], gap="large", vertical_alignment="center")
    with intro_column:
        st.subheader("Saudi policy and digital-health alignment")
        st.caption("Claims are limited to supplied public-domain notes and sources revalidated on 17 August 2026.")
    with image_column:
        if POLICY_IMAGE_PATH.exists():
            st.image(str(POLICY_IMAGE_PATH), width="stretch")

    st.plotly_chart(policy_heatmap(), width="stretch", config={"displayModeBar": False})

    st.markdown("#### Validated public evidence")
    for row_start in (0, 2):
        source_columns = st.columns(2, gap="medium")
        for column, source in zip(source_columns, POLICY_SOURCES[row_start:row_start + 2]):
            column.markdown(
                f"""
                <div class="policy-card">
                  <div class="verified">Official source verified</div>
                  <h4>{source['source']}</h4>
                  <p><b>{source['authority']}</b> · {source['supports']}</p>
                  <p><b>Application translation:</b> {source['application']}</p>
                  <p><a href="{source['url']}" target="_blank">Open official source ↗</a></p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("#### Saudi public-domain data and links")
    source_tiers = ["All sources"] + sorted({source["tier"] for source in PUBLIC_DOMAIN_SOURCES})
    selected_tier = st.selectbox("Source category", source_tiers, key="saudi_source_tier")
    public_sources = PUBLIC_DOMAIN_SOURCES
    if selected_tier != "All sources":
        public_sources = [source for source in public_sources if source["tier"] == selected_tier]
    public_source_frame = pd.DataFrame(public_sources).rename(columns={
        "tier": "Source type",
        "source": "Source",
        "publisher": "Publisher",
        "supports": "What it supports",
        "url": "Public link",
        "verified": "Checked",
    })
    st.dataframe(
        public_source_frame,
        hide_index=True,
        width="stretch",
        column_config={
            "Public link": st.column_config.LinkColumn("Public link", display_text="Open source ↗"),
        },
    )
    st.caption(
        "Government pages and reports are marked as official. Saudipedia and peer-reviewed records are "
        "shown separately as public background or public research."
    )

    st.markdown("#### Application actions")
    action_frame = pd.DataFrame([
        ("HSTP", "Access and digital transformation", "Resource-efficient MRI decision support for specialist workflows", "Mapped"),
        ("NSDAI", "Data and AI for healthcare access and preventive care", "Traceable evidence, governed model context, and research collaboration", "Mapped"),
        ("Seha Virtual Hospital", "Remote specialist care, teleradiology, sandbox, clinical research", "Candidate pathway for controlled evaluation", "Evidence-based pathway"),
        ("PDPL / AI Ethics", "Privacy, governance, compliance, and human oversight", "De-identification, local processing, auditability, and clinician review", "Designed"),
    ], columns=["Source", "Public-policy support", "Application action", "Coverage"])
    st.dataframe(action_frame, hide_index=True, width="stretch")
    st.caption("Alignment does not imply regulatory approval, hospital integration, or partnership.")


with tabs[5]:
    intro_column, image_column = st.columns([1.35, 0.65], gap="large", vertical_alignment="center")
    with intro_column:
        st.subheader("Evidence library")
        st.caption("Search the papers, neuroanatomy background, Eastern Province studies, and Saudi policy sources.")
    with image_column:
        if KNOWLEDGE_IMAGE_PATH.exists():
            st.image(str(KNOWLEDGE_IMAGE_PATH), width="stretch")
    manifest = build_manifest(records)
    manifest_columns = st.columns(4)
    manifest_columns[0].metric("Records", manifest["record_count"])
    manifest_columns[1].metric("Types", len(manifest["record_types"]))
    manifest_columns[2].metric("Retrieval chunks", len(kb.chunks))
    manifest_columns[3].metric("Schema", manifest["schema_version"])

    search_column, type_column = st.columns([1.5, 1])
    record_search = search_column.text_input("Search records", placeholder="hippocampus, Dammam, deployment, policy...")
    selected_types = type_column.multiselect("Record type", kb.record_types, default=[])

    filtered = records
    if selected_types:
        filtered = [record for record in filtered if record["type"] in selected_types]
    if record_search.strip():
        needle = record_search.lower().strip()
        filtered = [
            record for record in filtered
            if needle in " ".join([
                record["title"], record["domain"], record["country_scope"], record["full_text"]
            ]).lower()
        ]
    st.caption(f"Showing {len(filtered)} of {len(records)} records")

    for record in filtered:
        label = f"{record['title']} · {record['type'].replace('_', ' ').title()}"
        with st.expander(label):
            detail_column, metric_column = st.columns([1.5, 1])
            with detail_column:
                st.markdown(f"**Status:** {record['status']}")
                st.markdown(f"**Domain:** {record['domain']}")
                st.markdown(f"**Scope:** {record['country_scope']}")
                st.markdown(f"**Factors:** {', '.join(record['factors']) or '—'}")
                st.markdown(f"**Dimensions:** {', '.join(record['dimensions']) or '—'}")
                public_links = record.get("public_links", [])
                if public_links:
                    st.markdown("**Public sources**")
                    for link in public_links:
                        st.link_button(
                            link["label"],
                            link["url"],
                            width="stretch",
                        )
                elif record.get("reference_link"):
                    st.link_button("Open public reference", record["reference_link"])
            with metric_column:
                st.markdown("**Key metrics**")
                if record["key_metrics"]:
                    for key, value in record["key_metrics"].items():
                        st.markdown(f"- {key.replace('_', ' ').title()}: `{value}`")
                else:
                    st.caption("No numeric metrics registered")
            st.markdown("**Record summary**")
            st.write(record["summary"])
            st.download_button(
                "Download this record as JSON",
                json.dumps(record, indent=2, ensure_ascii=False),
                file_name=f"{record['id']}.json",
                mime="application/json",
                key=f"download_{record['id']}",
            )


with tabs[6]:
    st.subheader("Research evidence assistant")
    mode = "External synthesis over public excerpts" if use_external_llm else "Offline retrieval evidence"
    st.caption(f"Active mode: {mode}. Answers are bounded to the seven records and expose the retrieved chunks.")

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "pending_question" not in st.session_state:
        st.session_state.pending_question = None

    suggestions = [
        "What evidence supports deployment efficiency?",
        "What changes in the hippocampus, ventricles, and cortex in AD?",
        "What is the strongest Dammam-specific precedent?",
        "How does the application align with Saudi health and AI policy?",
    ]
    suggestion_columns = st.columns(4)
    for index, (column, suggestion) in enumerate(zip(suggestion_columns, suggestions)):
        if column.button(suggestion, width="stretch", key=f"suggestion_{index}"):
            st.session_state.pending_question = suggestion

    control_left, control_right = st.columns([1, 4])
    if control_left.button("Clear conversation", width="stretch"):
        st.session_state.chat_messages = []
        st.session_state.pending_question = None
        st.rerun()
    selected_chat_types = control_right.multiselect(
        "Limit retrieval to record types (optional)",
        kb.record_types,
        default=[],
        key="chat_types",
    )

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("hits"):
                with st.expander("Retrieved evidence"):
                    for number, hit in enumerate(message["hits"], start=1):
                        link = f" · [public link]({hit['reference_link']})" if hit.get("reference_link") else ""
                        st.markdown(
                            f"**[{number}] {hit['title']}** · chunk {hit['chunk_id']} · similarity {hit['score']:.3f}{link}"
                        )
                        st.caption(hit["text"][:500] + ("..." if len(hit["text"]) > 500 else ""))

    typed_question = st.chat_input("Ask about the papers, anatomy, Dammam context, policy, or Y.3172 readiness")
    question = typed_question or st.session_state.pending_question
    if question:
        st.session_state.pending_question = None
        hits = kb.retrieve(question, top_k=4, record_types=selected_chat_types)
        if use_external_llm:
            try:
                answer = synthesize_public_evidence(question, hits)
            except Exception as error:
                answer = build_extractive_answer(hits) + f"\n\n_External synthesis failed; offline evidence shown ({error})._"
        else:
            answer = build_extractive_answer(hits)
        st.session_state.chat_messages.extend([
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer, "hits": [hit.to_dict() for hit in hits]},
        ])
        st.rerun()


with tabs[7]:
    st.subheader("Deployment workbench")
    status_frame = pd.DataFrame([
        ("Phase 1", "Interactive synthetic web prototype", "Preserved in legacy_phase1", "Complete"),
        ("Phase 2A", "Characterized evidence library and offline retrieval", "Seven curated records", "Complete"),
        ("Phase 2B", "MRI-derived anatomical point-cloud workspace", "10 paired examples", "Complete"),
        ("Phase 2C", "Brain-only MRI and named anatomical regions", "Hippocampus, ventricles, cortical area, other tissue", "Complete"),
        ("Phase 3", "Versioned NeuroAPS-Net runtime integration", "Model, preprocessing, and class map", "Interface ready"),
        ("Phase 4", "Production hybrid RAG and authenticated evidence store", "Approved infrastructure", "Planned"),
        ("Phase 5", "Security, clinician study, sandbox, deployment validation", "Institutional approvals", "Planned"),
    ], columns=["Phase", "Scope", "Required input", "State"])
    st.dataframe(status_frame, hide_index=True, width="stretch")

    st.markdown("#### Check the next integration bundle")
    supplied = st.file_uploader(
        "Select files for a local readiness check (nothing is uploaded to the KB)",
        accept_multiple_files=True,
        key="integration_files",
    )
    if supplied:
        names = [item.name for item in supplied]
        checks = {
            "Feature table": any(name.lower().endswith((".csv", ".xlsx", ".parquet")) for name in names),
            "MRI sample": any(name.lower().endswith((".nii", ".nii.gz")) for name in names),
            "Point cloud": any(name.lower().endswith((".csv", ".npy", ".ply", ".pcd", ".npz")) for name in names),
            "Model artifact": any(name.lower().endswith((".pt", ".pth", ".onnx", ".joblib", ".pkl")) for name in names),
            "Preprocessing/config": any(name.lower().endswith((".json", ".yaml", ".yml", ".joblib", ".pkl")) for name in names),
            "Experiment results": any("result" in name.lower() or "metric" in name.lower() for name in names),
        }
        st.dataframe(pd.DataFrame(checks.items(), columns=["Required category", "Detected"]), hide_index=True, width="stretch")

    st.info("The deployment adapter is prepared for the versioned NeuroAPS-Net model, preprocessing configuration, and class mapping.")

    with st.expander("Hackathon application storyboard"):
        if HACKATHON_BOARD_IMAGE_PATH.exists():
            st.image(str(HACKATHON_BOARD_IMAGE_PATH), width="stretch")
        st.caption("Concept storyboard supplied for the project; implementation status is defined by the table above.")


st.divider()
st.caption("NeuroAPS Clinical Research Workspace · AI-readiness demonstrator · For research use only · Not a clinical diagnosis")

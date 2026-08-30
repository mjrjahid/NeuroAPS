"""NeuroAPS Clinical Research Workspace."""

from __future__ import annotations

import base64
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
    GOVERNANCE_SCENARIO,
    PIPELINE,
    PDPL_AI_ETHICS_CONTROLS,
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
MRI_POINTCLOUD_IMAGE_PATH = BASE / "assets" / "mri_pointcloud_workspace.svg"
ASSISTANT_IMAGE_PATH = BASE / "assets" / "research_assistant_bot.svg"
DEPLOYMENT_IMAGE_PATH = BASE / "assets" / "deployment_workbench.svg"
HACKATHON_BOARD_IMAGE_PATH = BASE / "assets" / "hackathon_storyboard.png"
CONTEXT_IMAGE_PATHS = {
    "The problem: fragmented data and delayed diagnosis": BASE / "assets" / "problem_inefficient_neuroimaging.png",
    "Current workflow: manual analysis": BASE / "assets" / "current_manual_analysis.png",
    "Root causes of delayed diagnosis": BASE / "assets" / "root_cause_delayed_diagnosis.png",
    "Why it matters in Saudi Arabia": BASE / "assets" / "saudi_neurological_impact.png",
}
SAMPLES_MANIFEST_PATH = BASE / "data" / "samples" / "sample_manifest.json"
WORKSPACE_NAMES = [
    "Context & Impact",
    "Readiness",
    "Y.3172 Workflow",
    "MRI → Point Cloud",
    "Policy Alignment",
    "Evidence Library",
    "Research Assistant",
    "Deployment",
]
WORKSPACE_VISUALS = {
    "Context & Impact": {
        "image": PLATFORM_VISION_IMAGE_PATH,
        "eyebrow": "Clinical context and platform vision",
        "title": "Connect the neuroimaging problem to an actionable research workflow.",
        "description": "Explore the supplied platform story, fragmented-data challenge, manual review burden, and Saudi neurological context.",
        "alt": "NeuroCloud AI brain-imaging platform concept",
    },
    "Readiness": {
        "image": READINESS_IMAGE_PATH,
        "eyebrow": "Application readiness",
        "title": "Move from published evidence to deployment-focused action.",
        "description": "Review thirteen readiness dimensions, human oversight, and resource-conscious performance evidence without inventing unavailable CNN benchmarks.",
        "alt": "NeuroAPS readiness and efficiency illustration",
    },
    "Y.3172 Workflow": {
        "image": PIPELINE_IMAGE_PATH,
        "eyebrow": "Standards-aligned workflow",
        "title": "Trace each application function through ITU-T Y.3172 roles.",
        "description": "Inspect how intent, preprocessing, model, policy, distribution, sink, orchestration, sandbox, and underlay functions align.",
        "alt": "ITU-T Y.3172 aligned application pipeline",
    },
    "MRI → Point Cloud": {
        "image": MRI_POINTCLOUD_IMAGE_PATH,
        "eyebrow": "Interactive imaging workspace",
        "title": "Move from brain-only MRI to an anatomical point cloud.",
        "description": "Inspect registered MRI slices and an 8,192-point representation labelled as hippocampus, ventricles, cortical area, and other brain tissue.",
        "alt": "Brain MRI transforming into an anatomical point cloud",
    },
    "Policy Alignment": {
        "image": POLICY_IMAGE_PATH,
        "eyebrow": "Saudi public-domain evidence",
        "title": "Translate policy and digital-health sources into research actions.",
        "description": "Review official government sources separately from public background and research evidence, with direct links and bounded claims.",
        "alt": "Saudi policy alignment and evidence illustration",
    },
    "Evidence Library": {
        "image": KNOWLEDGE_IMAGE_PATH,
        "eyebrow": "Characterized evidence library",
        "title": "Search the records that ground the NeuroAPS workspace.",
        "description": "Explore papers, neuroanatomy context, Eastern Province studies, and Saudi policy evidence with source-visible records.",
        "alt": "Evidence library and retrieval workflow illustration",
    },
    "Research Assistant": {
        "image": ASSISTANT_IMAGE_PATH,
        "eyebrow": "Grounded research conversation",
        "title": "Ask the NeuroAPS Evidence Copilot.",
        "description": "Use an LLM-style research chat while keeping every answer bounded to retrieved records and exposing its supporting chunks.",
        "alt": "NeuroAPS evidence copilot interface",
    },
    "Deployment": {
        "image": DEPLOYMENT_IMAGE_PATH,
        "eyebrow": "Controlled integration workbench",
        "title": "Prepare the model bundle for a governed next phase.",
        "description": "Check model, preprocessing, class-map, sample, and result artifacts against the interface prepared for future runtime integration.",
        "alt": "NeuroAPS deployment integration workbench",
    },
}


def image_data_uri(path: Path) -> str:
    """Return one packaged image as an embeddable data URI."""

    media_type = "image/svg+xml" if path.suffix.lower() == ".svg" else "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{media_type};base64,{encoded}"


st.set_page_config(
    page_title="NeuroAPS | AI-Ready Neuroimaging",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    :root { --navy:#081D33; --ink:#10243A; --teal:#16A7A2; --teal-dark:#0C7478; --aqua:#65E3D7;
            --green:#0B7A5C; --red:#C8405B; --gold:#D7952B; --line:#DDE6EC; --paper:#F5F8FA; }
    html, body, [class*="css"] {font-family:Inter,Segoe UI,Arial,sans-serif;}
    html {scroll-behavior:smooth;}
    .stApp {background:var(--paper);}
    .block-container {padding-top:.72rem;padding-bottom:0;max-width:1480px;}
    header[data-testid="stHeader"] {background:transparent;}
    [data-testid="stDecoration"] {display:none;}
    [data-testid="stSidebar"] {border-right:1px solid var(--line);background:#F7FAFC;}
    .eyebrow {color:var(--teal);font-weight:800;letter-spacing:.09em;font-size:.74rem;}
    .subtle {color:#536A78;font-size:.95rem;margin:.15rem 0 .65rem;}
    .guardrail {padding:.8rem 1rem;border-left:5px solid #C43B51;background:#FFF2F4;border-radius:8px;}
    .status-chip {display:inline-block;padding:.24rem .68rem;border-radius:999px;background:#E7F4F1;
                  color:#09644D;font-size:.76rem;font-weight:750;margin:.15rem .28rem .05rem 0;}
    .source-card {border:1px solid #DCE4EC;border-radius:12px;padding:.8rem 1rem;background:white;margin:.4rem 0;}
    .smallcaps {font-size:.72rem;letter-spacing:.07em;text-transform:uppercase;color:#657788;font-weight:700;}
    div[data-testid="stMetric"] {background:#FFFFFF;border:1px solid var(--line);padding:.82rem 1rem;border-radius:14px;
                                  box-shadow:0 4px 14px rgba(16,36,58,.035);}
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        position:sticky;top:.45rem;z-index:998;gap:.16rem;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:thin;
        margin:0 0 .8rem;padding:.52rem .62rem;border:1px solid #DCE6EB;border-radius:16px;
        background:rgba(255,255,255,.96);box-shadow:0 12px 28px rgba(8,29,51,.09);
        backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
    }
    div[data-testid="stTabs"] button[data-baseweb="tab"] {
        position:relative;height:auto;min-height:42px;padding:.58rem .78rem;border:0;border-radius:10px;
        background:transparent;color:#19384B;font-size:.79rem;font-weight:750;white-space:nowrap;
        transition:background-color .18s ease,color .18s ease,border-color .18s ease,
                   box-shadow .18s ease,transform .18s ease;
    }
    div[data-testid="stTabs"] button[data-baseweb="tab"] p {color:inherit!important;}
    div[data-testid="stTabs"] button[data-baseweb="tab"]:hover {
        background:#E7F4F2;color:#087167;box-shadow:none;transform:translateY(-1px);
    }
    div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {
        background:#F2FAF9;color:#087167;box-shadow:inset 0 -3px 0 var(--teal);
    }
    div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"]:hover {
        background:#E7F4F2;color:#075E55;
    }
    div[data-testid="stTabs"] button[data-baseweb="tab"]:focus-visible {
        outline:3px solid rgba(22,124,134,.25);outline-offset:2px;
    }
    div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {display:none;}
    div[data-testid="stTabs"] [data-baseweb="tab-border"] {display:none;}
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

    /* Evidence Copilot workspace. */
    .assistant-shell {padding:1rem;border:1px solid #DCE7EB;border-radius:22px;background:linear-gradient(145deg,#FFFFFF,#F2F8F8);
                      box-shadow:0 14px 32px rgba(8,29,51,.07);}
    .bot-profile {overflow:hidden;border:1px solid rgba(101,227,215,.22);border-radius:22px;background:
                  radial-gradient(circle at 85% 5%,rgba(101,227,215,.18),transparent 31%),linear-gradient(145deg,#071A2E,#0A3C50);
                  color:#FFF;padding:1.25rem;box-shadow:0 14px 32px rgba(8,29,51,.14);}
    .bot-identity {display:flex;align-items:center;gap:.8rem;margin-bottom:1rem;}
    .bot-avatar {position:relative;display:grid;place-items:center;width:58px;height:58px;border-radius:19px;
                 background:linear-gradient(145deg,var(--aqua),var(--teal));color:var(--navy);font-size:1.24rem;font-weight:950;
                 box-shadow:0 10px 24px rgba(22,167,162,.28);}
    .bot-avatar::after {content:"";position:absolute;right:-2px;bottom:-2px;width:13px;height:13px;border:3px solid #0A2F43;
                       border-radius:50%;background:#43D6A4;}
    .bot-identity h3 {margin:0;color:#FFF;font-size:1.03rem;}
    .bot-identity p {margin:.22rem 0 0;color:#A9C4CF;font-size:.72rem;}
    .bot-mode {display:flex;align-items:center;gap:.45rem;padding:.62rem .72rem;border:1px solid rgba(101,227,215,.19);
               border-radius:13px;background:rgba(101,227,215,.08);color:#BFF6F0;font-size:.73rem;font-weight:800;}
    .bot-mode-dot {width:8px;height:8px;border-radius:50%;background:#43D6A4;box-shadow:0 0 0 5px rgba(67,214,164,.10);}
    .bot-stats {display:grid;grid-template-columns:1fr 1fr;gap:.55rem;margin:.85rem 0;}
    .bot-stat {padding:.72rem;border-radius:13px;background:rgba(255,255,255,.07);}
    .bot-stat strong {display:block;color:#FFF;font-size:1.08rem;}
    .bot-stat span {display:block;margin-top:.16rem;color:#9DB6C2;font-size:.66rem;}
    .bot-boundary {margin:0;color:#A9C4CF;font-size:.7rem;line-height:1.5;}
    .assistant-chat-head {display:flex;align-items:center;justify-content:space-between;gap:1rem;margin-bottom:.7rem;padding:.85rem 1rem;
                         border:1px solid #DCE7EB;border-radius:16px;background:#FFF;}
    .assistant-chat-title {display:flex;align-items:center;gap:.65rem;}
    .assistant-mini-avatar {display:grid;place-items:center;width:39px;height:39px;border-radius:12px;background:#DDF8F4;
                            color:var(--teal-dark);font-size:.86rem;font-weight:950;}
    .assistant-chat-title strong {display:block;color:var(--ink);font-size:.9rem;}
    .assistant-chat-title span {display:block;margin-top:.16rem;color:#71848F;font-size:.67rem;}
    .assistant-secure {padding:.35rem .55rem;border-radius:999px;background:#E7F4F1;color:#09644D;font-size:.64rem;font-weight:850;white-space:nowrap;}
    .assistant-prompt-label {margin:.2rem 0 .5rem;color:#536A78;font-size:.72rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase;}
    div.st-key-assistant_chat [data-testid="stChatMessage"] {margin:.55rem 0;padding:.82rem .9rem;border:1px solid #DCE7EB;
                                                               border-radius:17px;background:#FFF;box-shadow:0 5px 14px rgba(8,29,51,.035);}
    div.st-key-assistant_chat [data-testid="stChatInput"] {border:1px solid #BBDDD7;border-radius:18px;background:#FFF;
                                                             box-shadow:0 8px 22px rgba(8,29,51,.07);}
    div.st-key-assistant_chat [data-testid="stButton"] button {min-height:58px;text-align:left;border-color:#D5E5E8;background:#F7FAFB;}
    div.st-key-assistant_chat [data-testid="stButton"] button:hover {border-color:#9FD4CA;background:#E9F7F4;color:#075E55;}

    /* Compact application identity and workspace header. */
    .application-head {display:flex;align-items:center;justify-content:space-between;gap:1rem;margin:0 0 .65rem;padding:.25rem .25rem .45rem;}
    .application-brand {display:flex;align-items:center;gap:.72rem;}
    .application-brand-copy {display:flex;flex-direction:column;line-height:1.08;}
    .application-brand-copy strong {color:var(--navy);font-size:1.02rem;letter-spacing:.01em;}
    .application-brand-copy span {margin-top:.2rem;color:#708692;font-size:.64rem;letter-spacing:.08em;text-transform:uppercase;}
    .application-state {display:flex;align-items:center;gap:.45rem;padding:.5rem .7rem;border:1px solid #CDE6E1;border-radius:999px;
                        background:#EFF9F7;color:#0A6A54;font-size:.69rem;font-weight:800;white-space:nowrap;}
    .application-state-dot {width:8px;height:8px;border-radius:50%;background:#25B786;box-shadow:0 0 0 5px rgba(37,183,134,.10);}

    /* Website shell inspired by modern clinical-intelligence product sites. */
    .brand-mark {display:grid;place-items:center;width:42px;height:42px;border-radius:13px;
                 background:linear-gradient(145deg,var(--aqua),var(--teal));color:var(--navy);font-size:1.12rem;font-weight:900;
                 box-shadow:0 7px 18px rgba(22,167,162,.32);}

    .hero-web {position:relative;overflow:hidden;display:grid;grid-template-columns:1.05fr .95fr;align-items:center;gap:2rem;
               min-height:430px;margin:.15rem 0 1rem;padding:2.75rem 3rem;border-radius:24px;background:
               radial-gradient(circle at 78% 24%,rgba(101,227,215,.23),transparent 26%),
               radial-gradient(circle at 18% 92%,rgba(25,111,151,.31),transparent 30%),
               linear-gradient(135deg,#061528 0%,#0B3450 50%,#0C7478 100%);
               box-shadow:0 24px 55px rgba(8,29,51,.20);isolation:isolate;}
    .hero-web::before,.hero-web::after {content:"";position:absolute;border-radius:50%;border:1px solid rgba(101,227,215,.15);z-index:-1;}
    .hero-web::before {width:520px;height:520px;right:-180px;top:-210px;box-shadow:0 0 0 85px rgba(101,227,215,.035);}
    .hero-web::after {width:360px;height:360px;left:-200px;bottom:-210px;box-shadow:0 0 0 70px rgba(101,227,215,.03);}
    .hero-kicker {display:inline-flex;align-items:center;gap:.48rem;margin-bottom:1.05rem;padding:.42rem .66rem;border-radius:999px;
                  border:1px solid rgba(101,227,215,.28);background:rgba(101,227,215,.09);color:#A8F2EA;
                  font-size:.69rem;font-weight:800;letter-spacing:.11em;text-transform:uppercase;}
    .pulse-dot {width:7px;height:7px;border-radius:50%;background:var(--aqua);box-shadow:0 0 0 5px rgba(101,227,215,.12);}
    .hero-web h1 {max-width:720px;margin:0;color:#FFF;font-size:clamp(2.25rem,4.3vw,3.85rem);line-height:1.01;letter-spacing:-.05em;font-weight:850;}
    .hero-web h1 span {color:var(--aqua);}
    .hero-lead {max-width:660px;margin:1.25rem 0 1.55rem;color:#C6D9E2;font-size:1.04rem;line-height:1.65;}
    .hero-trust {display:flex;gap:.95rem;flex-wrap:wrap;color:#9DB6C2;font-size:.72rem;}
    .hero-trust span::before {content:"✓";color:var(--aqua);font-weight:900;margin-right:.35rem;}
    .hero-visual {position:relative;min-width:0;}
    .visual-frame {position:relative;overflow:hidden;padding:.62rem;border:1px solid rgba(255,255,255,.19);border-radius:24px;
                   background:rgba(255,255,255,.09);box-shadow:0 24px 54px rgba(1,13,25,.36);transform:rotate(1.2deg);}
    .visual-frame img {display:block;width:100%;aspect-ratio:16/9;object-fit:contain;border-radius:18px;background:#071B2E;}
    .visual-badge {position:absolute;display:flex;align-items:center;gap:.55rem;padding:.68rem .82rem;border-radius:14px;
                   background:rgba(255,255,255,.94);box-shadow:0 14px 30px rgba(3,19,33,.25);color:var(--ink);font-size:.72rem;font-weight:750;}
    .visual-badge strong {display:block;font-size:.94rem;line-height:1.05;color:var(--teal-dark);}
    .badge-one {left:-1.2rem;top:1.5rem;}
    .badge-two {right:-.9rem;bottom:1.5rem;}
    .badge-icon {display:grid;place-items:center;width:33px;height:33px;border-radius:10px;background:#DDF8F4;color:var(--teal-dark);font-size:1rem;}

    .site-footer {margin:2rem -1rem 0;padding:2rem 2.2rem;border-radius:24px 24px 0 0;background:#081D33;color:#B8CDD5;}
    .footer-grid {display:flex;align-items:center;justify-content:space-between;gap:1.5rem;flex-wrap:wrap;}
    .footer-brand {display:flex;align-items:center;gap:.7rem;}
    .footer-brand strong {color:#FFF;font-size:.92rem;}
    .footer-brand span {font-size:.68rem;}
    .footer-note {max-width:640px;text-align:right;font-size:.68rem;line-height:1.5;}

    @media (max-width:1100px) {
      .hero-web {grid-template-columns:1fr;padding:3.2rem;}
      .hero-visual {max-width:760px;}
      .bot-stats {grid-template-columns:1fr 1fr;}
    }
    @media (max-width:700px) {
      .block-container {padding-left:.65rem;padding-right:.65rem;}
      .application-head {align-items:flex-start;}
      .application-state {display:none;}
      div[data-testid="stTabs"] [data-baseweb="tab-list"] {top:.2rem;border-radius:13px;padding:.4rem;}
      .hero-web {min-height:auto;padding:2.2rem 1.35rem;border-radius:21px;}
      .hero-web h1 {font-size:2.65rem;}
      .hero-visual {margin-top:.25rem;}
      .visual-badge {display:none;}
      .assistant-chat-head {align-items:flex-start;}
      .assistant-secure {display:none;}
      .footer-note {text-align:left;}
    }
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

requested_workspace = st.query_params.get("workspace")
if requested_workspace not in WORKSPACE_NAMES:
    requested_workspace = "Context & Impact"
if st.session_state.get("_workspace_query") != requested_workspace:
    st.session_state.workspace_tabs = requested_workspace
    st.session_state._workspace_query = requested_workspace
def sync_workspace_query() -> None:
    """Keep the active workspace menu and URL synchronized."""

    selected = st.session_state.workspace_tabs
    st.query_params["workspace"] = selected
    st.session_state._workspace_query = selected


def render_workspace_hero(workspace_name: str) -> None:
    """Render the distinct professional header for one workspace."""

    visual = WORKSPACE_VISUALS[workspace_name]
    visual_uri = image_data_uri(visual["image"])
    st.markdown(
        f"""
        <section class="hero-web" aria-label="{workspace_name} workspace introduction">
          <div class="hero-copy">
            <div class="hero-kicker"><span class="pulse-dot"></span>{visual['eyebrow']}</div>
            <h1>{visual['title']}</h1>
            <p class="hero-lead">{visual['description']}</p>
            <div class="hero-trust">
              <span>Offline evidence retrieval</span>
              <span>Human review retained</span>
              <span>Research use only</span>
            </div>
          </div>
          <div class="hero-visual">
            <div class="visual-frame"><img src="{visual_uri}" alt="{visual['alt']}"></div>
            <div class="visual-badge badge-one"><span class="badge-icon">⌁</span><span><strong>Focused module</strong>{workspace_name}</span></div>
            <div class="visual-badge badge-two"><span class="badge-icon">◎</span><span><strong>{len(records)} records</strong>grounded evidence</span></div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


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
    <header class="application-head" aria-label="NeuroAPS application identity">
      <div class="application-brand">
        <span class="brand-mark">N</span>
        <span class="application-brand-copy">
          <strong>NeuroAPS Clinical Research Workspace</strong>
          <span>AI-ready neuroimaging research demonstrator</span>
        </span>
      </div>
      <span class="application-state"><span class="application-state-dot"></span>Evidence workspace ready</span>
    </header>
    """,
    unsafe_allow_html=True,
)

tabs = st.tabs(
    WORKSPACE_NAMES,
    default=requested_workspace,
    key="workspace_tabs",
    on_change=sync_workspace_query,
)


with tabs[0]:
    render_workspace_hero("Context & Impact")
    st.markdown(
        """
        <div class="context-card">
          <div class="smallcaps">Application story</div>
          <h3>From fragmented imaging to a research-ready workflow</h3>
          <p>The workspace connects brain-only MRI viewing, an anatomical point cloud, readiness evidence, Saudi public sources, and human review in one interface.</p>
          <p>NeuroCloud AI is the supplied hackathon platform concept; NeuroAPS is the research workflow demonstrated in this build. It does not claim clinical deployment, regulatory approval, or a hospital partnership.</p>
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
    render_workspace_hero("Readiness")
    st.subheader("Application readiness")
    st.caption("Coverage combines the two published studies with functions implemented in this demonstrator.")
    chart_left, chart_column, chart_right = st.columns([0.18, 0.64, 0.18])
    with chart_column:
        st.plotly_chart(readiness_radar(), width="stretch", config={"displayModeBar": False})

    for factor in FACTORS:
        with st.expander(f"{factor['name']} — {SCORE_LABEL[factor['score']]}"):
            st.markdown(f"**Coverage:** {factor['coverage']}")
            st.markdown(f"**Evidence:** {factor['evidence']}")
            if factor.get("source_url"):
                st.link_button(factor["source_label"], factor["source_url"], width="stretch")

    st.divider()
    st.subheader("Why the proposed representation fits constrained clinical settings")
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
    render_workspace_hero("Y.3172 Workflow")
    st.subheader("ITU-T Y.3172-aligned workflow")
    st.caption("Every node is mapped to a concrete function, current evidence, and application state.")
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
    render_workspace_hero("MRI → Point Cloud")
    st.subheader("Brain MRI → anatomically labelled point cloud")
    st.caption("Select a subject, inspect the brain-only MRI, and explore the corresponding lightweight point-cloud representation.")

    if sample_registry_error:
        st.info(
            "The public GitHub edition does not distribute the controlled MRI, mask, or point-cloud files. "
            "The complete imaging workspace activates automatically when the authorized files are placed in "
            "their registered local folders."
        )
        preview_path = BASE / "docs" / "reference" / "mri_viewer.png"
        if preview_path.is_file():
            st.image(preview_path, caption="Reference view from the verified local research release", width="stretch")
        st.markdown(
            """
            **Authorized local-data setup**

            1. Obtain the data through the applicable ADNI/data-use process.
            2. Place raw MRI files in `data/samples/raw_mri/`, masks in `data/samples/nifti/`, and PLY files in `data/samples/point_clouds/`.
            3. Preserve the filenames and metadata registered in `data/samples/sample_manifest.json`.
            4. Restart the application; file size and checksum validation will run before viewing.

            [Open the official ADNI Data and Samples page](https://adni.loni.usc.edu/data-samples/)
            """
        )
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
    render_workspace_hero("Policy Alignment")
    st.subheader("Saudi policy and digital-health alignment")
    st.caption("Claims are bounded to the linked sources. ADNI, HSTP, MOH statistics, Seha Virtual Hospital, PDPL, and AI-ethics statements were cross-checked on 29 August 2026.")

    st.plotly_chart(policy_heatmap(), width="stretch", config={"displayModeBar": False})

    st.markdown("#### Validated public evidence")
    for row_start in (0, 2):
        source_columns = st.columns(2, gap="medium")
        for column, source in zip(source_columns, POLICY_SOURCES[row_start:row_start + 2]):
            source_links = " · ".join(
                f'<a href="{link["url"]}" target="_blank">{link["label"]} ↗</a>'
                for link in source["links"]
            )
            column.markdown(
                f"""
                <div class="policy-card">
                  <div class="verified">Official source checked · {source['checked']}</div>
                  <h4>{source['source']}</h4>
                  <p><b>{source['authority']}</b> · {source['supports']}</p>
                  <p><b>Application translation:</b> {source['application']}</p>
                  <p><b>Boundary:</b> {source['boundary']}</p>
                  <p>{source_links}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.info(
        "**Prevention claim:** HSTP explicitly prioritizes disease prevention. NeuroAPS may be described as "
        "a prevention-aligned early-screening research concept, but the phrase ‘from treatment-based care "
        "towards prevention and early intervention’ is not presented as a direct HSTP quotation or as proof "
        "of an adopted Alzheimer screening program."
    )

    st.markdown("#### PDPL and AI-ethics control cross-check")
    pdpl_frame = pd.DataFrame(
        PDPL_AI_ETHICS_CONTROLS,
        columns=["Control", "What this application requires", "Current state"],
    )
    st.dataframe(pdpl_frame, hide_index=True, width="stretch", height=310)
    st.caption(
        "The controls translate the PDPL implementing regulations and SDAIA AI Ethics Self-Assessment into "
        "design requirements. They are not a certification or legal opinion."
    )

    with st.expander("Governance stress-test: disclosure, profiling, and escalation"):
        st.caption("Synthetic evaluation scenario — not a report of an actual incident.")
        for number, title, description in GOVERNANCE_SCENARIO:
            st.markdown(f"**{number}. {title}** — {description}")

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
        "Government pages and reports are marked as official. ADNI is identified separately as an official "
        "research dataset with controlled access. Background and peer-reviewed research are not presented as law."
    )

    st.markdown("#### Application actions")
    action_frame = pd.DataFrame([
        ("HSTP", "Access, disease prevention, quality, and digital transformation", "Prevention-aligned research screening and specialist decision support; not an adopted national AD screening service", "Mapped with boundary"),
        ("NSDAI", "Data and AI for healthcare access and preventive care", "Traceable evidence, governed model context, and research collaboration", "Mapped"),
        ("Seha Virtual Hospital", "Remote specialist care, teleradiology, sandbox, clinical research", "Candidate pathway for controlled evaluation", "Evidence-based pathway"),
        ("PDPL / AI Ethics", "Sensitive health-data safeguards, DPIA triggers, purpose limitation, ethical assessment", "Lawful basis, minimum data, access control, auditability, human confirmation, and no unrelated profiling", "Designed; formal review pending"),
    ], columns=["Source", "Public-policy support", "Application action", "Coverage"])
    st.dataframe(action_frame, hide_index=True, width="stretch")
    st.caption("Alignment does not imply regulatory approval, legal compliance certification, hospital integration, or partnership.")


with tabs[5]:
    render_workspace_hero("Evidence Library")
    st.subheader("Evidence library")
    st.caption("Search the papers, neuroanatomy background, Eastern Province studies, and Saudi policy sources.")
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
    render_workspace_hero("Research Assistant")
    mode = "External synthesis over public excerpts" if use_external_llm else "Offline retrieval evidence"
    st.subheader("Research Assistant")
    st.caption(
        "A focused LLM-style interface over structured evidence records—not raw text. "
        "Every answer remains bounded to the packaged knowledge base and exposes its retrieved evidence."
    )

    with st.expander("Knowledge base scope and reference links"):
        st.write(
            f"The assistant searches {len(records)} characterized records across {len(kb.chunks)} offline "
            f"TF-IDF chunks. A separate {len(PUBLIC_DOMAIN_SOURCES)}-entry Saudi source register supports "
            "the Policy Alignment workspace."
        )
        assistant_reference_frame = pd.DataFrame([
            {
                "Record": record["title"],
                "Type": record["type"].replace("_", " ").title(),
                "Status": record["status"],
                "Reference": record.get("reference_link"),
            }
            for record in records
        ])
        st.dataframe(
            assistant_reference_frame,
            hide_index=True,
            width="stretch",
            column_config={
                "Reference": st.column_config.LinkColumn("Reference", display_text="Open source ↗"),
            },
        )

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "pending_question" not in st.session_state:
        st.session_state.pending_question = None

    assistant_control_column, assistant_chat_column = st.columns([0.30, 0.70], gap="large")
    with assistant_control_column:
        st.markdown(
            f"""
            <div class="bot-profile">
              <div class="bot-identity">
                <span class="bot-avatar">N</span>
                <span><h3>Evidence Copilot</h3><p>NeuroAPS research assistant</p></span>
              </div>
              <div class="bot-mode"><span class="bot-mode-dot"></span>{mode}</div>
              <div class="bot-stats">
                <div class="bot-stat"><strong>{len(records)}</strong><span>characterized records</span></div>
                <div class="bot-stat"><strong>{len(kb.chunks)}</strong><span>retrieval chunks</span></div>
                <div class="bot-stat"><strong>{len(PUBLIC_DOMAIN_SOURCES)}</strong><span>Saudi source entries</span></div>
                <div class="bot-stat"><strong>TF-IDF</strong><span>offline retrieval</span></div>
              </div>
              <p class="bot-boundary">Each record carries type, status, domain, country scope, mapped readiness fields, metrics, and public links where available. The copilot exposes supporting titles, chunk IDs, similarity scores, and citations. It does not diagnose or replace clinician review.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("#### Active evidence")
        selected_chat_types = st.multiselect(
            "Limit retrieval by source type",
            kb.record_types,
            default=[],
            key="chat_types",
            placeholder="All record types",
        )
        st.caption("Leave empty to search every characterized record.")
        if st.button("Clear conversation", width="stretch", key="clear_assistant_chat"):
            st.session_state.chat_messages = []
            st.session_state.pending_question = None
            st.rerun()
        with st.expander("How the copilot answers"):
            st.markdown(
                "1. Retrieves the most relevant evidence chunks.\n"
                "2. Builds an answer from those chunks.\n"
                "3. Shows titles, chunk IDs, similarity scores, and public links."
            )

    with assistant_chat_column:
        with st.container(key="assistant_chat"):
            st.markdown(
                f"""
                <div class="assistant-chat-head">
                  <div class="assistant-chat-title">
                    <span class="assistant-mini-avatar">N</span>
                    <span><strong>NeuroAPS Evidence Copilot</strong><span>{mode} · ready for a research question</span></span>
                  </div>
                  <span class="assistant-secure">● GROUNDED MODE</span>
                </div>
                <div class="assistant-prompt-label">Suggested questions</div>
                """,
                unsafe_allow_html=True,
            )

            suggestions = [
                "What evidence supports deployment efficiency?",
                "What changes in the hippocampus, ventricles, and cortex in AD?",
                "What is the strongest Dammam-specific precedent?",
                "How does the application align with Saudi health and AI policy?",
            ]
            for row_start in (0, 2):
                suggestion_columns = st.columns(2, gap="small")
                for index, (column, suggestion) in enumerate(
                    zip(suggestion_columns, suggestions[row_start:row_start + 2]),
                    start=row_start,
                ):
                    if column.button(suggestion, width="stretch", key=f"suggestion_{index}"):
                        st.session_state.pending_question = suggestion

            if not st.session_state.chat_messages:
                with st.chat_message("assistant"):
                    st.markdown(
                        "Hello — I’m the **NeuroAPS Evidence Copilot**. Ask me about readiness, MRI anatomy, "
                        "Eastern Province evidence, Saudi policy alignment, or the Y.3172 workflow. "
                        "I’ll show the retrieved sources with every answer."
                    )

            for message in st.session_state.chat_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                    if message.get("hits"):
                        with st.expander("Retrieved evidence and citations"):
                            for number, hit in enumerate(message["hits"], start=1):
                                link = f" · [public link]({hit['reference_link']})" if hit.get("reference_link") else ""
                                st.markdown(
                                    f"**[{number}] {hit['title']}** · chunk {hit['chunk_id']} · "
                                    f"similarity {hit['score']:.3f}{link}"
                                )
                                st.caption(hit["text"][:500] + ("..." if len(hit["text"]) > 500 else ""))

            typed_question = st.chat_input(
                "Ask NeuroAPS about evidence, anatomy, readiness, policy, or deployment...",
                key="neuroaps_research_question",
            )
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
    render_workspace_hero("Deployment")
    st.subheader("Deployment workbench")
    status_frame = pd.DataFrame([
        ("Phase 1", "Interactive synthetic web prototype", "Preserved in legacy_phase1", "Complete"),
        ("Phase 2A", "Characterized evidence library and offline retrieval", "10 curated records / 46 chunks", "Complete"),
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
    st.warning(
        "Research demonstrator boundary: live model weights are not integrated, the 10 registered examples are "
        "not a Saudi validation cohort, and no clinical, legal, security, privacy, or institutional approval is claimed."
    )

    with st.expander("Hackathon application storyboard"):
        if HACKATHON_BOARD_IMAGE_PATH.exists():
            st.image(str(HACKATHON_BOARD_IMAGE_PATH), width="stretch")
        st.caption("Concept storyboard supplied for the project; implementation status is defined by the table above.")


st.markdown(
    """
    <footer class="site-footer">
      <div class="footer-grid">
        <div class="footer-brand">
          <span class="brand-mark">N</span>
          <span><strong>NeuroAPS Clinical Research Workspace</strong><br>AI-ready neuroimaging research demonstrator</span>
        </div>
        <div class="footer-note">For research use only · Not a clinical diagnosis · Performance and policy statements are bounded to the evidence presented inside this application.</div>
      </div>
    </footer>
    """,
    unsafe_allow_html=True,
)

# NeuroAPS Clinical Research Workspace

A professional Streamlit application for AI-readiness evaluation, MRI-to-point-cloud exploration, ITU-T Y.3172 workflow mapping, Saudi policy alignment, and citation-grounded research support.

The verified local research release supports 10 registered subject examples (AD1–AD10), each with a raw T1 MRI, registered brain mask, and 8,192-point PLY representation. The public repository intentionally excludes those controlled imaging artifacts; authorized users can restore them locally through the registered folder structure.

**Public repository:** https://github.com/mjrjahid/NeuroAPS

## Application experience

Release 7.4 retains the horizontal workspace menu and adds the expanded structured knowledge base requested for the Research Assistant:

- a clean top workspace menu matching the supplied navigation reference;
- active-menu underline, hover background, keyboard focus, and mobile horizontal scrolling;
- a compact NeuroAPS application identity and evidence-ready status;
- a topic-specific hero visual for each of the eight workspaces;
- an LLM-style Evidence Copilot with suggested prompts and citation-visible retrieval;
- direct access to every focused research module; and
- a professional research-boundary footer.

The updated Policy Alignment workspace includes direct official links for ADNI data access, Saudi MOH statistics, HSTP, PDPL Implementing Regulations, and SDAIA's AI Ethics Self-Assessment. It also separates verified public-policy support from application interpretation.

The separate floating website navigation and long intermediate landing sections were removed. The application now opens directly into the selected workspace while retaining the NeuroAPS navy, teal, and cyan identity.

## Main workspaces

- **Context & Impact:** supplied ITU Hackathon visuals covering the platform vision, fragmented neuroimaging, manual analysis, root causes, and Saudi impact context.
- **Readiness:** six vertically stacked coverage factors, all 13 readiness dimensions, a six-step human-review scenario, and published deployment comparisons.
- **Y.3172 Workflow:** aligned ML Intent, SRC, C, PP, M, P, D, SINK, MLFO, Sandbox, and Underlay roles.
- **MRI → Point Cloud:** brain-only axial/coronal/sagittal MRI viewing and an interactive anatomical point cloud.
- **Policy Alignment:** verified HSTP, NSDAI, Seha Virtual Hospital, PDPL, data-governance, and AI-ethics sources.
- **Evidence Library:** 10 characterized research, clinical, regional, and policy records indexed into 46 offline retrieval chunks.
- **Research Assistant:** a polished LLM-style Evidence Copilot with offline citation-visible retrieval, suggested prompts, evidence filters, and optional public-evidence synthesis.
- **Deployment:** current implementation and the prepared model-integration interface.

The sidebar keeps offline retrieval, imaging, and external-LLM status inside a compact **Evidence mode** pop-up.

The eight menu options remain visible at the top on desktop and scroll horizontally on smaller screens. The active workspace is stored in the URL and synchronized with the menu. Each workspace receives a different topic-specific hero image. The Evidence mode panel remains available from the collapsed sidebar.

## Published deployment evidence

NeuroAPS-Net is reported at 8,192 points with:

- accuracy: **84.85%**
- inference latency: **1.48 ms**
- peak GPU memory: **234.6 MB**
- hardware: **one NVIDIA RTX 3060**

The application compares these measurements with the supplied PointNet, PointCNN, and DGCNN results. Dense 3D-CNN constraints are described qualitatively because the supplied evidence does not contain a harmonized voxel-CNN benchmark.

## Anatomical point-cloud labels

| PLY label | Region |
|---:|---|
| 1 | Hippocampus |
| 3 | Ventricles |
| 5 | Cortical area |
| 7 | Other brain tissue |

The registered MRI view uses the supplied mask to show the brain portion only. The mask is not displayed as a code-distribution panel.

## Run on Windows

1. Extract the complete ZIP to a normal folder, for example C:\NeuroAPS.
2. Double-click start_windows.bat.
3. Keep the command window open during first-time dependency installation.
4. Open http://localhost:8501 if the browser does not open automatically.

The launcher checks normal Python 3.10–3.13 locations, including:

~~~text
C:\Users\F M Jahiduzzaman\AppData\Local\Programs\Python\Python312\python.exe
~~~

It does not depend on Python being available in PATH and does not require manual virtual-environment activation.

## Run on macOS or Linux

~~~bash
chmod +x start_mac_linux.sh
./start_mac_linux.sh
~~~

## Manual run

~~~bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

python -m pip install -r requirements.txt
python ingest.py
python -m streamlit run app.py
~~~

## Authorized imaging-data setup

Raw MRI, mask, and PLY files are deliberately ignored by Git and are not redistributed through this public repository. Obtain data through the applicable ADNI/data-use process, then preserve the registered filenames under:

```text
data/samples/raw_mri/
data/samples/nifti/
data/samples/point_clouds/
```

`data/samples/sample_manifest.json` retains the expected metadata, byte counts, and SHA-256 values. When the controlled files are absent, the public application presents a professional reference preview and setup guidance rather than a technical failure. When authorized files are present, the full MRI-to-point-cloud viewer activates after registry validation.

Official access route: [ADNI Data and Samples](https://adni.loni.usc.edu/data-samples/).

## Criteria and source validation

`docs/CRITERIA_CROSSCHECK.md` records the criterion-by-criterion audit against the supplied DOCX. `data/source_notes/saudi_policy_validation.txt` records the government, controlled-research-dataset, public-background, and public-research sources revalidated on 29 August 2026. The application includes direct links to:

- Saudi Vision 2030 Health Sector Transformation Program
- Health Sector Transformation Report 2024
- SDAIA National Strategy for Data & AI
- the official NSDAI PDF and Saudipedia overview
- Saudi MOH Seha Virtual Hospital and Innovation Empowerment Center
- Saudi MOH statistics
- SDAIA PDPL and National Data Governance Platform
- SDAIA AI Ethics Self-Assessment
- ADNI Data and Samples through the official LONI access route
- the 2025 Saudi Alzheimer’s review and regional Dammam/Eastern Province studies

The Saudi MOH statistics dashboard is used only as an official health-indicator gateway; its overview is not cited as a national Alzheimer prevalence estimate. HSTP supports disease prevention, while “from treatment-based care toward prevention and early intervention” is identified as an application-level interpretation rather than a direct HSTP quotation.

The Policy Alignment workspace clearly separates official government sources, controlled research access, supporting background, and research. PDPL/AI-ethics controls require purpose limitation, an applicable lawful basis, impact assessment where required, health-data safeguards, processing records, human confirmation, and a prohibition on unrelated profiling or advertising. The application does not claim regulatory approval, legal certification, clinical validation, hospital integration, or partnership.

## Offline and optional external modes

Offline retrieval is the default and requires no API key. It returns evidence from 10 characterized records across 46 TF-IDF retrieval chunks and exposes titles, chunk IDs, similarity scores, citations, and public links.

Optional external synthesis can be enabled with ANTHROPIC_API_KEY and ALLOW_EXTERNAL_LLM=true. Only retrieved public evidence is eligible for synthesis.

## Project structure

~~~text
app.py                            Streamlit application
src/project_data.py               Readiness, policy, labels, scenario, Y.3172
src/viewers.py                    Brain MRI and point-cloud visualization
src/knowledge_base.py             Local retrieval and evidence citations
src/sample_registry.py            Subject registry and safe path resolution
src/llm.py                        Optional public-evidence synthesis
data/knowledge_records.json       Ten characterized records
data/source_notes/                Clinical, regional, and policy validation notes
docs/CRITERIA_CROSSCHECK.md       DOCX criterion-by-criterion audit and boundaries
data/samples/sample_manifest.json Authorized local-artifact registry; raw artifacts excluded from Git
assets/                           Professional topic and supplied hackathon visuals
tests/                            Unit, registry, retrieval, and configuration tests
legacy_phase1/                    Preserved earlier static prototype
~~~

## Validation

~~~bash
python ingest.py
python -m unittest discover -s tests -v
python -m py_compile app.py ingest.py src/*.py scripts/*.py
~~~

GitHub Actions runs the source, evidence, interface, and manifest-schema tests on Python 3.10–3.12. The controlled-file checksum test runs automatically in a complete authorized local installation and is skipped only when every registered imaging artifact is intentionally absent from the public checkout.

## Hosting boundary

GitHub hosts the public source and documentation. GitHub Pages cannot execute this Python/Streamlit application. Run it locally with the supplied launcher or connect this repository to a Python-capable Streamlit hosting service. A hosted deployment must continue to exclude controlled ADNI files unless its access controls and data-use terms explicitly permit them.

## Research boundary

- For research use only; not a clinical diagnosis.
- Do not redistribute controlled ADNI data.
- Use approved access control, storage, audit, ethics, privacy, and clinical-validation processes before deployment.
- Live NeuroAPS-Net execution requires the versioned model, preprocessing configuration, and class mapping used in the published experiment.

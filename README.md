# NeuroAPS Clinical Research Workspace

A professional Streamlit application for AI-readiness evaluation, MRI-to-point-cloud exploration, ITU-T Y.3172 workflow mapping, Saudi policy alignment, and citation-grounded research support.

The package includes 10 real subject examples (AD1–AD10). Each example contains a raw T1 MRI, its registered brain mask, and an 8,192-point PLY representation.

## Main workspaces

- **Context & Impact:** supplied ITU Hackathon visuals covering the platform vision, fragmented neuroimaging, manual analysis, root causes, and Saudi impact context.
- **Readiness:** six vertically stacked coverage factors, all 13 readiness dimensions, a six-step human-review scenario, and published deployment comparisons.
- **Y.3172 Workflow:** aligned ML Intent, SRC, C, PP, M, P, D, SINK, MLFO, Sandbox, and Underlay roles.
- **MRI → Point Cloud:** brain-only axial/coronal/sagittal MRI viewing and an interactive anatomical point cloud.
- **Policy Alignment:** verified HSTP, NSDAI, Seha Virtual Hospital, PDPL, data-governance, and AI-ethics sources.
- **Evidence Library:** seven characterized research, clinical, regional, and policy records.
- **Research Assistant:** offline citation-visible retrieval, with optional public-evidence synthesis.
- **Deployment:** current implementation and the prepared model-integration interface.

The sidebar keeps offline retrieval, imaging, and external-LLM status inside a compact **Evidence mode** pop-up.

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

## Data included

~~~text
data/samples/raw_mri/       AD1.nii ... AD10.nii
data/samples/nifti/         AD1_mask4.nii.gz ... AD10_mask4.nii.gz
data/samples/point_clouds/  ADPC_BEST_AD1_mask4.ply ... ADPC_BEST_AD10_mask4.ply
~~~

data/samples/sample_manifest.json retains the registry needed by the application. The diagnostic interface intentionally omits checksum and alignment panels.

## Saudi public-domain source validation

data/source_notes/saudi_policy_validation.txt records the government, public-background, and public-research sources revalidated on 17 August 2026. The application includes direct links to:

- Saudi Vision 2030 Health Sector Transformation Program
- Health Sector Transformation Report 2024
- SDAIA National Strategy for Data & AI
- the official NSDAI PDF and Saudipedia overview
- Saudi MOH Seha Virtual Hospital and Innovation Empowerment Center
- Saudi MOH statistics
- SDAIA PDPL and National Data Governance Platform
- SDAIA AI Ethics Self-Assessment
- the 2025 Saudi Alzheimer’s review and regional Dammam/Eastern Province studies

The Policy Alignment workspace clearly separates official government sources from supporting background and research. It does not claim regulatory approval, clinical validation, hospital integration, or partnership.

## Offline and optional external modes

Offline retrieval is the default and requires no API key. It returns evidence from the seven characterized records and exposes retrieved chunks.

Optional external synthesis can be enabled with ANTHROPIC_API_KEY and ALLOW_EXTERNAL_LLM=true. Only retrieved public evidence is eligible for synthesis.

## Project structure

~~~text
app.py                            Streamlit application
src/project_data.py               Readiness, policy, labels, scenario, Y.3172
src/viewers.py                    Brain MRI and point-cloud visualization
src/knowledge_base.py             Local retrieval and evidence citations
src/sample_registry.py            Subject registry and safe path resolution
src/llm.py                        Optional public-evidence synthesis
data/knowledge_records.json       Seven characterized records
data/source_notes/                Clinical, regional, and policy validation notes
data/samples/                     Ten MRI/mask/PLY examples
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

## Research boundary

- For research use only; not a clinical diagnosis.
- Do not redistribute controlled ADNI data.
- Use approved access control, storage, audit, ethics, privacy, and clinical-validation processes before deployment.
- Live NeuroAPS-Net execution requires the versioned model, preprocessing configuration, and class mapping used in the published experiment.
# NeuroAPS

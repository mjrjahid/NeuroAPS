# NeuroLens: ADNI MRI & Point-Cloud RAG GUI

NeuroLens is an interactive Phase 1 research prototype for exploring the planned integration of ADNI MRI data, lightweight MRI-derived point clouds, subject-level features, experiment results, and a citation-grounded RAG assistant.

> **Research use only.** This prototype is not a clinical diagnostic system. Every displayed subject, measurement, prediction, metric, explanation, and citation is synthetic or explicitly marked as a mock value.

## Current prototype

The repository currently contains a self-contained static application with eight interactive workspaces:

- Experiment overview with cohort and model-performance summaries.
- Searchable subject explorer with diagnosis filters and subject-level details.
- Synchronized synthetic axial, coronal, and sagittal MRI canvases.
- Draggable and zoomable synthetic point-cloud viewer.
- Feature comparison plot and mock SHAP ranking.
- Multimodal RAG-assistant interface with structured response sections.
- Knowledge-source upload and indexing simulation.
- Production architecture and phased implementation roadmap.

The interface is responsive, keyboard accessible where practical, and supports the operating system's light or dark color preference.

## Run locally

No build step or package installation is required.

### Windows — easiest method

1. Extract the ZIP file.
2. Open the extracted project folder.
3. Double-click `start_windows.bat`.
4. If the browser does not open automatically, visit `http://localhost:8000`.

The launcher uses `py` or `python` when available. If Python is not installed, it opens `index.html` directly instead.

### macOS or Linux

From the extracted project folder, run:

```bash
chmod +x start_mac_linux.sh
./start_mac_linux.sh
```

### Manual method

From the project folder, start a local static server:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000` in a current browser.

You may also open `index.html` directly. A network connection is used only to load the optional Lucide icon library from its public CDN; the prototype remains usable without the icons.

## Repository structure

```text
.
├── index.html                    # Complete Phase 1 application
├── start_windows.bat             # One-click Windows launcher
├── start_mac_linux.sh            # macOS/Linux launcher
├── README.md                     # Scope, setup, and roadmap
└── docs/
    ├── IMPLEMENTATION_SPECIFICATION.md  # Full production-system specification
    └── USER_GUIDE.md                    # Screen-by-screen operating guide
```

## What is implemented versus simulated

| Area | Phase 1 status | Production integration planned |
|---|---|---|
| MRI viewer | Synthetic canvas slices and controls | NiiVue with NIfTI and optional DICOM support |
| Point cloud | Synthetic interactive canvas | Three.js with PLY, PCD, XYZ, NPZ, or CSV adapters |
| Subjects/features | Synthetic records | Validated CSV/Excel import into PostgreSQL |
| Inference | Mock predictions | Existing model and preprocessing artifacts |
| RAG | Grounded-response interface and demo sources | Structured retrieval, document RAG, and compatible similar-case vectors |
| Knowledge base | Local upload/indexing simulation | Ingestion service, checksums, metadata, pgvector, and source inspection |
| Security | Visible research-use boundary | Authentication, roles, audit logs, upload validation, and controlled storage |

## Planned production architecture

- **Frontend:** React or Next.js, TypeScript, Tailwind CSS, shadcn/ui, NiiVue, Three.js, and Plotly/ECharts.
- **Backend:** FastAPI with typed ingestion, retrieval, inference, explanation, and file services.
- **Data layer:** PostgreSQL for structured research data, pgvector for embeddings, and object storage for large imaging/model artifacts.
- **Retrieval:** Separate structured retrieval, document RAG, and similar-case retrieval paths. Raw MRI or point clouds will not be searched with text embeddings.
- **Inference boundary:** Numerical predictions must be produced by the supplied trained model using the original feature order, preprocessing, class mapping, and validation rules—not by the LLM.

## Integration roadmap

1. **Phase 1 — Prototype:** navigation, synthetic visualizations, viewers, chatbot UI, knowledge-base UI, and architecture view.
2. **Phase 2 — Data:** import feature/result tables, link MRI and point-cloud files, and validate identifiers and schemas.
3. **Phase 3 — Model:** integrate trained-model and preprocessing artifacts and reproduce saved predictions.
4. **Phase 4 — RAG:** ingest experiment documents and implement metadata-filtered hybrid retrieval with inspectable citations.
5. **Phase 5 — Deployment:** add authentication, authorization, audit logs, tests, containerization, and performance optimization.

## Inputs needed for Phase 2

- One representative MRI file and its format information.
- One representative point-cloud file and its coordinate/channel definition.
- The complete feature table with names, units, and subject/visit identifiers.
- Trained model plus preprocessing artifacts and class mapping.
- Saved prediction and experiment-metric tables.
- Research documents and data dictionaries intended for the knowledge base.

Do not commit restricted ADNI files, secrets, credentials, identifiable records, or proprietary model artifacts to this public repository.

## Browser support

Use a current version of Chrome, Edge, Firefox, or Safari. Canvas rendering, CSS custom properties, and `color-mix()` support are required for the intended appearance.

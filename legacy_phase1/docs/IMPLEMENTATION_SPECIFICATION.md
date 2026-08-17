Act as a senior full-stack AI engineer, medical-imaging software developer, ML engineer, database architect, and UI/UX designer.

Build a complete, interactive, research-grade web application for exploring my Alzheimer’s disease experiment using ADNI MRI data and lightweight point-cloud representations.

## 1. Project objective

I have already completed the dataset preparation, model training, experiments, and evaluation. Do not retrain or replace my models unless explicitly requested.

The application must integrate:

1. ADNI MRI data.
2. Lightweight point-cloud data.
3. Extracted subject-level features.
4. Existing trained-model artifacts.
5. Existing prediction and evaluation results.
6. Research documents, experiment descriptions, Excel/CSV files, and model explanations.
7. A multimodal LLM chatbot using Retrieval-Augmented Generation (RAG).

The final system must allow a researcher to:

- Explore subjects and experiment results.
- View MRI volumes interactively.
- View and manipulate lightweight point clouds in 3D.
- Search by subject, diagnosis, visit, modality, or feature values.
- Ask natural-language questions.
- Upload an MRI image, scan, screenshot, or point-cloud file.
- Select specific features and ask questions about them.
- Run inference using my existing trained model.
- Receive explanations grounded in the database and retrieved sources.
- Compare subjects, models, features, and experimental results.

This is a research-support application, not an autonomous clinical diagnostic system.

## 2. Preferred technology stack

Use the following architecture unless an existing project requires compatible alternatives:

### Frontend

- React or Next.js with TypeScript.
- Tailwind CSS and shadcn/ui.
- Plotly or Apache ECharts for interactive scientific charts.
- NiiVue for NIfTI/MRI visualization.
- Three.js for point-cloud visualization.
- TanStack Query for API state management.
- A clean, responsive, professional medical-research interface.

### Backend

- Python FastAPI.
- Pydantic request and response schemas.
- WebSocket or server-sent-event streaming for chatbot responses.
- Modular services for ingestion, retrieval, inference, explanation, and file management.

### Storage

- PostgreSQL for structured subject, feature, experiment, and prediction data.
- pgvector for document and feature embeddings.
- Local or S3-compatible object storage for MRI, point-cloud, model, and report files.
- SQLite may be used only for the initial local demonstration.

### AI and RAG

- Keep the LLM provider configurable through environment variables.
- Use a modular embedding interface.
- Support local or API-based embedding and LLM models.
- Add metadata-filtered hybrid retrieval combining semantic similarity and structured database filters.
- Return source citations with every RAG-grounded answer.

## 3. Important retrieval design

Do not put every data type into one undifferentiated vector index.

Create three coordinated retrieval paths:

1. Structured retrieval:
   - Subject metadata.
   - Diagnosis labels.
   - Demographic variables.
   - MRI-derived measurements.
   - Point-cloud features.
   - Prediction values.
   - Performance metrics.
   - Feature-importance results.
2. Document RAG:
   - Excel or CSV descriptions.
   - Experiment notes.
   - Research reports.
   - Methodology descriptions.
   - Data dictionaries.
   - Model documentation.
   - Relevant PDF or text documents.
3. Similar-case retrieval:
   - Existing MRI embeddings, point-cloud embeddings, or standardized feature vectors.
   - Use these only when compatible encoders or feature representations are available.
   - Do not claim that raw MRI or point-cloud files can be searched semantically using text embeddings.
   - If an image or point-cloud encoder is unavailable, use extracted features and clearly report this limitation.

The LLM must orchestrate retrieval and explain results. Numerical prediction must come from my trained model, not from the LLM.

## 4. Main application pages

### A. Overview Dashboard

Display interactive cards and charts for:

- Number of subjects and scans.
- Diagnosis distribution, such as CN, MCI, and AD.
- Number of MRI and point-cloud files.
- Demographic distributions.
- Model accuracy, balanced accuracy, precision, recall, F1-score, AUROC, AUPRC, sensitivity, and specificity where available.
- Confusion matrix.
- ROC and precision–recall curves.
- Per-class performance.
- Feature-importance rankings.
- Data-quality and missing-value summaries.

All charts must support hover details, filtering, downloading, and cross-filtering where practical.

### B. Subject Explorer

Provide:

- Searchable and sortable subject table.
- Filters for subject ID, diagnosis, age, sex, visit, modality, model prediction, and feature ranges.
- Subject-detail page.
- Longitudinal visit timeline where repeated visits exist.
- MRI preview.
- Point-cloud preview.
- Extracted-feature table.
- Ground-truth label, predicted class, confidence, and model explanation.
- Similar-subject results with similarity score and retrieval basis.
- Export of selected subject information to CSV or PDF.

### C. MRI Viewer

Create an interactive MRI workspace with:

- NIfTI support and optional DICOM support if my files require it.
- Axial, sagittal, and coronal views.
- Optional 3D volume view.
- Slice navigation.
- Zoom, pan, reset, crosshair, window/level, opacity, and colormap controls.
- Segmentation-mask or heatmap overlay when available.
- Display of subject and scan metadata.
- Screenshot export.
- Side-by-side comparison of two selected scans.
- Clear loading progress and error handling for large files.

### D. Point-Cloud Viewer

Create a GPU-accelerated 3D viewer that supports the formats present in my dataset, such as PLY, PCD, XYZ, NPZ, or CSV.

Provide:

- Rotate, zoom, pan, reset, and fullscreen controls.
- Adjustable point size and opacity.
- Background and color-map controls.
- Color by class, intensity, region, or selected feature when available.
- Show/hide axes and bounding box.
- Display point count and compression ratio.
- Select or inspect individual points when technically feasible.
- Compare the original MRI-derived representation with the lightweight point cloud.
- Progressive loading or downsampling for performance.

### E. Multimodal RAG Chatbot

Create a persistent chatbot panel with:

- Text queries.
- MRI image or scan upload.
- Point-cloud upload.
- Subject selection.
- Feature-selection control.
- Suggested questions.
- Streaming responses.
- Conversation history.
- New-chat and clear-chat controls.

Example questions:

- “Show the prediction and most influential features for subject X.”
- “Why was this subject classified as AD?”
- “Compare this MRI with similar MCI subjects.”
- “Which point-cloud features distinguish AD from CN?”
- “Show the model’s performance for the MCI class.”
- “Which experiments produced the best balanced accuracy?”
- “Explain the relationship between hippocampal volume and the prediction.”
- “Find subjects with feature values similar to this uploaded sample.”

Every response must clearly separate:

- User input and active filters.
- Database facts.
- Retrieved evidence.
- Model prediction.
- Confidence or probability.
- Feature-level explanation.
- Similar cases.
- Source citations.
- Limitations or missing information.

Never invent unavailable feature values, predictions, citations, or medical interpretations.

### F. Feature Query and Comparison

Provide a dedicated feature-analysis page with:

- Multi-select feature control.
- Range filters.
- Histogram, box plot, violin plot, scatter plot, and correlation heatmap.
- Comparison by diagnosis or predicted class.
- Subject-level drill-down.
- Feature definitions and units.
- Missing-value indicators.
- Exportable filtered data.
- SHAP, permutation importance, attention, saliency, or other explanation outputs when supplied by my experiment.

### G. Knowledge-Base Administration

Provide an admin page to:

- Upload Excel, CSV, PDF, DOCX, TXT, JSON, and Markdown files.
- Preview extracted content.
- Map spreadsheet columns to the database schema.
- Configure document chunk size and overlap.
- Add metadata such as source, experiment, modality, date, model, and subject ID.
- Start or repeat vector indexing.
- Show indexing status and errors.
- Delete or re-index individual sources.
- Inspect retrieved chunks and similarity scores.
- Track source-file version and checksum to avoid duplicate ingestion.

## 5. Suggested database entities

Create normalized tables for:

- subjects
- visits
- scans
- point\_clouds
- features
- subject\_features
- models
- model\_versions
- predictions
- experiment\_runs
- evaluation\_metrics
- explanation\_results
- knowledge\_sources
- document\_chunks
- embeddings
- chat\_sessions
- chat\_messages
- audit\_logs

Store file references and metadata in the database, but keep large MRI and point-cloud files in object storage.

## 6. Existing experiment integration

Create adapters that can load my existing:

- Python model artifacts.
- PyTorch checkpoints.
- Scikit-learn pipelines.
- ONNX models.
- Pickle or joblib files.
- CSV/Excel prediction results.
- JSON configuration files.
- Feature lists and preprocessing objects.
- Confusion matrices, ROC values, and other saved metrics.

The inference pipeline must use exactly the same:

- Feature names.
- Feature ordering.
- Scaling.
- Normalization.
- Imputation.
- Class mapping.
- Preprocessing steps used during training.

Validate the uploaded feature schema before inference. If required inputs are missing or incompatible, display a specific error instead of producing a prediction.

## 7. UI design requirements

Use a modern scientific-dashboard style:

- Left navigation sidebar.
- Top search and active-subject selector.
- Main analysis workspace.
- Optional chatbot drawer on the right.
- Neutral light background with blue, teal, and purple accents.
- Diagnosis colors must remain consistent throughout the application.
- Clear typography and sufficient contrast.
- Responsive layout for laptop, desktop, and tablet.
- Dark mode.
- Tooltips for technical features and metrics.
- Skeleton loaders, upload progress, empty states, and useful error messages.
- Avoid decorative animations that distract from scientific analysis.

## 8. Privacy, validity, and safety

- Treat ADNI information as controlled research data.
- Do not expose credentials or restricted dataset URLs.
- Do not send identifiable or restricted raw data to an external LLM without explicit configuration and authorization.
- Store secrets only in environment variables.
- Validate uploads by extension, MIME type, and file size.
- Sanitize filenames.
- Implement authentication and role-based access for researcher and administrator roles.
- Keep audit logs for uploads, retrieval, inference, and exports.
- Display: “For research use only. This output is not a clinical diagnosis.”
- Do not claim causal or clinical conclusions from statistical associations.
- Make uncertainty and data limitations visible.

## 9. Required deliverables

Produce:

1. A clear architecture diagram.
2. A proposed repository structure.
3. Database schema and migrations.
4. Backend API implementation.
5. Responsive frontend implementation.
6. MRI and point-cloud viewers.
7. RAG ingestion and retrieval pipeline.
8. Existing-model adapter interface.
9. Example configuration files.
10. `.env.example` without secrets.
11. Docker Compose for local execution.
12. Synthetic demonstration data only—do not redistribute ADNI data.
13. Unit and integration tests.
14. API documentation.
15. Setup, ingestion, model-integration, and deployment instructions.
16. A user manual explaining each GUI page.
17. A list of assumptions and any information still required from me.

## 10. Development procedure

Implement the application in phases:

### Phase 1: Interactive prototype

- Build the full navigation and visual layout.
- Use synthetic subject data.
- Create working charts, filters, subject pages, chatbot layout, MRI viewer, and point-cloud viewer.
- Clearly label mock predictions.

### Phase 2: Data integration

- Import my Excel/CSV files.
- Create the structured database.
- Connect MRI and point-cloud file locations.
- Validate data types, feature names, missing values, and subject identifiers.

### Phase 3: Model integration

- Connect my existing trained models and preprocessing artifacts.
- Reproduce selected saved predictions to verify integration.
- Report any mismatch between the GUI pipeline and my experiment results.

### Phase 4: RAG integration

- Ingest research and experiment documents.
- Implement structured, semantic, and hybrid retrieval.
- Add source citations and retrieval inspection.

### Phase 5: Testing and deployment

- Add authentication, validation, logging, tests, Docker deployment, and documentation.
- Optimize large-file and 3D-viewer performance.

Do not attempt to implement everything in one unverified step. At the end of each phase, run the application, test its main workflow, report completed features, and identify the files or information required for the next phase.

Before starting implementation, inspect my supplied files and ask only the essential questions about:

- Dataset file formats and folder structure.
- MRI format.
- Point-cloud format.
- Diagnosis classes.
- Complete feature list and units.
- Model framework and artifact format.
- Preprocessing artifacts.
- Experiment-result file formats.
- Preferred LLM and embedding model.
- Local or cloud deployment requirement.

Then show the proposed architecture, folder structure, database schema, and first implementation milestone.
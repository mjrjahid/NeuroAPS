# NeuroLens Phase 1 User Guide

## Important boundary

NeuroLens Phase 1 is an interactive frontend prototype. All displayed subjects, scans, point clouds, measurements, predictions, metrics, explanations, and citations are synthetic. It does not read real ADNI data, execute a trained model, or call a production RAG backend.

For research use only. This output is not a clinical diagnosis.

## Starting the application

- Windows: double-click `start_windows.bat`.
- macOS/Linux: run `chmod +x start_mac_linux.sh`, then `./start_mac_linux.sh`.
- Direct mode: open `index.html` in a current browser.

## Main workspaces

### Overview

Review the synthetic cohort totals, diagnosis distribution, model metrics, feature importance, and experiment summaries. Cards and plots illustrate how real experiment outputs will be presented during data integration.

### Subject Explorer

Search or filter the demonstration subjects. Selecting a row updates the active-subject context used by other panels. The detail view shows mock metadata, diagnosis, prediction, confidence, features, and similar cases.

### MRI Viewer

Use the slice and display controls to interact with synthetic axial, coronal, and sagittal canvas views. These are visual placeholders for a later NiiVue-based NIfTI/DICOM integration.

### Point Cloud

Drag to rotate, use the mouse wheel to zoom, and use the panel controls to change the synthetic point-cloud presentation. The production phase will replace this canvas demonstration with format-specific Three.js loaders.

### Feature Analysis

Select features and inspect the demonstration distributions, comparisons, and mock explanation ranking. Real values, units, missing-data rules, and explanation outputs must come from the supplied experiment files.

### RAG Assistant

Enter a question or choose a suggested query. Responses are divided into database facts, model output, feature explanation, similar cases, limitations, and sources. The current responses are scripted demonstrations, not LLM-generated medical conclusions.

### Knowledge Base

Choose a supported document to simulate validation and indexing. The browser does not upload the file to a server in Phase 1. Production ingestion will require a backend, checksums, metadata, vector indexing, access controls, and source inspection.

### Architecture

Review the intended production components and the five implementation phases. Phase 2 begins when representative data and model artifacts are supplied.

## Data required for Phase 2

1. One representative MRI file and its format.
2. One representative point-cloud file and its coordinate/channel definition.
3. The complete feature table with names, units, subject IDs, and visit IDs.
4. The trained model, preprocessing artifacts, feature order, and class mapping.
5. Saved predictions and experiment metrics.
6. Research documents and data dictionaries for the knowledge base.

Do not place restricted ADNI data, credentials, secrets, or identifiable records in a public repository.

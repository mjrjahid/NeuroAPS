# MRI-to-point-cloud sample integration

## Included examples

The workspace registers 10 subjects (AD1–AD10), each with:

- one 3D float32 T1 MRI;
- one registered brain mask used to isolate the brain view;
- one ASCII PLY point cloud containing 8,192 points.

The application presents the scientific workflow as:

**brain-only MRI → anatomically labelled point cloud**

## Viewer controls

- axial, coronal, and sagittal MRI planes;
- synchronized slice selection;
- balanced, tissue-focused, and full-range contrast;
- anatomical-region filtering;
- minimum reliability filtering;
- point size and opacity;
- anatomical-region, reliability, and original-file color views;
- interactive rotate, zoom, pan, and hover.

## Anatomical labels

| PLY label | Region | Interface color |
|---:|---|---|
| 1 | Hippocampus | pink |
| 3 | Ventricles | teal |
| 5 | Cortical area | purple |
| 7 | Other brain tissue | gold |

These names follow the mapping supplied for this application update.

## Interface simplification

The professional viewer intentionally omits:

- mask-code distribution;
- PLY integrity tables;
- alignment/checksum panels;
- synthetic teaching views;
- long internal-processing notices.

The manifest remains in data/samples/sample_manifest.json for application loading and technical verification.

## Research scope

The interface is a research demonstrator and not a clinical diagnosis. A formal evaluation requires the versioned model, complete preprocessing configuration, class mapping, local governance approval, and clinician study.

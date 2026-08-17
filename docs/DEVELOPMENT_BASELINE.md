# Development baseline

## Source hierarchy

1. The two published NeuroAPS-Net / Sampling Matters contributions and their supplied characterized records.
2. 2.mentoring.session.pptx for application and demonstration requirements.
3. ITU-T Y.3172 for ML-pipeline terminology.
4. Papers_Only Dimension Mapping.docx for the papers-only 13-dimension assessment.
5. Supplied clinical, Eastern Province, and Saudi public-domain policy notes.
6. User-supplied AD1–AD10 raw MRI, mask, and PLY examples.
7. Earlier Phase 1 interface, preserved in legacy_phase1.

## Preserved evidence

- ADNI-2DPC: 1,000 subjects (500 AD / 500 CN).
- NeuroAPS-Net: 84.85% accuracy, 1.48 ms inference, and 234.6 MB peak GPU memory at 8,192 points.
- Hardware: one NVIDIA RTX 3060.
- Intended role: clinician/researcher decision support.
- Anatomical emphasis: hippocampus, ventricles, cortical area, and other brain tissue.

## Final-interface changes

- Added a qualitative dense 3D-CNN limitation view and a measured NeuroAPS-Net comparison against supplied point-cloud baselines.
- Replaced readiness gap cards with application coverage and evidence.
- Updated all 13 readiness dimensions with paper baseline, application coverage, implemented evidence, and next evaluation.
- Expanded the human-in-the-loop workflow to six clinical evaluation steps.
- Aligned every Y.3172 node with a concrete function, status, and implemented evidence.
- Removed the pipeline lock notice.
- Simplified the imaging workspace to brain-only MRI → point-cloud representation.
- Applied the supplied PLY label mapping: 1 hippocampus, 3 ventricles, 5 cortical area, and 7 other brain tissue.
- Removed mask-distribution, PLY-integrity, checksum/alignment, and synthetic-teaching panels.
- Rebuilt the Saudi workspace around validated official public sources.
- Added professional topic illustrations and concise navigation.

## Public-source validation

The source register in data/source_notes/saudi_policy_validation.txt records:

- HSTP / Saudi Vision 2030;
- NSDAI / SDAIA;
- Seha Virtual Hospital and Innovation Empowerment Center / MOH;
- PDPL and National Data Governance Platform / SDAIA;
- AI Ethics Self-Assessment / SDAIA;
- four retained Eastern Province / Saudi research records.

The application treats these as alignment evidence. It does not infer regulatory approval, partnership, clinical validation, or hospital integration.

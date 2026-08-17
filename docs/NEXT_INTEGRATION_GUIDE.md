# Next integration guide

## Required artifact bundle

Provide the following together so the next model-enabled build can be verified end to end:

1. A de-identified feature table with a data dictionary and units.
2. Expected subject/visit identifiers and provenance for the 10 supplied raw MRI volumes and aligned NIfTI masks. The files and geometry checks are now integrated.
3. Coordinate-system and physical-unit documentation for the supplied PLY fields. The anatomical mapping is integrated as label 1 hippocampus, 3 ventricles, 5 cortical area, and 7 other brain tissue.
4. The trained model artifact and model-definition code.
5. Every preprocessing artifact used during training: imputer, scaler, normalizer, label encoder, class map, feature list, and configuration.
6. A saved prediction/result table containing at least a few known inputs, expected classes, probabilities, and model version.
7. Final experiment metrics and plots in CSV/JSON where possible.

The current sample bundle contains only AD-labeled examples. Provide representative CN data before implementing class-comparison or validation views.

Do not include restricted ADNI data unless the local handling environment is authorized for it.

## Acceptance test before inference is enabled

The GUI inference adapter must:

1. Validate file type and schema.
2. Match the expected subject and visit.
3. Reproduce the training preprocessing byte-for-byte or step-for-step.
4. Confirm feature order and class mapping.
5. Run the registered model version.
6. Reproduce selected saved predictions within a defined numeric tolerance.
7. Log the input checksum, preprocessing version, model version, output, and any warning.
8. Refuse prediction if any required field or artifact is missing.

## Retrieval paths to preserve

- Structured retrieval: subject, visit, features, predictions, and metrics.
- Document retrieval: papers, methods, policies, standards, and experiment documentation.
- Similar-case retrieval: compatible MRI/point-cloud embeddings or standardized feature vectors only.

Raw MRI, mask, and point-cloud files must not be placed in a text-embedding index. If a validated modality encoder is unavailable, similar-case search must use registered extracted features and clearly state that basis.

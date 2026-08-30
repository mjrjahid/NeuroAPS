# Controlled imaging artifacts

The public repository does not distribute the registered raw MRI, segmentation-mask, or point-cloud files.

Authorized users can activate the complete local imaging workspace by placing the expected files under:

```text
data/samples/raw_mri/
data/samples/nifti/
data/samples/point_clouds/
```

Keep the filenames recorded in `sample_manifest.json`. The application verifies file presence, byte count, alignment metadata, and—during the complete integrity test—SHA-256 checksums before the artifacts are used.

Official access information: https://adni.loni.usc.edu/data-samples/

Do not commit controlled data, patient-identifying information, or credentials.

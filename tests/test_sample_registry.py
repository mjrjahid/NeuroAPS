"""Integrity checks for the user-supplied raw-MRI/mask/PLY cohort."""

from __future__ import annotations

import unittest
from pathlib import Path

from src.project_data import POINT_LABELS
from src.sample_registry import load_sample_manifest, subject_lookup, validate_manifest_files


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "samples" / "sample_manifest.json"


class SampleRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load_sample_manifest(MANIFEST)
        cls.subjects = subject_lookup(cls.manifest)

    def test_ten_unique_triples_are_registered(self):
        self.assertEqual(self.manifest["sample_count"], 10)
        self.assertEqual(self.manifest["triple_count"], 10)
        self.assertEqual(self.manifest["artifact_count"], 30)
        self.assertEqual(set(self.subjects), {f"AD{index}" for index in range(1, 11)})

    def test_all_files_match_size_and_sha256(self):
        self.assertEqual(validate_manifest_files(self.manifest, ROOT, verify_hashes=True), [])

    def test_raw_mri_files_are_finite_float_intensity_volumes(self):
        for subject in self.subjects.values():
            raw = subject["raw_mri"]
            self.assertEqual(raw["datatype_code"], 16)
            self.assertEqual(raw["content_kind"], "raw_intensity_mri")
            self.assertEqual(raw["shape"][:2], [256, 256])
            self.assertEqual(raw["intensity"]["finite_fraction"], 1.0)
            self.assertGreater(raw["intensity"]["maximum"], raw["intensity"]["minimum"])

    def test_segmentation_masks_are_discrete_and_aligned(self):
        for subject in self.subjects.values():
            mask = subject["segmentation_mask"]
            self.assertEqual(mask["datatype_code"], 2)
            self.assertEqual(set(mask["label_counts"]), {"0", "1", "2", "3", "4"})
            self.assertEqual(subject["raw_mri"]["shape"], mask["shape"])
            self.assertTrue(subject["alignment"]["validated"])
            self.assertTrue(subject["alignment"]["qform_match"])
            self.assertTrue(subject["alignment"]["overlay_permitted"])

    def test_ply_schema_is_consistent(self):
        required_properties = {"x", "y", "z", "x_norm", "y_norm", "z_norm", "red", "green", "blue", "label", "branch", "reliability"}
        for subject in self.subjects.values():
            cloud = subject["point_cloud"]
            self.assertEqual(cloud["vertex_count"], 8192)
            self.assertTrue(required_properties.issubset(cloud["properties"]))
            self.assertEqual(set(cloud["label_counts"]), {"1", "3", "5", "7"})
            self.assertEqual(sum(cloud["label_counts"].values()), 8192)

    def test_point_labels_have_supplied_anatomical_names(self):
        self.assertEqual(POINT_LABELS[1], "Hippocampus")
        self.assertEqual(POINT_LABELS[3], "Ventricles")
        self.assertEqual(POINT_LABELS[5], "Cortical area")
        self.assertEqual(POINT_LABELS[7], "Other brain tissue")


if __name__ == "__main__":
    unittest.main()

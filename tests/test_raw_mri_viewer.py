"""Focused tests for synchronized raw-MRI and mask rendering."""

from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from src.viewers import point_cloud_figure, raw_mri_slice_figure


class RawMRIViewerTests(unittest.TestCase):
    def setUp(self):
        self.raw = np.arange(8 * 9 * 10, dtype=np.float32).reshape(8, 9, 10)
        self.mask = np.zeros_like(self.raw, dtype=np.uint8)
        self.mask[2:6, 3:7, 4:8] = 2

    def test_raw_view_has_one_intensity_trace(self):
        figure = raw_mri_slice_figure(self.raw, self.mask, "Axial", 5, display_mode="Brain-only MRI")
        self.assertEqual(len(figure.data), 1)

    def test_brain_only_view_hides_non_brain_voxels(self):
        figure = raw_mri_slice_figure(self.raw, self.mask, "Axial", 5, display_mode="Brain-only MRI")
        rendered = np.asarray(figure.data[0].z)
        mask_view = np.rot90(np.take(self.mask, 5, axis=2))
        self.assertTrue(np.isnan(rendered[mask_view == 0]).all())

    def test_overlay_has_aligned_second_trace(self):
        figure = raw_mri_slice_figure(
            self.raw,
            self.mask,
            "Coronal",
            4,
            display_mode="Raw + mask overlay",
            overlay_opacity=0.5,
        )
        self.assertEqual(len(figure.data), 2)
        self.assertEqual(np.asarray(figure.data[0].z).shape, np.asarray(figure.data[1].z).shape)

    def test_mismatched_shape_is_rejected(self):
        with self.assertRaises(ValueError):
            raw_mri_slice_figure(self.raw, self.mask[..., :-1], "Axial", 3)

    def test_anatomical_point_labels_are_named(self):
        frame = pd.DataFrame({
            "x": [0.0, 1.0, 2.0, 3.0],
            "y": [0.0, 1.0, 2.0, 3.0],
            "z": [0.0, 1.0, 2.0, 3.0],
            "label": [1, 3, 5, 7],
            "reliability": [1.0, 1.0, 1.0, 1.0],
        })
        figure = point_cloud_figure(frame, color_mode="Anatomical region")
        self.assertEqual(
            {trace.name for trace in figure.data},
            {"Hippocampus", "Ventricles", "Cortical area", "Other brain tissue"},
        )


if __name__ == "__main__":
    unittest.main()

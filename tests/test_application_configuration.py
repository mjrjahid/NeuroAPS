"""Checks for the revised readiness, policy, and workflow configuration."""

from __future__ import annotations

import unittest
from pathlib import Path

from src.project_data import (
    BASELINE_COMPARISON,
    FACTORS,
    PIPELINE,
    POLICY_SOURCES,
    PUBLIC_DOMAIN_SOURCES,
    READINESS_DIMENSIONS,
    SCENARIO,
)


ROOT = Path(__file__).resolve().parents[1]


class ApplicationConfigurationTests(unittest.TestCase):
    def test_readiness_uses_coverage_evidence_not_gap_fields(self):
        self.assertEqual(len(FACTORS), 6)
        self.assertTrue(all("coverage" in factor and "evidence" in factor for factor in FACTORS))
        self.assertTrue(all("gap" not in factor for factor in FACTORS))

    def test_all_thirteen_dimensions_are_mapped(self):
        self.assertEqual(len(READINESS_DIMENSIONS), 13)
        self.assertTrue(all(len(row) == 5 for row in READINESS_DIMENSIONS))

    def test_human_review_scenario_has_six_steps(self):
        self.assertEqual(len(SCENARIO), 6)
        self.assertEqual([row[0] for row in SCENARIO], [str(index) for index in range(1, 7)])

    def test_pipeline_nodes_are_unique_and_statused(self):
        self.assertEqual(len({row[0] for row in PIPELINE}), len(PIPELINE))
        self.assertTrue(all(row[2].strip() for row in PIPELINE))

    def test_comparison_contains_proposed_model(self):
        proposed = [row for row in BASELINE_COMPARISON if row[0] == "NeuroAPS-Net"]
        self.assertEqual(proposed, [("NeuroAPS-Net", 84.85, 1.48, 234.60)])

    def test_policy_sources_use_https(self):
        self.assertEqual(len(POLICY_SOURCES), 4)
        self.assertTrue(all(source["url"].startswith("https://") for source in POLICY_SOURCES))

    def test_public_domain_source_register_is_tiered_and_linked(self):
        self.assertGreaterEqual(len(PUBLIC_DOMAIN_SOURCES), 13)
        self.assertTrue(all(source["url"].startswith("https://") for source in PUBLIC_DOMAIN_SOURCES))
        tiers = {source["tier"] for source in PUBLIC_DOMAIN_SOURCES}
        self.assertEqual(tiers, {"Official government", "Public background", "Public research"})
        urls = {source["url"] for source in PUBLIC_DOMAIN_SOURCES}
        self.assertIn(
            "https://www.vision2030.gov.sa/media/h0yb5d03/health-sector-transformation-report-2024.pdf",
            urls,
        )
        self.assertIn("https://www.moh.gov.sa/en/statistics/pages/dashboard.aspx", urls)

    def test_supplied_context_visuals_are_packaged(self):
        expected = {
            "neurocloud_platform_vision.png",
            "problem_inefficient_neuroimaging.png",
            "current_manual_analysis.png",
            "root_cause_delayed_diagnosis.png",
            "saudi_neurological_impact.png",
            "hackathon_storyboard.png",
        }
        self.assertTrue(all((ROOT / "assets" / name).is_file() for name in expected))

    def test_evidence_mode_is_a_popover_and_summary_metric_is_removed(self):
        app_source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn('st.popover("Evidence mode", use_container_width=True)', app_source)
        self.assertNotIn("Application readiness summary", app_source)
        self.assertIn('"Context & Impact"', app_source)


if __name__ == "__main__":
    unittest.main()

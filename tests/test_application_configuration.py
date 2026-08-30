"""Checks for the revised readiness, policy, and workflow configuration."""

from __future__ import annotations

import unittest
from pathlib import Path

from src.project_data import (
    BASELINE_COMPARISON,
    FACTORS,
    GOVERNANCE_SCENARIO,
    PIPELINE,
    PDPL_AI_ETHICS_CONTROLS,
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
        self.assertTrue(all(source["links"] for source in POLICY_SOURCES))
        self.assertTrue(
            all(
                link["url"].startswith("https://")
                for source in POLICY_SOURCES
                for link in source["links"]
            )
        )
        self.assertTrue(all(source["boundary"].strip() for source in POLICY_SOURCES))

    def test_public_domain_source_register_is_tiered_and_linked(self):
        self.assertEqual(len(PUBLIC_DOMAIN_SOURCES), 13)
        self.assertTrue(all(source["url"].startswith("https://") for source in PUBLIC_DOMAIN_SOURCES))
        tiers = {source["tier"] for source in PUBLIC_DOMAIN_SOURCES}
        self.assertEqual(
            tiers,
            {"Official government", "Public background", "Public research"},
        )
        urls = {source["url"] for source in PUBLIC_DOMAIN_SOURCES}
        self.assertIn(
            "https://www.vision2030.gov.sa/media/h0yb5d03/health-sector-transformation-report-2024.pdf",
            urls,
        )
        self.assertIn("https://www.moh.gov.sa/en/statistics/pages/dashboard.aspx", urls)
        self.assertNotIn("https://adni.loni.usc.edu/data-samples/", urls)

    def test_adni_is_controlled_access_and_open_source_claim_is_bounded(self):
        factors = {factor["name"]: factor for factor in FACTORS}
        self.assertEqual(factors["Open Data"]["source_url"], "https://adni.loni.usc.edu/data-samples/")
        self.assertIn("controlled research access", factors["Open Data"]["coverage"].lower())
        self.assertIn("github.com/mjrjahid/NeuroAPS", factors["Open Source"]["evidence"])
        self.assertIn("Controlled imaging artifacts remain excluded", factors["Open Source"]["evidence"])

    def test_pdpl_ethics_and_governance_controls_are_explicit(self):
        self.assertEqual(len(PDPL_AI_ETHICS_CONTROLS), 6)
        controls_text = " ".join(" ".join(row) for row in PDPL_AI_ETHICS_CONTROLS).lower()
        self.assertIn("article 25", controls_text)
        self.assertIn("lawful basis", controls_text)
        self.assertIn("no unrelated profiling", controls_text)
        self.assertEqual(len(GOVERNANCE_SCENARIO), 4)
        scenario_text = " ".join(" ".join(row) for row in GOVERNANCE_SCENARIO).lower()
        self.assertIn("advertising", scenario_text)
        self.assertIn("insurer", scenario_text)

    def test_prevention_claim_is_qualified_in_application(self):
        app_source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn("HSTP explicitly prioritizes disease prevention", app_source)
        self.assertIn("not presented as a direct HSTP quotation", app_source)
        self.assertIn("PDPL and AI-ethics control cross-check", app_source)

    def test_criteria_crosscheck_is_packaged(self):
        crosscheck = ROOT / "docs" / "CRITERIA_CROSSCHECK.md"
        self.assertTrue(crosscheck.is_file())
        text = crosscheck.read_text(encoding="utf-8")
        self.assertIn("ADNI Data and Samples", text)
        self.assertIn("Saudi MOH statistics dashboard", text)
        self.assertIn("PDPL and AI ethics", text)

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

    def test_each_workspace_has_a_topic_specific_visual(self):
        expected = {
            "neurocloud_platform_vision.png",
            "readiness_efficiency.svg",
            "y3172_pipeline.svg",
            "mri_pointcloud_workspace.svg",
            "policy_alignment.svg",
            "knowledge_rag.svg",
            "research_assistant_bot.svg",
            "deployment_workbench.svg",
        }
        self.assertEqual(len(expected), 8)
        self.assertTrue(all((ROOT / "assets" / name).is_file() for name in expected))
        app_source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn("WORKSPACE_VISUALS", app_source)
        self.assertIn('visual_uri = image_data_uri(visual["image"])', app_source)
        self.assertEqual(app_source.count("render_workspace_hero("), 9)

    def test_evidence_mode_is_a_popover_and_summary_metric_is_removed(self):
        app_source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn('st.popover("Evidence mode", use_container_width=True)', app_source)
        self.assertNotIn("Application readiness summary", app_source)
        self.assertIn('"Context & Impact"', app_source)

    def test_top_tabs_use_menu_hover_and_active_states(self):
        app_source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn('button[data-baseweb="tab"]:hover', app_source)
        self.assertIn('button[data-baseweb="tab"][aria-selected="true"]', app_source)
        self.assertIn('button[data-baseweb="tab"]:focus-visible', app_source)
        self.assertIn('flex-wrap:nowrap', app_source)
        self.assertIn('overflow-x:auto', app_source)
        self.assertIn('position:sticky', app_source)
        self.assertIn("default=requested_workspace", app_source)
        self.assertIn("on_change=sync_workspace_query", app_source)

    def test_research_assistant_is_in_top_menu_and_uses_bot_interface(self):
        app_source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn('"Research Assistant",', app_source)
        self.assertIn("NeuroAPS Evidence Copilot", app_source)
        self.assertIn('class="bot-profile"', app_source)
        self.assertIn('key="assistant_chat"', app_source)
        self.assertIn("Retrieved evidence and citations", app_source)
        self.assertIn("Ask NeuroAPS about evidence", app_source)
        self.assertIn("Saudi source entries", app_source)
        self.assertIn("structured evidence records—not raw text", app_source)
        self.assertIn("Knowledge base scope and reference links", app_source)

    def test_professional_workspace_shell_is_packaged(self):
        app_source = (ROOT / "app.py").read_text(encoding="utf-8")
        required_markers = {
            'class="application-head"',
            'class="application-state"',
            'class="hero-web"',
            'aria-label="{workspace_name} workspace introduction"',
            'class="site-footer"',
            '@media (max-width:700px)',
        }
        self.assertTrue(all(marker in app_source for marker in required_markers))
        self.assertNotIn('class="site-nav"', app_source)
        self.assertNotIn('class="site-menu"', app_source)
        self.assertIn("visual['title']", app_source)
        self.assertIn("WORKSPACE_VISUALS", app_source)
        self.assertNotIn("MedicineOne", app_source)


if __name__ == "__main__":
    unittest.main()

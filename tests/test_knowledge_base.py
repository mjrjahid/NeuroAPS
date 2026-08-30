"""Built-in unittest coverage for the local retrieval layer."""

from __future__ import annotations

import unittest
from pathlib import Path

from src.knowledge_base import KnowledgeBase, build_manifest, chunk_text, load_records


ROOT = Path(__file__).resolve().parents[1]


class KnowledgeBaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = load_records(ROOT / "data" / "knowledge_records.json")
        cls.kb = KnowledgeBase(cls.records)

    def test_all_ten_records_load(self):
        self.assertEqual(len(self.records), 10)
        self.assertEqual(len({record["id"] for record in self.records}), 10)
        self.assertEqual(len(self.kb.chunks), 46)

    def test_retrieval_finds_neuroaps_efficiency(self):
        hits = self.kb.retrieve("inference latency and GPU memory", top_k=3)
        self.assertTrue(hits)
        self.assertIn("neuroaps_net", {hit.record_id for hit in hits})

    def test_retrieval_finds_regional_context(self):
        hits = self.kb.retrieve("Dammam hospital 152 patients", top_k=3)
        self.assertTrue(hits)
        self.assertEqual(hits[0].record_id, "eastern_province_context")

    def test_type_filter_is_enforced(self):
        hits = self.kb.retrieve("Saudi policy", top_k=5, record_types=["policy_document"])
        self.assertTrue(hits)
        self.assertTrue(all(hit.record_type == "policy_document" for hit in hits))

    def test_manifest_is_stable_shape(self):
        manifest = build_manifest(self.records)
        self.assertEqual(manifest["record_count"], 10)
        self.assertEqual(len(manifest["sha256"]), 64)

    def test_saudi_records_expose_verified_public_links(self):
        expected = {
            "clinical_atrophy_patterns",
            "eastern_province_context",
            "hstp",
            "hstp_2024_report",
            "neuroaps_net",
            "nsdai",
            "sampling_matters",
            "saudi_ad_genetics_review",
            "saudi_nghs_prevalence",
            "seha_digital_health",
        }
        linked = {record["id"] for record in self.records if record.get("public_links")}
        self.assertEqual(linked, expected)
        for record in self.records:
            for link in record.get("public_links", []):
                self.assertTrue(link["url"].startswith("https://"))
                self.assertIn(
                    link["category"],
                    {"Official government", "Official research dataset", "Public background", "Public research"},
                )

    def test_new_saudi_records_are_retrievable(self):
        prevalence_hits = self.kb.retrieve("3.37 percent National Guard participants", top_k=5)
        self.assertIn("saudi_nghs_prevalence", {hit.record_id for hit in prevalence_hits})
        genetics_hits = self.kb.retrieve("Saudi Alzheimer genetics understudied population", top_k=5)
        self.assertIn("saudi_ad_genetics_review", {hit.record_id for hit in genetics_hits})
        report_hits = self.kb.retrieve("Security Forces Hospital 23000 AI imaging tests", top_k=5)
        self.assertIn("hstp_2024_report", {hit.record_id for hit in report_hits})

    def test_neuroaps_record_links_to_official_adni_access(self):
        record = next(record for record in self.records if record["id"] == "neuroaps_net")
        urls = {link["url"] for link in record["public_links"]}
        self.assertIn("https://adni.loni.usc.edu/data-samples/", urls)
        self.assertIn("controlled research access", record["full_text"])

    def test_requested_record_links_are_present(self):
        by_id = {record["id"]: record for record in self.records}
        self.assertEqual(
            by_id["sampling_matters"]["reference_link"],
            "https://github.com/towhidulislam133086/ITU-Hac/blob/main/IJCNN2026_SaplingMatters_Towhid_et_al.pdf",
        )
        self.assertEqual(
            by_id["saudi_nghs_prevalence"]["reference_link"],
            "https://pubmed.ncbi.nlm.nih.gov/39962762/",
        )
        self.assertEqual(
            by_id["saudi_ad_genetics_review"]["reference_link"],
            "https://pubmed.ncbi.nlm.nih.gov/39994993/",
        )
        self.assertEqual(
            by_id["hstp_2024_report"]["reference_link"],
            "https://www.vision2030.gov.sa/media/h0yb5d03/health-sector-transformation-report-2024.pdf",
        )

    def test_policy_record_contains_bounded_pdpl_controls(self):
        record = next(record for record in self.records if record["id"] == "nsdai")
        self.assertIn("Article 25", record["full_text"])
        self.assertIn("consent is required where applicable", record["full_text"].lower())
        self.assertIn("does not by itself certify", record["full_text"])

    def test_chunk_bounds(self):
        chunks = chunk_text("Sentence one. " * 200, chunk_size=300, overlap=50)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk) <= 305 for chunk in chunks))


if __name__ == "__main__":
    unittest.main()

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

    def test_all_seven_records_load(self):
        self.assertEqual(len(self.records), 7)
        self.assertEqual(len({record["id"] for record in self.records}), 7)

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
        self.assertEqual(manifest["record_count"], 7)
        self.assertEqual(len(manifest["sha256"]), 64)

    def test_saudi_records_expose_verified_public_links(self):
        expected = {"eastern_province_context", "hstp", "nsdai", "seha_digital_health"}
        linked = {record["id"] for record in self.records if record.get("public_links")}
        self.assertEqual(linked, expected)
        for record in self.records:
            for link in record.get("public_links", []):
                self.assertTrue(link["url"].startswith("https://"))
                self.assertIn(link["category"], {"Official government", "Public background", "Public research"})

    def test_chunk_bounds(self):
        chunks = chunk_text("Sentence one. " * 200, chunk_size=300, overlap=50)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk) <= 305 for chunk in chunks))


if __name__ == "__main__":
    unittest.main()

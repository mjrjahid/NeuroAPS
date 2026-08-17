"""Smoke-test the complete Streamlit application."""

from __future__ import annotations

import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]


class StreamlitApplicationTests(unittest.TestCase):
    def test_application_runs_without_exceptions(self):
        app = AppTest.from_file(str(ROOT / "app.py"))
        app.run(timeout=120)
        self.assertEqual(list(app.exception), [])

        app.selectbox(key="registered_subject").select("AD10")
        app.run(timeout=120)
        self.assertEqual(list(app.exception), [])

        app.selectbox(key="context_story").select("Why it matters in Saudi Arabia")
        app.selectbox(key="saudi_source_tier").select("Public research")
        app.run(timeout=120)
        self.assertEqual(list(app.exception), [])


if __name__ == "__main__":
    unittest.main()

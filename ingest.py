"""Validate the characterized records and emit a reproducibility manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.knowledge_base import KnowledgeBase, build_manifest, load_records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, default=Path("data/knowledge_records.json"))
    parser.add_argument("--manifest", type=Path, default=Path("data/kb_manifest.json"))
    args = parser.parse_args()

    records = load_records(args.records)
    kb = KnowledgeBase(records)
    manifest = build_manifest(records)
    manifest["retrieval_chunk_count"] = len(kb.chunks)
    manifest["retrieval_method"] = "TF-IDF unigrams+bigrams, cosine similarity"
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Validated {len(records)} characterized records and {len(kb.chunks)} retrieval chunks.")
    print(f"Manifest written to {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


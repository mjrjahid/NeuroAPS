"""Validated, local-first retrieval over characterized knowledge records."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


REQUIRED_FIELDS = {
    "id",
    "title",
    "type",
    "status",
    "domain",
    "country_scope",
    "factors",
    "dimensions",
    "key_metrics",
    "images",
    "reference_link",
    "source_file",
    "full_text",
    "summary",
}


@dataclass(frozen=True)
class RetrievalHit:
    record_id: str
    title: str
    record_type: str
    source_file: str
    reference_link: str | None
    chunk_id: int
    text: str
    score: float

    def to_dict(self) -> dict:
        return asdict(self)


def load_records(path: str | Path) -> list[dict]:
    """Load and validate characterized records.

    Loading JSON rather than a pickle keeps startup inspectable and avoids
    deserializing executable Python objects.
    """

    source = Path(path)
    records = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(records, list) or not records:
        raise ValueError("knowledge_records.json must contain a non-empty list")

    seen: set[str] = set()
    for position, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"Record {position} is not a JSON object")
        missing = sorted(REQUIRED_FIELDS.difference(record))
        if missing:
            raise ValueError(f"Record {position} is missing: {', '.join(missing)}")
        record_id = str(record["id"]).strip()
        if not record_id:
            raise ValueError(f"Record {position} has an empty id")
        if record_id in seen:
            raise ValueError(f"Duplicate record id: {record_id}")
        seen.add(record_id)
        if not str(record["full_text"]).strip():
            raise ValueError(f"Record {record_id} has no full_text")
    return records


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 160) -> list[str]:
    """Create bounded, overlapping text chunks with sentence-aware endings."""

    if chunk_size < 200:
        raise ValueError("chunk_size must be at least 200 characters")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size")

    normalized = re.sub(r"\n{3,}", "\n\n", text.strip())
    chunks: list[str] = []
    start = 0
    while start < len(normalized):
        tentative = min(start + chunk_size, len(normalized))
        end = tentative
        if tentative < len(normalized):
            candidates = [
                normalized.rfind(". ", start + chunk_size // 2, tentative + 1),
                normalized.rfind("\n", start + chunk_size // 2, tentative + 1),
            ]
            boundary = max(candidates)
            if boundary > start:
                end = boundary + 1
        chunk = normalized[start:end].strip()
        if len(chunk) > 30:
            chunks.append(chunk)
        if end >= len(normalized):
            break
        start = max(end - overlap, start + 1)
    return chunks


class KnowledgeBase:
    """In-memory TF-IDF retrieval with metadata filters and traceable hits."""

    def __init__(self, records: Sequence[dict], chunk_size: int = 900, overlap: int = 160):
        self.records = list(records)
        self.chunks: list[dict] = []
        for record in self.records:
            for chunk_id, text in enumerate(chunk_text(record["full_text"], chunk_size, overlap)):
                self.chunks.append(
                    {
                        "record_id": record["id"],
                        "title": record["title"],
                        "record_type": record["type"],
                        "source_file": record["source_file"],
                        "reference_link": record.get("reference_link"),
                        "chunk_id": chunk_id,
                        "text": text,
                    }
                )
        if not self.chunks:
            raise ValueError("No retrievable chunks were created")
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_df=0.95,
            min_df=1,
            ngram_range=(1, 2),
            sublinear_tf=True,
        )
        self.matrix = self.vectorizer.fit_transform(chunk["text"] for chunk in self.chunks)

    @property
    def record_types(self) -> list[str]:
        return sorted({str(record["type"]) for record in self.records})

    def retrieve(
        self,
        query: str,
        top_k: int = 4,
        record_types: Iterable[str] | None = None,
        min_score: float = 0.01,
    ) -> list[RetrievalHit]:
        query = query.strip()
        if not query:
            return []
        allowed = set(record_types or [])
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.matrix).ravel()
        ranked = similarities.argsort()[::-1]
        hits: list[RetrievalHit] = []
        for index in ranked:
            item = self.chunks[int(index)]
            score = float(similarities[int(index)])
            if score < min_score:
                continue
            if allowed and item["record_type"] not in allowed:
                continue
            hits.append(RetrievalHit(score=score, **item))
            if len(hits) >= max(1, top_k):
                break
        return hits


def build_extractive_answer(hits: Sequence[RetrievalHit]) -> str:
    """Return a transparent offline answer without inventing synthesis."""

    if not hits:
        return (
            "No sufficiently relevant evidence was found in the current seven-record "
            "knowledge base. Refine the question or inspect the records directly."
        )
    lines = ["The most relevant evidence currently available is:"]
    for number, hit in enumerate(hits[:4], start=1):
        excerpt = re.sub(r"\s+", " ", hit.text).strip()
        if len(excerpt) > 420:
            excerpt = excerpt[:417].rsplit(" ", 1)[0] + "..."
        lines.append(f"{number}. {excerpt} [{number}]")
    lines.append(
        "\nThis is retrieval evidence, not a clinical interpretation or a trained-model prediction."
    )
    return "\n\n".join(lines)


def build_manifest(records: Sequence[dict]) -> dict:
    canonical = json.dumps(list(records), sort_keys=True, ensure_ascii=False).encode("utf-8")
    return {
        "schema_version": "2.0",
        "record_count": len(records),
        "record_ids": [record["id"] for record in records],
        "record_types": sorted({record["type"] for record in records}),
        "sha256": hashlib.sha256(canonical).hexdigest(),
    }


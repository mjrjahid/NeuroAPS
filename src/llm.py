"""Optional external synthesis over public KB excerpts only."""

from __future__ import annotations

import json
import os
import urllib.request
from typing import Sequence

from .knowledge_base import RetrievalHit


def external_llm_available() -> bool:
    return bool(os.getenv("ANTHROPIC_API_KEY")) and os.getenv("ALLOW_EXTERNAL_LLM", "false").lower() == "true"


def synthesize_public_evidence(query: str, hits: Sequence[RetrievalHit]) -> str:
    """Send only characterized public-text excerpts after explicit local enablement."""

    if not external_llm_available():
        raise RuntimeError("External LLM mode is not enabled by the local administrator")
    if not hits:
        return "No relevant evidence was found in the current knowledge base."

    context = "\n\n".join(
        f"[{number}] {hit.title} | chunk {hit.chunk_id}\n{hit.text}"
        for number, hit in enumerate(hits, start=1)
    )
    prompt = (
        "You are a research knowledge assistant for an AI-ready neuroimaging use case in Saudi Arabia. "
        "Answer only from the supplied public knowledge-base excerpts. Cite claims with bracketed source "
        "numbers such as [1]. Separate established evidence, proposed application design, and limitations. "
        "Never produce a clinical diagnosis or invent a model prediction. If evidence is missing, say so.\n\n"
        f"QUESTION:\n{query}\n\nPUBLIC EVIDENCE:\n{context}"
    )
    body = json.dumps({
        "model": os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
        "max_tokens": 700,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")
    request = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-api-key": os.environ["ANTHROPIC_API_KEY"],
            "anthropic-version": "2023-06-01",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read())
    return payload["content"][0]["text"]


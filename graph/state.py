"""Estado compartilhado que flui pelo grafo LangGraph (Agentes A -> B -> C)."""
from __future__ import annotations

from typing import TypedDict


class ResearchState(TypedDict, total=False):
    topic: str        # entrada
    findings: str     # produzido pelo Agente A
    summary: str      # produzido pelo Agente B
    report: str       # produzido pelo Agente C

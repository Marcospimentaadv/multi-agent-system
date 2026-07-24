"""Agente B — Resumidor. Sintetiza os achados do Agente A."""
from __future__ import annotations

from config import get_llm

_PROMPT = """Você é um analista. Resuma os achados de pesquisa abaixo sobre "{topic}" \
em um sumário claro e conciso.

Estruture como:
- 3 a 5 pontos-chave (bullet points)
- 1 parágrafo de contexto geral

Achados:
{findings}
"""


def run_summary(topic: str, findings: str) -> str:
    """Retorna um resumo estruturado (Agente B)."""
    llm = get_llm(temperature=0.3)
    return llm.invoke(_PROMPT.format(topic=topic, findings=findings)).content

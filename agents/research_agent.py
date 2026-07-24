"""Agente A — Pesquisador. Busca na internet e coleta achados sobre um tema."""
from __future__ import annotations

from config import get_llm
from tools.web_tools import web_search, format_results

_PROMPT = """Você é um pesquisador. Com base nos resultados de busca abaixo sobre o \
tema "{topic}", extraia os achados factuais mais relevantes.

Liste de 5 a 10 achados objetivos, cada um com uma frase, citando a fonte (URL) \
quando possível. Não opine; apenas relate.

Resultados de busca:
{results}
"""


def run_research(topic: str) -> str:
    """Retorna um texto com os achados de pesquisa (Agente A)."""
    llm = get_llm(temperature=0.2)
    results = web_search(topic, max_results=8)
    prompt = _PROMPT.format(topic=topic, results=format_results(results))
    findings = llm.invoke(prompt).content
    return findings

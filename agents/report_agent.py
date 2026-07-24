"""Agente C — Redator. Formata um relatório final em Markdown."""
from __future__ import annotations

from datetime import date

from config import get_llm

_PROMPT = """Você é um redator técnico. Produza um RELATÓRIO final em Markdown sobre \
"{topic}", usando o resumo abaixo.

O relatório deve conter:
# Título
Data: {today}

## Resumo executivo
## Principais achados
## Análise
## Conclusão

Seja objetivo e profissional. Use apenas as informações fornecidas.

Resumo:
{summary}
"""


def run_report(topic: str, summary: str) -> str:
    """Retorna o relatório final formatado em Markdown (Agente C)."""
    llm = get_llm(temperature=0.4)
    prompt = _PROMPT.format(topic=topic, summary=summary, today=date.today().isoformat())
    return llm.invoke(prompt).content

"""Busca na web usando DuckDuckGo (sem necessidade de API key)."""
from __future__ import annotations

from duckduckgo_search import DDGS


def web_search(query: str, max_results: int = 6) -> list[dict]:
    """Retorna uma lista de resultados: {title, href, body}."""
    results: list[dict] = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append(
                {
                    "title": r.get("title", ""),
                    "href": r.get("href", ""),
                    "body": r.get("body", ""),
                }
            )
    return results


def format_results(results: list[dict]) -> str:
    """Formata resultados de busca em texto para o LLM consumir."""
    if not results:
        return "Nenhum resultado encontrado."
    lines = []
    for i, r in enumerate(results, start=1):
        lines.append(f"{i}. {r['title']}\n   {r['href']}\n   {r['body']}")
    return "\n\n".join(lines)

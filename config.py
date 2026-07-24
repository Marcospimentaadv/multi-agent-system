"""Configuração central: carrega variáveis de ambiente e cria o cliente do LLM."""
from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()

DEFAULT_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")


def _require_api_key() -> str:
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY não definida. Copie .env.example para .env "
            "e preencha sua chave da Anthropic."
        )
    return key


@lru_cache(maxsize=None)
def get_llm(temperature: float = 0.2, model: str | None = None) -> ChatAnthropic:
    """Retorna um cliente ChatAnthropic reutilizável (cacheado por parâmetros)."""
    _require_api_key()
    return ChatAnthropic(
        model=model or DEFAULT_MODEL,
        temperature=temperature,
        max_tokens=4096,
    )

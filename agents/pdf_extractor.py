"""Agente que lê um PDF longo, extrai campos específicos e preenche uma planilha."""
from __future__ import annotations

import json
from pathlib import Path

from config import get_llm
from tools.pdf_tools import extract_text, chunk_text
from tools.spreadsheet_tools import write_rows

_EXTRACTION_PROMPT = """Você é um extrator de dados preciso. A partir do trecho de \
documento abaixo, extraia os seguintes campos: {fields}.

Regras:
- Responda SOMENTE com um objeto JSON válido, sem texto extra.
- Use exatamente as chaves fornecidas.
- Se um campo não aparecer neste trecho, use string vazia "".
- Não invente valores.

Trecho do documento:
\"\"\"
{chunk}
\"\"\"
"""

_MERGE_PROMPT = """Você recebeu extrações parciais (uma por trecho) do MESMO documento. \
Consolide em um único objeto JSON com os campos: {fields}.

Para cada campo, escolha o valor mais completo e correto entre as extrações; \
se houver conflito, prefira o mais específico. Responda SOMENTE com JSON válido.

Extrações parciais:
{partials}
"""


def _parse_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip().strip("`").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end != -1:
            return json.loads(text[start : end + 1])
        raise


def extract_pdf_to_spreadsheet(
    pdf_path: str | Path,
    fields: list[str],
    output_path: str | Path,
) -> Path:
    """Fluxo completo: PDF longo -> extração por chunk -> merge -> planilha."""
    llm = get_llm(temperature=0.0)
    full_text = extract_text(pdf_path)
    chunks = chunk_text(full_text)
    fields_str = ", ".join(fields)

    print(f"[pdf_extractor] {len(chunks)} trecho(s) a processar...")
    partials: list[dict] = []
    for i, chunk in enumerate(chunks, start=1):
        prompt = _EXTRACTION_PROMPT.format(fields=fields_str, chunk=chunk)
        resp = llm.invoke(prompt)
        try:
            partials.append(_parse_json(resp.content))
        except Exception as e:  # noqa: BLE001
            print(f"[pdf_extractor] aviso: trecho {i} não retornou JSON válido ({e})")
        print(f"[pdf_extractor] trecho {i}/{len(chunks)} ok")

    if not partials:
        raise RuntimeError("Nenhuma extração válida foi obtida do PDF.")

    if len(partials) == 1:
        merged = partials[0]
    else:
        merge_prompt = _MERGE_PROMPT.format(
            fields=fields_str,
            partials=json.dumps(partials, ensure_ascii=False, indent=2),
        )
        merged = _parse_json(llm.invoke(merge_prompt).content)

    row = {f: merged.get(f, "") for f in fields}
    out = write_rows(output_path, fields, [row])
    print(f"[pdf_extractor] planilha salva em: {out}")
    return out

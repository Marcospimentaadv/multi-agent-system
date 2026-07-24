"""Utilitários para ler PDFs longos e dividir em pedaços (chunks)."""
from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader


def extract_text(pdf_path: str | Path) -> str:
    """Extrai todo o texto de um PDF, página por página."""
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")

    reader = PdfReader(str(pdf_path))
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(f"[página {i}]\n{text}")
    return "\n\n".join(pages)


def chunk_text(text: str, max_chars: int = 12000, overlap: int = 500) -> list[str]:
    """Divide texto longo em pedaços com sobreposição para não perder contexto."""
    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks

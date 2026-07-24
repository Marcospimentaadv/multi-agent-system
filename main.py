"""CLI do sistema multi-agente.

Exemplos:
  python main.py pdf --input data/input/doc.pdf --output data/output/dados.xlsx \
      --fields "nome,data,valor total"
  python main.py research --topic "IA generativa em 2025" \
      --output data/output/relatorio.md
"""
from __future__ import annotations

import argparse
from pathlib import Path


def cmd_pdf(args: argparse.Namespace) -> None:
    from agents.pdf_extractor import extract_pdf_to_spreadsheet

    fields = [f.strip() for f in args.fields.split(",") if f.strip()]
    extract_pdf_to_spreadsheet(args.input, fields, args.output)


def cmd_research(args: argparse.Namespace) -> None:
    from graph.workflow import run_research_pipeline

    report = run_research_pipeline(args.topic)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"[main] relatório salvo em: {out}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sistema multi-agente (Claude + LangGraph)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_pdf = sub.add_parser("pdf", help="Extrair campos de um PDF para planilha")
    p_pdf.add_argument("--input", required=True, help="Caminho do PDF de entrada")
    p_pdf.add_argument("--output", required=True, help="Caminho do .xlsx de saída")
    p_pdf.add_argument("--fields", required=True, help="Campos separados por vírgula")
    p_pdf.set_defaults(func=cmd_pdf)

    p_res = sub.add_parser("research", help="Rodar pipeline A->B->C")
    p_res.add_argument("--topic", required=True, help="Tema da pesquisa")
    p_res.add_argument("--output", default="data/output/relatorio.md", help="Arquivo .md de saída")
    p_res.set_defaults(func=cmd_research)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

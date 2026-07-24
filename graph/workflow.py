"""Orquestração LangGraph: Agente A (pesquisa) -> B (resumo) -> C (relatório)."""
from __future__ import annotations

from langgraph.graph import StateGraph, START, END

from agents.research_agent import run_research
from agents.summarizer_agent import run_summary
from agents.report_agent import run_report
from graph.state import ResearchState


def _node_research(state: ResearchState) -> ResearchState:
    print("[Agente A] pesquisando na internet...")
    return {"findings": run_research(state["topic"])}


def _node_summary(state: ResearchState) -> ResearchState:
    print("[Agente B] resumindo os achados...")
    return {"summary": run_summary(state["topic"], state["findings"])}


def _node_report(state: ResearchState) -> ResearchState:
    print("[Agente C] formatando o relatório...")
    return {"report": run_report(state["topic"], state["summary"])}


def build_graph():
    """Constrói e compila o grafo A -> B -> C."""
    graph = StateGraph(ResearchState)
    graph.add_node("research", _node_research)
    graph.add_node("summarize", _node_summary)
    graph.add_node("report", _node_report)

    graph.add_edge(START, "research")
    graph.add_edge("research", "summarize")
    graph.add_edge("summarize", "report")
    graph.add_edge("report", END)

    return graph.compile()


def run_research_pipeline(topic: str) -> str:
    """Executa o pipeline completo e retorna o relatório final (Markdown)."""
    app = build_graph()
    result = app.invoke({"topic": topic})
    return result["report"]

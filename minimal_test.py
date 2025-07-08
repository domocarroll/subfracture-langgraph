#!/usr/bin/env python3
"""
Ultra-minimal LangGraph test for server startup debugging
"""

from langgraph.graph import StateGraph, START, END

def simple_node(state: dict) -> dict:
    """Ultra-simple synchronous node"""
    return {"output": f"Processed: {state.get('input', 'test')}"}

# Create ultra-minimal workflow with basic dict state
workflow = StateGraph(dict)
workflow.add_node("process", simple_node)
workflow.add_edge(START, "process")
workflow.add_edge("process", END)

# Export for platform
try:
    graph = workflow.compile()
    print("✅ Ultra-minimal graph compiled successfully")
except Exception as e:
    print(f"❌ Graph compilation failed: {e}")
    # Fallback to simplest possible graph
    fallback_workflow = StateGraph(dict)
    fallback_workflow.add_node("simple", lambda state: {"result": "ok"})
    fallback_workflow.add_edge(START, "simple")
    fallback_workflow.add_edge("simple", END)
    graph = fallback_workflow.compile()
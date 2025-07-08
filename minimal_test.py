#!/usr/bin/env python3
"""
Minimal LangGraph test to isolate deployment issues
"""

from typing import TypedDict, Optional, Dict, Any
from langgraph.graph import StateGraph, START, END

class MinimalState(TypedDict):
    input: str
    output: Optional[str]

async def simple_node(state: MinimalState) -> MinimalState:
    """Simple test node"""
    return {"output": f"Processed: {state['input']}"}

# Create minimal workflow
workflow = StateGraph(MinimalState)
workflow.add_node("process", simple_node)
workflow.add_edge(START, "process")
workflow.add_edge("process", END)

# Export for platform
graph = workflow.compile()
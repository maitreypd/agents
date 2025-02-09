from langgraph.constants import START, END
from langgraph.graph import StateGraph, MessagesState

from graph.graph_actions import GraphActions
from tools.tool_manager import ToolManager


class GraphManager:
    @staticmethod
    def build_graph() -> StateGraph:
        builder = StateGraph(MessagesState)
        builder.add_node("agent", GraphActions.call_model)
        builder.add_node("tools", ToolManager.tool_node)
        builder.add_node("user_input", GraphActions.user_input_node)
        builder.add_node("final", GraphActions.call_final_model)
        builder.add_node("summary", GraphActions.call_model_summarise)
        builder.add_edge(START, "agent")
        builder.add_conditional_edges("agent", GraphActions.tool_or_agent)
        builder.add_edge("tools", "summary")
        builder.add_edge("summary", "user_input")
        builder.add_conditional_edges("user_input", GraphActions.user_confirmation_edge)
        builder.add_edge("final", END)
        return builder.compile(debug=True)
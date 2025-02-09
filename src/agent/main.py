from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from graph.graph_manager import GraphManager
from models.chat_models import ChatModels
from tools.tool_manager import ToolManager
import chainlit as cl


# Bind the Spotify tools so that the agent can call them.
ChatModels.model = ChatModels.model.bind_tools(ToolManager.tools)
ChatModels.final_model = ChatModels.final_model.with_config(tags=["final_node"])
graph = GraphManager.build_graph()

@cl.on_chat_start
async def main():
    await cl.Message(content=f"Hello, I am your Spotify assistant. "
                             f"You can create a playlist, search tracks and "
                             f"add tracks to the playlist..").send()

@cl.on_message
async def on_message(msg: cl.Message):
    config = {"configurable": {"thread_id": cl.context.session.id}}
    final_answer = cl.Message(content="")

    async for message, metadata in graph.astream(
        {"messages": [HumanMessage(content=msg.content)]},
        stream_mode="messages",
        config=RunnableConfig(**config)
    ):
        if (message.content and not isinstance(message, HumanMessage)
                and metadata["langgraph_node"] == "final"):
            await final_answer.stream_token(message.content)
    await final_answer.send()
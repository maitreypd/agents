from typing import Literal
import chainlit as cl
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import MessagesState

from models.chat_models import ChatModels
from tools.tool_manager import ToolManager


class GraphActions:
    @staticmethod
    async def user_input_node(state: MessagesState):
        user_input = await cl.AskUserMessage(content="Do you want to perform any other action?", timeout=200).send()
        res: str = user_input["output"]
        state["messages"].append(HumanMessage(res))
        return {"messages": state["messages"]}

    @staticmethod
    async def user_confirmation_edge(state: MessagesState) -> Literal["agent", "final"]:
        messages = state["messages"]
        last_message = messages[-1].content
        if "yes" in last_message:
            return "agent"
        else:
            return "final"

    @staticmethod
    async def tool_or_agent(state: MessagesState) -> Literal["tools", "agent"]:
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return "agent"

    @staticmethod
    async def call_model(state: MessagesState):
        messages = state["messages"]
        prompt = f"""
            Based on user input and current conversation history, think about the next action.
            User input: {messages}
            Available tools: {[t.name + ': ' + t.description for t in ToolManager.tools]}
            Decide:
            1. Whether a tool is needed
            2. If needed, which tool to use
            3. What parameters to call the tool with
            **Rules:**
                - Focus on latest instructions from User and utilize previous answers for history and context. 
                - Use track uri in this format from previous messages spotify:track:sometrackid 
                - Do not add tracks to the playlist until user asks it explicitly. 
            """
        response = await ChatModels.model.ainvoke(prompt)
        return {"messages": [response]}

    @staticmethod
    async def call_model_summarise(state: MessagesState):
        messages = state["messages"]
        prompt = f"""
            list track names or playlist name and what action you took. 
            Example 1  
            Here are the tracks:
            Track 1
            Track 2
            Example 2
            Playlist myplaylist created.
            Keep the track uri and playlist id in memory. 
            User input: {messages}
            **Rules** 
                £xtract track URI or playlist id as returned by the Spotify API call.
                Track URI is in this format. URI: spotify:track:sometrackid 
                When you create a playlist, it returns a playlist id. Extract it.
            """
        last_ai_message = messages[-1]
        response = await ChatModels.model.ainvoke(prompt)
        response.id = last_ai_message.id
        summary_answer = cl.Message(content="")
        await summary_answer.stream_token(response.content)
        await summary_answer.send()
        return {"messages": [response]}

    @staticmethod
    async def call_final_model(state: MessagesState):
        messages = state["messages"]
        last_ai_message = messages[-1]
        all_messages = [SystemMessage(f"Rewrite the answer concisely in simple language. "
                          f"Include the information user desired and how you arrived at the solution. ")]
        all_messages.extend([f"{type(m)}: {m.content}" for m in messages])
        response = await ChatModels.final_model.ainvoke(
            all_messages
        )
        response.id = last_ai_message.id
        final_answer = cl.Message(content="")
        await final_answer.stream_token(response.content)
        await final_answer.send()
        return {"messages": [response]}
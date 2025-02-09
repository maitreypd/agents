from langchain_openai import ChatOpenAI

from config.config import openai_key, gpt_model


class ChatModels:
    model = ChatOpenAI(model_name=gpt_model, api_key=openai_key)
    model_summarise = ChatOpenAI(model_name=gpt_model, api_key=openai_key)
    final_model = ChatOpenAI(model_name=gpt_model, api_key=openai_key)
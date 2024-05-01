from langchain.chat_models import ChatOpenAI


def build_llm(chat_args, model_name):
    return ChatOpenAI(
        streaming=True, 
        model_name=model_name
    )

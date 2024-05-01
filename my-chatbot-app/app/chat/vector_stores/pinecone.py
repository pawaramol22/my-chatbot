import os
import pinecone
from langchain.vectorstores.pinecone import Pinecone
from app.chat.embeddings.openai import embeddings


text_field = "text"

pc = pinecone.Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index = pc.Index(name=os.getenv("PINECONE_INDEX_NAME"), host=os.getenv("PINECONE_CONTROLLER_HOST"))

vector_store = Pinecone(
    index, embeddings, text_field
)

def build_retriever(chat_args, k):
    search_kwargs = {
        "filter": { "pdf_id": chat_args.pdf_id },
        "k": k
        }
    return vector_store.as_retriever(
        search_kwargs=search_kwargs
    )
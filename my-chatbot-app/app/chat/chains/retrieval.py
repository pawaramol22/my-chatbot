from langchain.chains import ConversationalRetrievalChain
from app.chat.chains.streamable import StremableChain
from app.chat.chains.traceable import TraceableChain


class StreamingConversationalRetrivalChain(
    TraceableChain, StremableChain, ConversationalRetrievalChain
):
    pass


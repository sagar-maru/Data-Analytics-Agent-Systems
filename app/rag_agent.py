import os
import hashlib
import pandas as pd
from typing import List, Dict
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document

# Constants
EMBEDDING_DIR = "data\embeddings"
os.makedirs(EMBEDDING_DIR, exist_ok=True)

# Initialize global components
llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
embedding = OpenAIEmbeddings()
retriever_chain = None

def get_embedding_path(text: str) -> str:
    """Create a hash-based path for storing FAISS index based on text content."""
    text_hash = hashlib.md5(text.encode()).hexdigest()
    return os.path.join(EMBEDDING_DIR, f"{text_hash}.faiss")

def create_rag_chain(text: str):
    global retriever_chain

    index_path = get_embedding_path(text)

    if os.path.exists(index_path):
        # Load existing FAISS index
        vectorstore = FAISS.load_local(index_path, embeddings=embedding, allow_dangerous_deserialization=True)
        print(f"✅ Loaded cached embeddings from: {index_path}")
    else:
        # Generate and store FAISS index
        docs = [Document(page_content=text)]
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        split_docs = text_splitter.split_documents(docs)
        vectorstore = FAISS.from_documents(split_docs, embedding)
        vectorstore.save_local(index_path)
        print(f"💾 Saved new embeddings to: {index_path}")

    retriever_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())

def update_rag_doc_context(text: str):
    """Update the RAG agent with new textual content."""
    create_rag_chain(text)

def query_rag(messages: List[Dict[str, str]]) -> str:
    """
    Accepts a list of messages with roles and content.
    Concatenates last 5 messages (user + assistant) as context.
    Sends to retriever_chain.run() as a single string query.
    """
    if retriever_chain is None:
        return "No context loaded for RAG agent."

    # Build a combined string prompt from roles and content
    # For example: "User: ... Assistant: ..."
    combined_query = "\n".join(
        f"{msg['role'].capitalize()}: {msg['content']}" for msg in messages
    )

    # Send combined string to the retriever_chain
    return retriever_chain.run(combined_query)

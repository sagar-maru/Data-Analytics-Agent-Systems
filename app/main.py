import pandas as pd
from fastapi import FastAPI, Body, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import time
import os
from app.config import SECRET_ID, SECRET_KEY, TOKEN_STORE, generate_bearer_token
from app.auth import verify_token
# from app.auth import router as auth_router
from app.llm_agent import query_data_analytics, update_dataframe
from app.rag_agent import query_rag, update_rag_doc_context
from app.sql_agent import query_sql_data, update_sql_database
import logging

logger = logging.getLogger("uvicorn.error")

app = FastAPI()
# app.include_router(auth_router)

# === Data Models ===
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class DataFrameUpdateRequest(BaseModel):
    data: str

class ContextQuery(BaseModel):
    question: str

class ContextData(BaseModel):
    text: str

class SQLQueryRequest(BaseModel):
    messages: List[ChatMessage]

class SQLUpdateRequest(BaseModel):
    db_uri: str  # Format: "sqlite:///path/to/your.db"

class AuthRequest(BaseModel):
    secret_id: str
    secret_key: str

@app.post("/auth/token")
def auth_token(payload: AuthRequest):
    if payload.secret_id != SECRET_ID or payload.secret_key != SECRET_KEY:
        return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})

    current_time = time.time()

    # If existing token is still valid
    if TOKEN_STORE["token"] and TOKEN_STORE["expires_at"] > current_time:
        remaining = int(TOKEN_STORE["expires_at"] - current_time)
        return {"access_token": TOKEN_STORE["token"], "expires_in": remaining}

    # Generate new token
    token = generate_bearer_token()
    return {"access_token": token, "expires_in": 360}

# === LLM Chat Endpoints ===
@app.post("/chat", dependencies=[Depends(verify_token)])
def chat(payload: ChatRequest):
    messages = payload.messages
    return {"response": query_data_analytics(messages)}

@app.post("/update-df", dependencies=[Depends(verify_token)])
def update_df(request: DataFrameUpdateRequest):
    df = pd.read_json(request.data, orient="split")
    update_dataframe(df)
    return {"status": "Dataframe data updated successfully."}

# === RAG Endpoints ===
@app.post("/context", dependencies=[Depends(verify_token)])
def context_chat(payload: ChatRequest):
    messages = payload.messages
    formatted_messages = [{"role": msg.role, "content": msg.content} for msg in messages]
    return {"response": query_rag(formatted_messages)}

@app.post("/update-context", dependencies=[Depends(verify_token)])
def update_context_data(data: ContextData):
    update_rag_doc_context(data.text)
    return {"message": "Context data updated successfully."}

# === SQL Agent Endpoints ===
@app.post("/sql", dependencies=[Depends(verify_token)])
def sql_chat(payload: SQLQueryRequest):
    messages = payload.messages
    return {"response": query_sql_data(messages)}

@app.post("/update-sql", dependencies=[Depends(verify_token)])
def update_sql(request: SQLUpdateRequest):
    update_sql_database(request.db_uri)
    return {"message": f"SQL database updated to: {request.db_uri}"}

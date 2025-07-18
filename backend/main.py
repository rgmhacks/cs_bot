# backend/main.py
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from rag import RAGAgent
from contextlib import ExitStack
from langgraph.checkpoint.mongodb import MongoDBSaver


stack = ExitStack()
memory = stack.enter_context(MongoDBSaver.from_conn_string(os.getenv("DB_URI")))

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG agent
# Update the index_name to match your Pinecone index
rag_agent = RAGAgent(memory)

@app.get("/")
async def root():
    return {"message": "Dream11 CS Bot with RAG backend running."}

@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    user_input = body.get("message")
    session_id = body.get("session_id")
    print("chat",session_id)
    
    if not user_input:
        return {"reply": "Please provide a message."}
    
    try:
        response = rag_agent.get_response(user_input,session_id)
        return response
    except Exception as e:
        return {"reply": f"Sorry, I encountered an error: {str(e)}"}
    
@app.post("/api/chat_resume")
async def chat_resume(request: Request):
    body = await request.json()
    user_input = body.get("message")
    session_id = body.get("session_id")
    print("resume",session_id)
    
    if not user_input:
        return {"reply": "Please provide a message."}
    
    try:
        response = rag_agent.resume_chat(user_input,session_id)
        return response
    except Exception as e:
        return {"reply": f"Sorry, I encountered an error: {str(e)}"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "rag_agent": "initialized"}

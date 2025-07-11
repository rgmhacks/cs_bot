# backend/main.py
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from rag_agent import RAGAgent

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
rag_agent = RAGAgent()

@app.get("/")
async def root():
    return {"message": "Dream11 CS Bot with RAG backend running."}

@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    user_input = body.get("message")
    
    if not user_input:
        return {"reply": "Please provide a message."}
    
    try:
        # Get RAG-based response
        response = rag_agent.get_response(user_input,"1324")
        return {"reply": response}
    except Exception as e:
        return {"reply": f"Sorry, I encountered an error: {str(e)}"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "rag_agent": "initialized"}

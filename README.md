# RAG-Based Chatbot with Pinecone

A Retrieval-Augmented Generation (RAG) chatbot that uses Pinecone as the vector database.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create a `.env` file with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   PINECONE_ENVIRONMENT=your_pinecone_environment_here
   GOOGLE_API_KEY=your_google_api_key_here
   DB_URI=your_database_uri_here
   ```

3. **Run the Server**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

## API Endpoints

- `GET /` - Health check
- `GET /api/health` - Detailed health status
- `POST /api/chat` - Chat endpoint
  ```json
  {
    "message": "Your question here"
  }
  ```

## How it Works

1. User sends a question via the `/api/chat` endpoint
2. The RAG agent retrieves relevant documents from Pinecone using semantic search
3. Retrieved documents are formatted as context
4. The LLM generates a response based on the context and user question
5. Response is returned to the user

## Customization

- Modify the system prompt in `rag_agent.py`
- Change the number of retrieved documents (`k` parameter)
- Update the LLM model or temperature settings

## Workflow
<img width="379" height="925" alt="image" src="https://github.com/user-attachments/assets/213a56fa-b638-42f4-bb77-83ed38a15bae" />


import os
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Import the RAG logic from the app package
from app.pipeline import ask_question

# Load environment variables (for local dev)
load_dotenv()

app = FastAPI(
    title="HR Policy RAG API",
    description="API for querying company policies using RAG",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]
    latency_ms: float

@app.get("/health")
def health_check():
    """
    Health check endpoint.
    Returns simple status via JSON as required by the project rubric.
    """
    return {"status": "healthy", "service": "rag-policy-engine"}

@app.post("/chat", response_model=QueryResponse)
def chat_endpoint(req: QueryRequest):
    """
    Chat endpoint.
    Receives user questions (POST) and returns model-generated answers 
    with citations and snippets.
    """
    start_time = time.time()
    
    # Ensure Groq API key is available
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured on server.")
    
    try:
        # Call the RAG pipeline
        result = ask_question(req.question)
        
        # Calculate latency
        latency_ms = round((time.time() - start_time) * 1000, 2)
        
        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "latency_ms": latency_ms
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Run locally if executed directly
    uvicorn.run(app, host="0.0.0.0", port=8000)
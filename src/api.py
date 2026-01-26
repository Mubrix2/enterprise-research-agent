from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.main import start_research
import threading

app = FastAPI(title="Enterprise Research API")

class ResearchRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"status": "Research API is online"}

@app.post("/research")
async def perform_research(request: ResearchRequest):
    try:
        # We run this as a background task or return the agent's final answer
        # For now, we'll let the agent run and return a success message
        # In a real app, you'd use a WebSocket or a Task Queue (like Celery)
        result = start_research(request.query)
        return {"status": "complete", "query": request.query, "message": "Research finished. Check logs for details."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
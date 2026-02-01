import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.main import start_research

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/research")
async def research_endpoint(request: QueryRequest):
    try:
        # Calls the agent orchestration in main.py
        answer = start_research(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="127.0.0.1",  # Change this from "0.0.0.0" to "127.0.0.1"
        port=8000,
        log_level="info"
    )
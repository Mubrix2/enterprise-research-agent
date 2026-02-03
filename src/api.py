import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.main import start_research # This works if PYTHONPATH=/app

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"status": "online", "message": "Research API is running"}

@app.post("/research")
async def research_endpoint(request: QueryRequest):
    try:
        answer = start_research(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
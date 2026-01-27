from fastapi import FastAPI
from pydantic import BaseModel
from src.main import start_research

app = FastAPI()

class RequestBody(BaseModel):
    query: str

@app.post("/research")
async def research_endpoint(data: RequestBody):
    # This calls our agent logic
    answer = start_research(data.query)
    # Clean up the 'TERMINATE' string from the UI output
    clean_answer = answer.replace("TERMINATE", "").strip()
    return {"answer": clean_answer}
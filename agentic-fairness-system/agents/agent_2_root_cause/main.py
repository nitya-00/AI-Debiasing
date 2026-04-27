# Placeholder for agent 2 root cause analysis service
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "healthy", "agent": "root_cause_analysis"}

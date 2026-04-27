# Placeholder for agent 5 monitoring service
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "healthy", "agent": "monitoring"}

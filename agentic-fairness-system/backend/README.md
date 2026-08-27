# Python backend

This is the small FastAPI backend for the fairness console. It serves the frontend from the same process and keeps workflows in memory for now.

From this directory:

```bash
python3 -m pip install -r requirements.txt
python3 -m uvicorn main:app --reload --port 8080
```

Open http://localhost:8080. The API is available at `/api/health` and `/api/workflows`.

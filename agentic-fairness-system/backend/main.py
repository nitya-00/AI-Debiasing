from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field


class CreateWorkflowRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(min_length=1)
    protected_attributes: list[str] = Field(
        min_length=1, alias="protectedAttributes"
    )
    target_column: str = Field(min_length=1, alias="targetColumn")


class Workflow(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: UUID
    name: str
    protected_attributes: list[str] = Field(alias="protectedAttributes")
    target_column: str = Field(alias="targetColumn")
    status: str
    created_at: datetime = Field(alias="createdAt")


app = FastAPI(title="Agentic AI Fairness System", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

workflows: dict[UUID, Workflow] = {}
workflows_lock = Lock()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "healthy", "service": "agentic-fairness-system"}


@app.get("/api/workflows", response_model=list[Workflow])
def list_workflows() -> list[Workflow]:
    with workflows_lock:
        return list(workflows.values())


@app.get("/api/workflows/{workflow_id}", response_model=Workflow)
def get_workflow(workflow_id: UUID) -> Workflow:
    with workflows_lock:
        workflow = workflows.get(workflow_id)
    if workflow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    return workflow


@app.post("/api/workflows", response_model=Workflow, status_code=status.HTTP_201_CREATED)
def create_workflow(request: CreateWorkflowRequest) -> Workflow:
    workflow = Workflow(
        id=uuid4(),
        name=request.name.strip(),
        protectedAttributes=[item.strip() for item in request.protected_attributes if item.strip()],
        targetColumn=request.target_column.strip(),
        status="PENDING",
        createdAt=datetime.now(timezone.utc),
    )
    if not workflow.protected_attributes or not workflow.target_column:
        raise HTTPException(status_code=422, detail="Workflow fields cannot be empty")
    with workflows_lock:
        workflows[workflow.id] = workflow
    return workflow


static_directory = Path(__file__).parent / "src" / "main" / "resources" / "static"
app.mount("/", StaticFiles(directory=static_directory, html=True), name="frontend")

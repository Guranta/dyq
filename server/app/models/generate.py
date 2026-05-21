from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class GenerationType(StrEnum):
    image = "image"
    video = "video"


class GenerationMode(StrEnum):
    text_to_image = "text_to_image"
    image_to_image = "image_to_image"
    text_to_video = "text_to_video"
    image_to_video = "image_to_video"


class TaskStatus(StrEnum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class EstimateRequest(BaseModel):
    type: GenerationType
    mode: GenerationMode
    count: int = Field(default=1, ge=1, le=8)
    duration: int = Field(default=5, ge=1, le=30)


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    mode: GenerationMode
    ratio: str = "9:16"
    resolution: str = "720p"
    duration: int = Field(default=5, ge=1, le=30)
    count: int = Field(default=1, ge=1, le=8)
    negative_prompt: str | None = None
    asset_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class GeneratedAsset(BaseModel):
    id: str
    type: GenerationType
    url: str
    mime_type: str


class TaskRecord(BaseModel):
    id: str
    status: TaskStatus
    type: GenerationType
    mode: GenerationMode
    prompt: str
    provider: str
    model: str
    cost: int
    progress: int = 0
    results: list[GeneratedAsset] = Field(default_factory=list)
    error: str | None = None
    raw_response: dict[str, Any] = Field(default_factory=dict)


class GenerateResponse(BaseModel):
    task_id: str
    status: TaskStatus
    cost: int
    provider: str
    model: str
    poll_url: str
    results: list[GeneratedAsset] = Field(default_factory=list)
    error: str | None = None

    @classmethod
    def from_task(cls, task: TaskRecord) -> "GenerateResponse":
        return cls(
            task_id=task.id,
            status=task.status,
            cost=task.cost,
            provider=task.provider,
            model=task.model,
            poll_url=f"/api/v1/tasks/{task.id}",
            results=task.results,
            error=task.error,
        )


class TaskResponse(BaseModel):
    id: str
    status: TaskStatus
    type: GenerationType
    mode: GenerationMode
    progress: int
    provider: str
    model: str
    results: list[GeneratedAsset]
    cost: int
    error: str | None = None

    @classmethod
    def from_task(cls, task: TaskRecord) -> "TaskResponse":
        return cls(
            id=task.id,
            status=task.status,
            type=task.type,
            mode=task.mode,
            progress=task.progress,
            provider=task.provider,
            model=task.model,
            results=task.results,
            cost=task.cost,
            error=task.error,
        )

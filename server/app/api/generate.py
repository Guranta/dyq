from fastapi import APIRouter, HTTPException

from app.models.generate import EstimateRequest, GenerateRequest, GenerateResponse
from app.services.provider_manager import get_provider_manager
from app.services.task_store import task_store


router = APIRouter(prefix="/generate", tags=["generate"])


@router.post("/estimate")
async def estimate(request: EstimateRequest) -> dict[str, object]:
    manager = get_provider_manager()
    provider = manager.select_provider(request.type, request.mode)
    if provider is None:
        raise HTTPException(status_code=400, detail="No provider supports this generation type")
    cost = manager.estimate_cost(request.type, request.count, request.duration)
    return {
        "cost": cost,
        "estimated_time_seconds": provider.estimated_time_seconds(request.type),
        "selected_provider": provider.name,
        "selected_model": provider.model_for(request.type),
    }


@router.post("/image", response_model=GenerateResponse)
async def generate_image(request: GenerateRequest) -> GenerateResponse:
    manager = get_provider_manager()
    result = await manager.generate_image(request)
    task_store.save(result)
    return GenerateResponse.from_task(result)


@router.post("/video", response_model=GenerateResponse)
async def generate_video(request: GenerateRequest) -> GenerateResponse:
    manager = get_provider_manager()
    result = await manager.generate_video(request)
    task_store.save(result)
    return GenerateResponse.from_task(result)

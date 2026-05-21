from fastapi import APIRouter

from app.services.provider_manager import get_provider_manager


router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("")
async def list_providers() -> dict[str, list[dict[str, object]]]:
    manager = get_provider_manager()
    return {"items": [provider.public_info() for provider in manager.providers]}

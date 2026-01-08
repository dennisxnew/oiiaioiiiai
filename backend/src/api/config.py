from ..models.config import AppConfig
from ..services.config_service import get_app_config, save_app_config
from fastapi import APIRouter

router = APIRouter()

@router.get("/api/config", response_model=AppConfig)
async def get_config():
    """Retrieves the entire application configuration."""
    return get_app_config()

@router.put("/api/config", response_model=AppConfig)
async def update_config(new_config: AppConfig):
    """Updates the entire application configuration."""
    save_app_config(new_config)
    return new_config

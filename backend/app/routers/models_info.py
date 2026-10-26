"""
Models & Dataset Transparency router.
Reads directly from `models_saved/metadata.json` generated during training sessions.
Never hardcoded — dynamic computation from real data.
"""

from typing import Any, Dict
from fastapi import APIRouter
from backend.ml.metadata_manager import load_metadata

router = APIRouter(prefix="/models", tags=["Model & Dataset Transparency"])


@router.get("/info", response_model=Dict[str, Any])
def get_models_info():
    """
    Returns dynamically computed training metadata for all defensive ML models,
    including total datasets used, exact training record counts, feature dimensions,
    train/test splits, and full confusion matrices.
    """
    meta = load_metadata()
    return meta

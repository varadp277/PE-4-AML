"""
Metadata manager for model registries, evaluation metrics, and dataset auditing.
Zero hardcoding: all counts, metrics, and timestamps are computed dynamically from real datasets.
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger("ai_threat.metadata_manager")

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models_saved")
METADATA_FILE = os.path.join(MODELS_DIR, "metadata.json")

try:
    os.makedirs(MODELS_DIR, exist_ok=True)
except OSError:
    pass


def load_metadata() -> Dict[str, Any]:
    """Load existing metadata or return a fresh skeleton."""
    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, "r") as f:
                return json.load(f)
        except Exception as exc:
            logger.warning(f"Failed to read metadata.json: {exc}")

    return {
        "summary": {
            "total_datasets": 0,
            "total_records_trained_on": 0,
            "total_models_trained": 0,
            "last_updated": None
        },
        "models": {}
    }


def save_model_metadata(model_id: str, model_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Save or update metadata for a specific trained model, recalculating all global totals.
    Safe against read-only filesystems.
    """
    meta = load_metadata()
    meta["models"][model_id] = model_info

    # Dynamically compute global totals across all currently trained models
    unique_datasets = set()
    total_records = 0

    for m in meta["models"].values():
        dataset_name = m.get("dataset_name")
        if dataset_name:
            unique_datasets.add(dataset_name)
        total_records += int(m.get("num_records_trained", 0))

    meta["summary"] = {
        "total_datasets": len(unique_datasets),
        "total_records_trained_on": total_records,
        "total_models_trained": len(meta["models"]),
        "last_updated": datetime.now().isoformat()
    }

    try:
        with open(METADATA_FILE, "w") as f:
            json.dump(meta, f, indent=2)
    except OSError as exc:
        logger.warning(f"Could not persist metadata file (read-only filesystem): {exc}")

    return meta

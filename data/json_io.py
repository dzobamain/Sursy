# data/json_io.py

import json
import os
from typing import Any
from util.log import logger

def save_to_json(obj: Any, path: str) -> None:
    """
    Save any Python object (class instance or dict) to a JSON file.

    :param obj: Object to save. If it's a class instance, its __dict__ will be used.
    :param path: Path to the JSON file.
    """
    try:
        # Ensure the directory exists before saving
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Convert class object to dictionary if needed
        data: Any = obj.__dict__ if hasattr(obj, "__dict__") else obj

        # Write JSON file with indentation and UTF-8 encoding
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        logger.info(f"Saved JSON successfully to {path}")

    except Exception as e:
        logger.error(f"Failed to save JSON: {e}") 


def load_from_json(obj: Any, path: str) -> None:
    """
    Load data from a JSON file into an existing object.

    :param obj: The object whose attributes will be updated.
    :param path: Path to the JSON file.
    """
    try:
        # Check if the file exists
        if not os.path.exists(path):
            logger.warning(f"Settings file not found: {path}. Using defaults.")
            return

        # Read and parse JSON data
        with open(path, "r", encoding="utf-8") as f:
            data: dict[str, Any] = json.load(f)

        # Update object attributes if they exist
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        logger.info(f"Loaded JSON successfully from {path}")

    except Exception as e:
        logger.error(f"Failed to load JSON: {e}")


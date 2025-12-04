# data/json_io.py

import json
import os
from typing import Any
from util.log import logger

def save_to_json(obj: Any, path: str) -> bool:
    logger.debug("Enter")
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

    
def load_into_object(obj: Any, path: str) -> bool:
    """
    Load JSON into an existing object (`obj`) and return True if loaded.
    """
    try:
        if not os.path.exists(path):
            logger.warning(f"Settings file not found: {path}.")
            return False

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        logger.info(f"Loaded JSON successfully from {path}")
        return True

    except Exception as e:
        logger.error(f"Failed to load JSON: {e}")
        return False


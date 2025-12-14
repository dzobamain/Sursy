#config.py
import json
from pathlib import Path
from shutil import copy2
from util.log import logger

class Config:
    """
    Config class for managing program configuration files.
    This class provides methods to load and save JSON configuration files.
    """
    PROGRAM_CONFIG: str = "prconfig.json"

    def __init__(self) -> None:
        logger.info("Enter")
        
        self.prconfig = self.load_json(self.PROGRAM_CONFIG)
        if self.prconfig is None:
            logger.error("Failed to load program configuration.")
            self.prconfig = {}
        
        
    @staticmethod
    def load_json(file_path: str = PROGRAM_CONFIG) -> dict | None:
        path = Path(file_path)
        try:
            if not path.is_file():
                logger.warning(f"Settings file not found: {file_path}.")
                return None

            # Read
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
    
            logger.info(f"Loaded JSON successfully from {file_path}")
            return data
    
        except Exception as e:
            logger.error(f"Failed to load JSON: {e}")
            return None

    @staticmethod
    def save_json(data: dict, file_path: str = PROGRAM_CONFIG) -> None:
        # Save JSON to file with backup and log changes
        path = Path(file_path)
        backup_dir = Path("temp")
        backup_dir.mkdir(exist_ok=True)
        backup_path = backup_dir / path.name

        old_data = {}
        if path.is_file():
            try:
                with path.open("r", encoding="utf-8") as f:
                    old_data = json.load(f)
                copy2(path, backup_path)  # backup old config
            except Exception as e:
                logger.warning(f"Could not backup: {e}")

        # Save new data
        try:
            with path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save JSON: {e}")
            return

        # Compare old and new to log changes
        changes = Config._diff_dicts(old_data, data)
        if changes:
            for key_path, (old_val, new_val) in changes.items():
                logger.info(f"Changed {key_path}: {old_val} -> {new_val}")
        else:
            logger.info("Saved JSON with no changes.")

        logger.info(f"Saved JSON successfully to {file_path}")

    @staticmethod
    def _diff_dicts(old: dict, new: dict, parent_key="") -> dict:
        # Recursively find differences between two dicts
        changes = {}
        old_keys = set(old.keys())
        new_keys = set(new.keys())

        for key in old_keys | new_keys:
            full_key = f"{parent_key}.{key}" if parent_key else key
            old_val = old.get(key)
            new_val = new.get(key)

            if isinstance(old_val, dict) and isinstance(new_val, dict):
                changes.update(Config._diff_dicts(old_val, new_val, full_key))
            elif old_val != new_val:
                changes[full_key] = (old_val, new_val)

        return changes
    
    
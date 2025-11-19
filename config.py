# config.py
import json
from pathlib import Path
from util.log import logger

class Config:
    """
    Config class for managing program configuration files.

    This class provides methods to load and save JSON configuration files.
    """
    PROGRAM_CONFIG: str = "prconfig.json"
    SETTINGS_PATH: str = "data/settings.json"
    BROWSER_CONFIG: str = "browser/brconfig.json"
    GUI_CONFIG: str = "qt5ui/uiconfig.json"

    @classmethod
    def load_json(cls, file_path: str):
        """Load JSON config if it exists. Returns a dict or None."""
        path = Path(file_path)
        if not path.is_file():
            logger.warning(f"Configuration file {file_path} not found.")
            return None
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info(f"Configuration loaded successfully from {file_path}.")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in {file_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while reading {file_path}: {e}")
            return None

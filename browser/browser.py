#browser/browser.py
import sys
import os
import subprocess
import platform
from pathlib import Path
from util.log import logger
from config import Config

class Browser:
    def __init__(self) -> None:        
        logger.info("Enter")
        
        self.config = Config()
        
        if self.config.prconfig is None:
            logger.error("Failed to load program configuration.")
            self.config.program_config = {}
    
        if not self.is_browser_available(self.config.prconfig["browser"]["path"]):
            logger.debug("Browser executable not found or not accessible.")
            sys.exit(1)
    
    
    def is_browser_available(browser_path: str) -> bool:
        return os.path.isfile(browser_path) and os.access(browser_path, os.X_OK)
    
        
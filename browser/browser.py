#browser/browser.py
import sys
import os
import subprocess
import platform
from pathlib import Path
from util.log import logger
from config import Config
from qt5ui.error import ask_user

class Browser:
    def __init__(self) -> None:        
        logger.info("Enter")
        
        self.browser_status: bool = True
        self.config = Config()
        
        try:
            while self.browser_status:
                if self.is_browser_available(self.config.prconfig["browser"]["path"]):
                    break
                
                self.config.prconfig["browser"]["path"] = ask_user(
                    parent=None,
                    title="Browser Not Found",
                    message="The specified browser executable was not found or is not executable. Please provide a valid path."
                )
        except KeyError:
            logger.error("Browser path not found in configuration.")
        
        self.config.save_json(self.config.prconfig)
    
    
    def is_browser_available(self, browser_path: str) -> bool:
        return os.path.isfile(browser_path) and os.access(browser_path, os.X_OK)
    
    
    
        
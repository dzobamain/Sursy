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
        
        self.browser_status: bool = False
        self.config = Config()
        
        self.browser_status = self.verify_browser_path()
        self.config.save_json(self.config.prconfig)
    
    
    def verify_browser_path(self) -> bool:
        attempts = 2

        try:
            for _ in range(attempts):

                path = self.config.prconfig["browser"]["path"]

                if self.is_browser_available(path):
                    self.config.save_json(self.config.prconfig)
                    return True

                new_path = ask_user(
                    parent=None,
                    title="Browser Not Found",
                    message="The specified browser executable was not found or is not executable. Please provide a valid path."
                )

                self.config.prconfig["browser"]["path"] = new_path

        except KeyError:
            logger.error("Browser path not found in configuration.")
        return False
    
    
    def is_browser_available(self, browser_path: str) -> bool:
        return os.path.isfile(browser_path) and os.access(browser_path, os.X_OK)
    
    
    def open_in_one_window(browser: str, urls: list[str], window_args) -> None:
        # Opens all URLs in a single browser window.
        if not urls:
            return

        subprocess.Popen(
            [browser, *urls, *window_args],
            start_new_session=True,
            close_fds=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )


    def open_in_new_windows(browser: str, urls: list[str], window_args) -> None:
        # Opens each URL in a separate new browser window.
        for url in urls:
            subprocess.Popen(
                [browser, "--new-window", url, *window_args],
                start_new_session=True,
                close_fds=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            

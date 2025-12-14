#browser/browser.py
import os
import subprocess
from util.log import logger
from config import Config
from qt5ui.error import ask_user
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

class Browser:
    def __init__(self) -> None:        
        logger.info("Enter")
        
        self.config = Config()
    
    
    def verify_browser_path(self) -> bool:
        try:
            path = self.config.prconfig["browser"]["path"]

            if self.is_browser_available(path):
                return True

            new_path = ask_user(
                parent=None,
                title="Browser Not Found",
                message="The specified browser executable was not found or is not executable. Please provide a valid path."
            )

            if new_path and self.is_browser_available(new_path):
                self.config.prconfig["browser"]["path"] = new_path
                self.config.save_json(self.config.prconfig)
                return True

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
            
    def search_links(query: str, limit: int) -> list[str]:
        # Performs a search query and returns a list of links.
        urls: list[str] = []
        search_url = f"https://duckduckgo.com/html/?q={quote(query)}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for a in soup.select("a.result__a"):
            href = a.get("href")
            if href:
                urls.append(href)
            if len(urls) >= limit:
                break

        return urls


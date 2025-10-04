# test/subprocess.py

import sys
import os
import subprocess
import platform
from pathlib import Path

# List of test URLs
urls = [
    "https://example.com",
    "https://python.org",
    "https://news.ycombinator.com",
    # Next 3 URLs to open in new windows
    "https://wikipedia.org",
    "https://reddit.com",
    "https://twitter.com"
]

args=["--disable-background-networking",
      "--disable-default-apps",
      "--disable-extensions",
      "--disable-sync",
      "--no-first-run",
      "--disable-component-update",
      "--disable-client-side-phishing-detection",
      "--disable-popup-blocking"]

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
WINDOW_POSITION_X = 100
WINDOW_POSITION_Y = 100

def get_chrome_path():
    system = platform.system()
    if system == "Darwin":
        return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif system == "Windows":
        return r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    elif system == "Linux":
        return "/usr/bin/google-chrome"
    else:
        raise RuntimeError("Unsupported OS")

def open_urls():
    chrome_path = get_chrome_path()

    if not Path(chrome_path).exists():
        print(f"❌ Chrome not found at: {chrome_path}")
        return

    window_args = [
        f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}",
        "--disable-logging",
        "--log-level=3",
        "--no-first-run",
        "--no-default-browser-check",
    ]

    
    with open("var/brauser_launch.log", "w") as log_file:
        subprocess.Popen(
            [chrome_path, *urls[:2], *window_args],
            start_new_session=True,
            close_fds=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    for url in urls[2:]:
        subprocess.Popen([chrome_path, "--new-window", url, *window_args],
                         close_fds=True,
                         start_new_session=True)

    sys.exit(0)

if __name__ == "__main__":
    open_urls()

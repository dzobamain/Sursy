# util/log.py

import logging
import inspect
from typing import Optional

# Log levels and their meaning:
# DEBUG -> Detailed information, useful for debugging
# INFO -> General information about program execution
# WARNING -> Indication of potential problems
# ERROR -> Error messages, something went wrong
# CRITICAL -> Serious errors, program may not continue

class CustomFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        class_method: str = record.funcName
        try:
            # Get class through inspect
            frame: Optional[inspect.FrameType] = inspect.currentframe()
            while frame:
                if frame.f_code.co_name == record.funcName:
                    cls: Optional[object] = frame.f_locals.get('self', None)
                    if cls:
                        class_method = f"{type(cls).__name__}.{record.funcName}"
                        break
                frame = frame.f_back
        except Exception:
            pass

        if record.levelno == logging.INFO:
            self._style._fmt = f"[%(levelname)s][%(asctime)s][%(pathname)s] {class_method}: %(message)s"
        else:
            self._style._fmt = f"[%(levelname)s][%(asctime)s][%(pathname)s:%(lineno)d] {class_method}: %(message)s"
        return super().format(record)

# Global logger
logger: logging.Logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Toggles for output
ENABLE_FILE_LOG: bool = True  # set to False to disable file logging
ENABLE_CONSOLE_LOG: bool = False  # set to False to disable console logging

# Path to the log file
log_file_path: str = "var/app.log"

# File handler (only if enabled)
if ENABLE_FILE_LOG:
    file_handler: logging.FileHandler = logging.FileHandler(log_file_path, mode='w')
    file_handler.setFormatter(CustomFormatter())
    logger.addHandler(file_handler)

# Console handler (only if enabled)
if ENABLE_CONSOLE_LOG:
    console_handler: logging.StreamHandler = logging.StreamHandler()
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)


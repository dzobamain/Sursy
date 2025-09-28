# util/log.py

import logging

# Log levels and their meaning:
# DEBUG -> Detailed information, useful for debugging
# INFO -> General information about program execution
# WARNING -> Indication of potential problems
# ERROR -> Error messages, something went wrong
# CRITICAL -> Serious errors, program may not continue

class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            # INFO without line number
            self._style._fmt = "[%(levelname)s][%(asctime)s][%(pathname)s] %(funcName)s: %(message)s"
        else:
            # Other levels with line number
            self._style._fmt = "[%(levelname)s][%(asctime)s][%(pathname)s:%(lineno)d] %(funcName)s: %(message)s"
        return super().format(record)


# Global logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Toggles for output
ENABLE_FILE_LOG = True # set to False to disable file logging
ENABLE_CONSOLE_LOG = False  # set to False to disable console logging

# Path to the log file
log_file_path = "var/app.log"

# File handler (only if enabled)
if ENABLE_FILE_LOG:
    file_handler = logging.FileHandler(log_file_path, mode='w')
    file_handler.setFormatter(CustomFormatter())
    logger.addHandler(file_handler)

# Console handler (only if enabled)
if ENABLE_CONSOLE_LOG:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)

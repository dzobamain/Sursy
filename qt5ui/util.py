# qt5ui/util.py

from util.log import logger

def load_stylesheet(path) -> str:
    # Load a QSS/CSS stylesheet from a file and return it as a string.
    try:
        with open(path, "r", encoding="utf-8") as style:
            return style.read()
    except Exception as e:
        logger.error(f"Failed to load stylesheet: {e}")
        return ""

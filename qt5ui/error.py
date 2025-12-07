# util/error.py
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5.QtCore import Qt
from util.log import logger
from qt5ui.common import center_window

# Displays an error message box with optional details and actions.
def show_error(
    parent: QWidget,
    title: str,
    message: str,
    details: str = ""
):
    logger.warning(f"{title} — {message}")

    if details:
        logger.warning(f"DETAILS: {details}")
    
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle(title)
    msg.setText(message)

    if details:
        msg.setDetailedText(details)

    msg.setStandardButtons(QMessageBox.Ok)
    msg.setWindowFlag(Qt.WindowStaysOnTopHint, True)  # Keep the message box on top of all windows

    msg.show() # Show so that Qt calculates the frameGeometry
    center_window(msg)
    msg.exec_() 



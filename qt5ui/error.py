# util/error.py
from PyQt5.QtWidgets import QMessageBox, QWidget, QInputDialog
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

def ask_user(
    parent: QWidget,
    title: str,
    message: str,
    default_text: str = ""
) -> str:
    logger.warning(f"{title}: {message}")

    dialog = QInputDialog(parent)
    dialog.setWindowTitle(title)
    dialog.setLabelText(message)
    dialog.setTextValue(default_text)

    dialog.setWindowFlag(Qt.WindowStaysOnTopHint, True)

    dialog.show()   # allow Qt to calculate window geometry
    center_window(dialog)

    result = dialog.exec_()

    if result:  # OK pressed
        text = dialog.textValue()
        logger.info(f"Input ressult: {text}")
        return text
    else:  # Cancel pressed
        logger.info("Input canceled by user")
        return ""

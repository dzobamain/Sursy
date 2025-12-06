# util/error.py
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget
from util.log import logger

# Displays an error message box with optional details and actions.
def show_error(
    parent: QWidget,
    title: str,
    message: str,
    details: str = "",
    close_parent: bool = False,
    quit_app: bool = False
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
    msg.exec_()
        
    # window close
    if close_parent and parent is not None:
        logger.error("Closing parent window due to error.")
        parent.close()

    # Quit application
    if quit_app:
        logger.critical("Application terminated due to a critical error.")
        QApplication.quit()


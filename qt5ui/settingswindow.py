# qt5ui/settingswindow.py

from PyQt5.QtWidgets import (
    QWidget
)

from util.log import logger
from qt5ui.common import load_stylesheet
from qt5ui.uiconfig import UiConfig
from qt5ui.common import center_window

class SettingsWindow(QWidget):
    # Window
    WINDOW_NAME = "Settings"
    
    WIN_HEIGHT = 600
    WIN_WIDTH = 400
    
    def __init__(self):
        logger.info("Enter")
        super().__init__()

        self.setStyleSheet(load_stylesheet(UiConfig.SETTINGSWINDOW_STYLE))
        self.init_ui()
        
    def closeEvent(self, event):
        # Triggered when the window is closed
        logger.info("Settings window closed")
        event.accept()

    def init_ui(self):
        logger.info("Enter")

        self.setWindowTitle(self.WINDOW_NAME)
        self.resize(self.WIN_HEIGHT, self.WIN_WIDTH)
        center_window(self)  # Center the window on screen

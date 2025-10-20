# qt5ui/mainwindow.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QDesktopWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from util.log import logger
from qt5ui.common import load_stylesheet
from qt5ui.uiconfig import UiConfig
from qt5ui.common import center_window
from qt5ui.settingswindow import SettingsWindow
from config import Config

class MainWindow(QWidget):
    # Window
    WIN_HEIGHT = 800
    WIN_WIDTH = 600
    
    STYLE_PATH = UiConfig.MAINWINDOW_STYLE
    
    # ObjectNames
    SEAR_INPUT = "search_input"
    SEARCH_BUTTON = "search_button"
    SETTINGS_BUTTON = "settings_button"
    
    def __init__(self):
        logger.info("Enter")
        super().__init__()

        self.setStyleSheet(load_stylesheet(self.STYLE_PATH))
        self.init_ui()
        
    def closeEvent(self, event):
        # Triggered when the window is closed
        logger.info("Main window closed")
        # Closed SettingsWindow
        if self.settings_window is not None:
            self.settings_window.close()
        event.accept()

    def init_ui(self):
        logger.info("Enter")

        self.setWindowTitle(Config.PROGRAM_NAME)
        self.resize(self.WIN_HEIGHT, self.WIN_WIDTH)
        center_window(self)  # Center the window on screen

        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Horizontal row for input and buttons
        row_layout = QHBoxLayout()
        row_layout.setSpacing(10)

        self.text_box = QTextEdit()
        self.text_box.setObjectName(self.SEAR_INPUT) # For QSS selector
        self.text_box.setPlaceholderText("Enter your text here...")

        # Make it visually like QLineEdit
        self.text_box.setFixedHeight(40)  # same height as QLineEdit
        self.text_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_box.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_box.setWordWrapMode(True)

        # Adjust font size like QLineEdit
        font = self.text_box.font()
        font.setPointSize(16)
        self.text_box.setFont(font)

        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.setObjectName(self.SEARCH_BUTTON) # For QSS selector
        self.search_button.setMinimumHeight(40)
        self.search_button.clicked.connect(self.on_search_button_click)

        # Settings button
        self.settings_button = QPushButton()
        self.settings_button.setObjectName(self.SETTINGS_BUTTON)  # For QSS selector
        self.settings_button.setIcon(QIcon(SettingsWindow.SETTINGS_BUTTON_ICON))
        self.settings_button.setFixedSize(40, 40)
        self.settings_button.clicked.connect(self.on_settings_button_click)

        row_layout.addWidget(self.text_box, stretch=1)
        row_layout.addWidget(self.search_button)
        row_layout.addWidget(self.settings_button)

        # Label for displaying search results
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; margin-top: 20px;")

        main_layout.addLayout(row_layout)
        main_layout.addWidget(self.label)

        # Set the final layout
        self.setLayout(main_layout)
    
    def on_search_button_click(self):
        logger.info("Enter")
        
        text = self.text_box.toPlainText()
        self.text_box.clear()
        print(f"Your query: {text}")
    

    def on_settings_button_click(self):
        logger.info("Enter")

        self.settings_window = SettingsWindow()
        self.settings_window.show()


    def center(self):
        logger.info("Enter")
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

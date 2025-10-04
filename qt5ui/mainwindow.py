# qt5ui/mainwindow.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QDesktopWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from util.log import logger
from qt5ui.util import load_stylesheet
from qt5ui.uiconfig import UiConfig

class MainWindow(QWidget):
    SET_ICON = "image/icon/settings.png"
    
    def __init__(self):
        logger.info("Enter")
        super().__init__()

        self.setStyleSheet(load_stylesheet(UiConfig.MAINWINDOW_STYLE))
        self.init_ui()
        
    def closeEvent(self, event):
        # Triggered when the window is closed
        logger.info("Main window closed")
        event.accept()

    def init_ui(self):
        logger.info("Enter")

        self.setWindowTitle("Sursy")
        self.resize(800, 600)
        self.center()  # Center the window on screen

        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Horizontal row for input and buttons
        row_layout = QHBoxLayout()
        row_layout.setSpacing(10)

        # Input line
        self.text_line = QLineEdit()
        self.text_line.setPlaceholderText("Enter search query...")  # User-friendly placeholder
        self.text_line.setMinimumHeight(40)

        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.setMinimumHeight(40)
        self.search_button.clicked.connect(self.on_search_button_click)

        # Settings button
        self.settings_button = QPushButton()
        self.settings_button.setObjectName("settings_button")  # For QSS selector
        self.settings_button.setIcon(QIcon(self.SET_ICON))
        self.settings_button.setFixedSize(40, 40)
        self.settings_button.clicked.connect(self.on_settings_button_click)

        row_layout.addWidget(self.text_line, stretch=1)
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
        
        text = self.text_line.text()
        self.text_line.clear()
        print(f"Your query: {text}")

    def on_settings_button_click(self):
        logger.info("Enter")

    def center(self):
        logger.info("Enter")
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

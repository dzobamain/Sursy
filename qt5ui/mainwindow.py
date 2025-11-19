# qt5ui/mainwindow.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QListWidget, QAbstractItemView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCloseEvent, QFont

from util.log import logger
from qt5ui.common import load_stylesheet, center_window
from qt5ui.uiconfig import UiConfig
from qt5ui.settingswindow import SettingsWindow
from config import Config

class MainWindow(QWidget):
    # Window
    WIN_HEIGHT: int = 800
    WIN_WIDTH: int = 600
    
    STYLE_PATH: str = UiConfig.MAINWINDOW_STYLE
    
    # ObjectNames
    SEAR_INPUT: str = "search_input"
    SEARCH_BUTTON: str = "search_button"
    SETTINGS_BUTTON: str = "settings_button"
    SITE_LIST: str = "site_list"
    
    def __init__(self) -> None:
        logger.info("Enter")
        super().__init__()
        
        # Setting window
        self.settings_window = SettingsWindow()

        self.setStyleSheet(load_stylesheet(self.STYLE_PATH))
        self.init_ui()
    
    
    def closeEvent(self, event: QCloseEvent) -> None:
        # Triggered when the window is closed
        logger.info("Main window closed")
        # Close SettingsWindow if open
        if self.settings_window is not None:
            self.settings_window.close()
        event.accept()


    def init_ui(self) -> None:
        logger.info("Enter")

        program_config = Config.load_json(Config.PROGRAM_CONFIG)
        if program_config:
            self.setWindowTitle(program_config.get("program", {}).get("name", "Unknown"))
        self.resize(self.WIN_HEIGHT, self.WIN_WIDTH)
        center_window(self)  # Center the window on screen

        # Main vertical layout
        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Horizontal row for input and buttons
        row_layout: QHBoxLayout = QHBoxLayout()
        row_layout.setSpacing(10)

        self.text_box: QTextEdit = QTextEdit()
        self.text_box.setObjectName(self.SEAR_INPUT)  # For QSS selector
        self.text_box.setPlaceholderText("Enter your text here...")

        # Make it visually like QLineEdit
        self.text_box.setFixedHeight(40)  # same height as QLineEdit
        self.text_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_box.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_box.setWordWrapMode(True)

        # Adjust font size like QLineEdit
        font: QFont = self.text_box.font()
        font.setPointSize(16)
        self.text_box.setFont(font)

        # Search button
        self.search_button: QPushButton = QPushButton("Search")
        self.search_button.setObjectName(self.SEARCH_BUTTON)  # For QSS selector
        self.search_button.setMinimumHeight(40)
        self.search_button.clicked.connect(self.on_search_button_click)

        # Settings button
        self.settings_button: QPushButton = QPushButton()
        self.settings_button.setObjectName(self.SETTINGS_BUTTON)  # For QSS selector
        self.settings_button.setIcon(QIcon(SettingsWindow.SETTINGS_BUTTON_ICON))
        self.settings_button.setFixedSize(40, 40)
        self.settings_button.clicked.connect(self.on_settings_button_click)

        row_layout.addWidget(self.text_box, stretch=1)
        row_layout.addWidget(self.search_button)
        row_layout.addWidget(self.settings_button)

        # Results list (site/s)
        self.list_widget: QListWidget = QListWidget()
        self.list_widget.setObjectName(self.SITE_LIST)  # For QSS selector
        self.list_widget.setSelectionMode(QAbstractItemView.SingleSelection)

        # Test items
        self.list_widget.addItems([
            f"Site{i}: test" for i in range(21)
        ])

        # Add all widgets to the layout
        main_layout.addLayout(row_layout)
        main_layout.addWidget(self.list_widget, stretch=5)

        # Set the final layout
        self.setLayout(main_layout)

    
    def on_search_button_click(self) -> None:
        logger.info("Enter")
        
        text: str = self.text_box.toPlainText()
        self.text_box.clear()
        print(f"Your query: {text}")
    
    
    def on_settings_button_click(self):
        if self.settings_window is None:
            self.settings_window = SettingsWindow()

        # Show the window if it was hidden
        self.settings_window.show()

        # Bring the window to the front and focus it
        self.settings_window.raise_() # brings the window to the front
        self.settings_window.activateWindow()  # makes the window active/focused


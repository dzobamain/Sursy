# qt5ui/mainwindow.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QListWidget, QAbstractItemView
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QCloseEvent, QFont

from util.log import logger
from qt5ui.common import load_stylesheet, center_window
from qt5ui.settingswindow import SettingsWindow
from config import Config
from data.settings import Settings
from qt5ui.error import show_error
from browser.browser import Browser

class MainWindow(QWidget):
    # Window
    WIN_HEIGHT: int = 800
    WIN_WIDTH: int = 600
    
    # ObjectNames
    SEAR_INPUT: str = "search_input"
    SEARCH_BUTTON: str = "search_button"
    SETTINGS_BUTTON: str = "settings_button"
    SITE_LIST: str = "site_list"
    
    # Icons
    SETTINGS_BUTTON_ICON: str = "image/icon/settings.png"
    SEARCH_BUTTON_ICON: str = "image/icon/search.png"
    
    def __init__(self) -> None:
        logger.info("Enter")
        super().__init__()
        
        self.init_success: bool = True
        self.settings_window = None
        #self.settings = Settings()
        self.config = Config()
        self.browser = None
        
        # Style
        try:
            self.setStyleSheet(load_stylesheet(self.config.prconfig["gui"]["style"]["mainwindow"]))
        except Exception as e:
            logger.error(f"Failed to load main window stylesheet: {e}")
            show_error(
                parent=self,
                title="Style Load Error",
                message="Could not load main window stylesheet",
                details=str(e)
            )
            #self.init_success = False
            return

    
    def closeEvent(self, event: QCloseEvent) -> None:
        # Triggered when the window is closed
        # Close SettingsWindow if open
        if self.settings_window is not None:
            self.settings_window.close()
            
        logger.info("Main window closed")
        event.accept()


    def init_ui(self) -> None: 
        try:
            self.setWindowTitle(self.config.prconfig["program"]["name"])
        except Exception as e:
            logger.error(f"Failed to load main window stylesheet: {e}")
            show_error(
                parent=self,
                title="Warning",
                message='Config has not style for main window title, using default.',
                details=str(e),
                close_parent=True
            )
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
        self.settings_button.setIcon(QIcon(self.SETTINGS_BUTTON_ICON))
        self.settings_button.setFixedSize(40, 40)
        self.settings_button.clicked.connect(self.on_settings_button_click)

        row_layout.addWidget(self.text_box, stretch=1)
        row_layout.addWidget(self.search_button)
        row_layout.addWidget(self.settings_button)

        # Results list (site/s)
        self.list_widget: QListWidget = QListWidget()
        self.list_widget.setObjectName(self.SITE_LIST)  # For QSS selector
        self.list_widget.setSelectionMode(QAbstractItemView.SingleSelection)

        # items

        # Add all widgets to the layout
        main_layout.addLayout(row_layout)
        main_layout.addWidget(self.list_widget, stretch=5)

        # Set the final layout
        self.setLayout(main_layout)

    
    def on_search_button_click(self) -> None:
        if self.browser is None:
            self.browser = Browser()
        
        if not self.browser.verify_browser_path():
            show_error(
                parent=self,
                title="Browser Error",
                message="Browser is not configured properly. Please check your settings."
            )
        return
    
    
    def on_settings_button_click(self):
        if self.settings_window is None:
            self.settings_window = SettingsWindow()
            self.settings_window.init_ui()

        # Show the window if it was hidden
        self.settings_window.show()

        # Bring the window to the front and focus it
        self.settings_window.raise_() # brings the window to the front
        self.settings_window.activateWindow()  # makes the window active/focused


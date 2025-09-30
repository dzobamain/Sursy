# qt5ui/mainwindow.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QDesktopWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from util.log import logger

class MainWindow(QWidget):
    def __init__(self):
        logger.info("Enter")
        
        super().__init__()
        # Initialize the user interface
        self.init_ui()

    def init_ui(self):
        logger.info("Enter")
        
        self.setWindowTitle("Sursy")
        self.resize(800, 600)
        # Center the window on the screen
        self.center()

        # Main vertical layout (all elements stacked vertically)
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)  # Align content to the top

        # === Horizontal row for input and buttons ===
        row_layout = QHBoxLayout()
        row_layout.setSpacing(10)  # Spacing between elements

        # === Input line for user text ===
        self.text_line = QLineEdit()
        self.text_line.setPlaceholderText("Enter search query...")  # More descriptive placeholder
        self.text_line.setMinimumHeight(40)
        self.text_line.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid #ccc;  /* gray border */
                border-radius: 10px;     /* rounded corners */
                padding: 0 10px;         /* text padding */
                font-size: 16px;         /* font size */
            }
            QLineEdit:focus {
                border: 2px solid #0078d7;  /* blue border on focus */
            }
            """
        )

        # === Button style shared by main buttons ===
        button_style = """
        QPushButton {
            background-color: #0078d7; /* blue button */
            color: white;              /* white text */
            border-radius: 10px;       /* rounded corners */
            font-size: 16px;           /* font size */
            padding: 5px 15px;         /* internal padding */
        }
        QPushButton:hover {
            background-color: #005a9e; /* darker on hover */
        }
        QPushButton:pressed {
            background-color: #003f6b; /* even darker when pressed */
        }
        """

        # === Search button ===
        self.search_button = QPushButton("Search")
        self.search_button.setMinimumHeight(40)
        self.search_button.setStyleSheet(button_style)
        self.search_button.clicked.connect(self.on_search_button_click)  # Trigger on click

        # === Settings icon button ===
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon("image/icon/settings.png"))
        self.settings_button.setFixedSize(40, 40)
        self.settings_button.clicked.connect(self.on_settings_button_click)
        self.settings_button.setStyleSheet(
            """
            QPushButton {
                background-color: white;   /* white button */
                border-radius: 10px;       /* rounded corners */
                border: 1px solid #ccc;    /* light gray border */
            }
            QPushButton:hover {
                background-color: #f0f0f0; /* light gray on hover */
            }
            QPushButton:pressed {
                background-color: #e0e0e0; /* slightly darker on press */
            }
            """
        )

        # Add widgets to horizontal row
        # stretch=1 ensures the input line expands to fill available space
        row_layout.addWidget(self.text_line, stretch=1)
        row_layout.addWidget(self.search_button)
        row_layout.addWidget(self.settings_button)

        # === Label for displaying search results or feedback ===
        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignCenter)  # Center the text
        self.label.setStyleSheet("font-size: 18px; margin-top: 20px;")  # Font size and top margin

        # Add the row and label to the main layout
        main_layout.addLayout(row_layout)
        main_layout.addWidget(self.label)

        # Set the main layout for the window
        self.setLayout(main_layout)

    # === Triggered when Search button is clicked ===
    def on_search_button_click(self):
        logger.info("Enter")
        
        text = self.text_line.text()
        self.text_line.clear()
        
        print(f"Your query: {text}")
        
    def on_settings_button_click(self):
        logger.info("Enter")

    # === Center the window on the screen ===
    def center(self):
        logger.info("Enter")
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

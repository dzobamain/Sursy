from PyQt5.QtWidgets import (
    QWidget, QLabel, QComboBox, QLineEdit, QCheckBox, QFormLayout, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt

from util.log import logger
from qt5ui.common import load_stylesheet, center_window
from qt5ui.uiconfig import UiConfig

class SettingsWindow(QWidget):
    # Window
    WINDOW_NAME = "Settings"
    
    # Icons
    SETTINGS_BUTTON_ICON = "image/icon/settings.png"
    
    STYLE_PATH = UiConfig.SETTINGSWINDOW_STYLE
    
    # Window size
    WIN_WIDTH = 600
    WIN_HEIGHT = 400
    
    def __init__(self):
        logger.info("Enter")
        super().__init__()

        self.setStyleSheet(load_stylesheet(self.STYLE_PATH))
        self.init_ui()
        
    def closeEvent(self, event):
        # Triggered when the window is closed
        logger.info("Settings window closed")
        event.accept()

    def init_ui(self):
        logger.info("Enter")

        self.setWindowTitle(self.WINDOW_NAME)
        self.resize(self.WIN_WIDTH, self.WIN_HEIGHT)
        center_window(self)

        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)
        layout.setFormAlignment(Qt.AlignTop)
        layout.setHorizontalSpacing(10)

        def add_row(label_text, widget):
            row = QHBoxLayout()
            label = QLabel(label_text)
            row.addWidget(label)
            row.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
            row.addWidget(widget, alignment=Qt.AlignRight)
            layout.addRow(row)

        # 1. Dropdown (combobox)
        combo1 = QComboBox(); combo1.addItems(["1", "2", "3"])
        add_row("tab_open_style:", combo1)

        # 2–4. Int input fields (max 3 digits)
        input1 = QLineEdit(); input1.setMaxLength(3); input1.setFixedWidth(50)
        add_row("limit_count:", input1)

        input2 = QLineEdit(); input2.setMaxLength(3); input2.setFixedWidth(50)
        add_row("min_page_rating:", input2)

        input3 = QLineEdit(); input3.setMaxLength(3); input3.setFixedWidth(50)
        add_row("max_page_rating:", input3)

        # 5. Checkbox
        checkbox1 = QCheckBox()
        add_row("clear_input_after_search:", checkbox1)

        # 6. Another dropdown
        combo2 = QComboBox(); combo2.addItems(["1", "2", "3"])
        add_row("language_preference:", combo2)

        # 7. Another checkbox
        checkbox2 = QCheckBox()
        add_row("program_opinion:", checkbox2)

        self.setLayout(layout)


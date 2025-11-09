# qt5ui/settingswindow.py

from typing import List
from PyQt5.QtWidgets import (
    QWidget, QLabel, QComboBox, QLineEdit, QCheckBox, QFormLayout, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent, QIntValidator

from util.log import logger
from qt5ui.common import load_stylesheet, center_window
from qt5ui.uiconfig import UiConfig
from data.settings import Settings
from data.json_io import load_from_json
from config import Config

class SettingsWindow(QWidget):
    STYLE_PATH: str = UiConfig.SETTINGSWINDOW_STYLE
    
    # Window
    WIN_WIDTH: int = 600
    WIN_HEIGHT: int = 400
    WINDOW_NAME: str = "Settings"
    
    # Icons
    SETTINGS_BUTTON_ICON: str = "image/icon/settings.png"
    
    def __init__(self) -> None:
        logger.info("Enter")
        super().__init__()

        self.setStyleSheet(load_stylesheet(self.STYLE_PATH))
        self.init_ui()

    def closeEvent(self, event: QCloseEvent) -> None:
        # Triggered when the window is closed
        logger.info("Settings window closed")
        event.accept()

    def init_ui(self) -> None:
        logger.info("Enter")
        self.setWindowTitle(self.WINDOW_NAME)
        self.resize(self.WIN_WIDTH, self.WIN_HEIGHT)
        center_window(self)

        layout: QFormLayout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)
        layout.setFormAlignment(Qt.AlignTop)
        layout.setHorizontalSpacing(10)

        settings = Settings()
        load_from_json(settings, Config.SETTINGS_PATH)

        # Create UI elements
        combobox_open_style: QComboBox = self.make_dynamic_combobox(settings.TAB_OPEN_STYLE_OPTIONS)
        self.add_row("Information display mode", combobox_open_style, layout)
        combobox_open_style.setCurrentIndex(settings.tab_open_style_value)

        line_limit_count: QLineEdit = self.make_resizable_lineedit()
        self.add_row("Number of sources", line_limit_count, layout)
        line_limit_count.setText(settings.limit_count.__str__())

        line_min_page_rating: QLineEdit = self.make_resizable_lineedit()
        self.add_row("Minimum source rating", line_min_page_rating, layout)
        line_min_page_rating.setText(settings.min_page_rating.__str__())

        line_max_page_rating: QLineEdit = self.make_resizable_lineedit()
        self.add_row("Maximum source rating", line_max_page_rating, layout)
        line_max_page_rating.setText(settings.max_page_rating.__str__())

        checkbox_clear_input: QCheckBox = QCheckBox()
        self.add_row("Clear input after search", checkbox_clear_input, layout)
        checkbox_clear_input.setChecked(settings.clear_input_after_search)

        combobox_language: QComboBox = self.make_dynamic_combobox(settings.LANGUAGE_PREFERENCE_OPTIONS)
        self.add_row("Search language", combobox_language, layout)
        combobox_language.setCurrentIndex(settings.language_preference_value)

        checkbox_program_opinion: QCheckBox = QCheckBox()
        self.add_row("Program opinion", checkbox_program_opinion, layout)
        checkbox_program_opinion.setChecked(settings.program_opinion)

        self.setLayout(layout)


    # Add row with label and widget
    def add_row(self, label_text: str, widget: QWidget, layout: QFormLayout) -> None:
        logger.info(f"Enter {widget}")
        row: QHBoxLayout = QHBoxLayout()
        label: QLabel = QLabel(label_text)
        row.addWidget(label)
        row.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        row.addWidget(widget, alignment=Qt.AlignRight)
        layout.addRow(row)
        
    # Create resizable QLineEdit
    def make_resizable_lineedit(self) -> QLineEdit:
        logger.info("Enter")
        line_edit: QLineEdit = QLineEdit()
        line_edit.setMaxLength(3)  # max 3 digits 
        line_edit.setValidator(QIntValidator()) # Only int input
        line_edit.setFixedHeight(40)  # height same as other fields 
        line_edit.setAlignment(Qt.AlignCenter)  # center text
        line_edit.textChanged.connect(lambda text, le=line_edit: self.adjust_width_lineedit(le, text))
        self.adjust_width_lineedit(line_edit, "")
        return line_edit

    # Create dynamic QComboBox
    def make_dynamic_combobox(self, items: List[str]) -> QComboBox:
        logger.info("Enter")
        combo: QComboBox = QComboBox()
        combo.addItems(items)
        combo.setEditable(False)  # user can only select

        # Adjust field width under current text
        self.adjust_width_combobox(combo)

        # Adjust dropdown width under the longest item
        metrics = combo.fontMetrics()
        max_text_width: int = max([metrics.horizontalAdvance(text) for text in items])
        combo.view().setMinimumWidth(max_text_width + 34)  # + padding

        # Update field width when selection changes
        combo.currentTextChanged.connect(lambda text, cb=combo: self.adjust_width_combobox(cb))

        return combo

    # Adjust QLineEdit width dynamically
    def adjust_width_lineedit(self, widget: QLineEdit, text: str) -> None:
        metrics = widget.fontMetrics()
        width: int = metrics.horizontalAdvance(text)
        min_width: int = 60
        max_width: int = 150
        widget.setFixedWidth(max(min_width, min(width, max_width)))
        
    # Adjust QComboBox width dynamically
    def adjust_width_combobox(self, combo: QComboBox) -> None:
        metrics = combo.fontMetrics()
        width: int = metrics.horizontalAdvance(combo.currentText()) + 24
        min_width: int = 30
        max_width: int = 250
        combo.setFixedWidth(max(min_width, min(width, max_width)))

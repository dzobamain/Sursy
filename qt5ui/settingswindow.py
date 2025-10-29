# qt5ui/settingswindow.py

from typing import List
from PyQt5.QtWidgets import (
    QWidget, QLabel, QComboBox, QLineEdit, QCheckBox, QFormLayout, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent

from util.log import logger
from qt5ui.common import load_stylesheet, center_window
from qt5ui.uiconfig import UiConfig
from data.settings import Settings

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

        # Add row with label and widget
        def add_row(label_text: str, widget: QWidget) -> None:
            logger.info(f"Enter {widget}")
            
            row: QHBoxLayout = QHBoxLayout()
            label: QLabel = QLabel(label_text)
            row.addWidget(label)
            row.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
            row.addWidget(widget, alignment=Qt.AlignRight)
            layout.addRow(row)

        # Create resizable QLineEdit
        def make_resizable_lineedit() -> QLineEdit:
            logger.info("Enter")
            
            line_edit: QLineEdit = QLineEdit()
            line_edit.setMaxLength(3)  # max 3 digits 
            line_edit.setFixedHeight(40)  # height same as other fields 
            line_edit.setAlignment(Qt.AlignCenter)  # center text
            line_edit.textChanged.connect(lambda text, le=line_edit: self.adjust_width_lineedit(le, text))
            self.adjust_width_lineedit(line_edit, "")
            return line_edit

        # Create dynamic QComboBox
        def make_dynamic_combobox(items: List[str]) -> QComboBox:
            logger.info("Enter")
            
            combo: QComboBox = QComboBox()
            combo.addItems(items)
            combo.setEditable(False)  # user can only select

            # Adjust field width under current text / ширина поля під текст
            self.adjust_width_combobox(combo)

            # Adjust dropdown width under the longest item / ширина списку під найдовший пункт
            metrics = combo.fontMetrics()
            max_text_width: int = max([metrics.horizontalAdvance(text) for text in items])
            combo.view().setMinimumWidth(max_text_width + 40)  # + padding

            # Update field width when selection changes / підлаштовуємо ширину при зміні
            combo.currentTextChanged.connect(lambda text, cb=combo: self.adjust_width_combobox(cb))

            return combo

        set = Settings()
        
        # Create UI elements
        combobox_open_style: QComboBox = make_dynamic_combobox(set.TAB_OPEN_STYLE_OPTIONS)
        add_row("Information display mode", combobox_open_style)

        line_limit_count: QLineEdit = make_resizable_lineedit()
        add_row("Number of sources", line_limit_count)

        line_min_page_rating: QLineEdit = make_resizable_lineedit()
        add_row("Minimum source rating", line_min_page_rating)

        line_max_page_rating: QLineEdit = make_resizable_lineedit()
        add_row("Maximum source rating", line_max_page_rating)

        checkbox_clear_input: QCheckBox = QCheckBox()
        add_row("Clear input after search", checkbox_clear_input)

        combobox_language: QComboBox = make_dynamic_combobox(set.LANGUAGE_PREFERENCE_OPTIONS)
        add_row("Search language", combobox_language)

        checkbox_program_opinion: QCheckBox = QCheckBox()
        add_row("Program opinion", checkbox_program_opinion)

        self.setLayout(layout)

    # Adjust QLineEdit width dynamically
    def adjust_width_lineedit(self, widget: QLineEdit, text: str) -> None:
        metrics = widget.fontMetrics()
        width: int = metrics.horizontalAdvance(text) + 30  # padding / запас
        min_width: int = 60
        max_width: int = 150
        widget.setFixedWidth(max(min_width, min(width, max_width)))

    # Adjust QComboBox width dynamically
    def adjust_width_combobox(self, combo: QComboBox) -> None:
        metrics = combo.fontMetrics()
        width: int = metrics.horizontalAdvance(combo.currentText()) + 30
        min_width: int = 30
        max_width: int = 250
        combo.setFixedWidth(max(min_width, min(width, max_width)))

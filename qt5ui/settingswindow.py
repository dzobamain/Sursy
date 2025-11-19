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
from data.json_io import save_to_json
from config import Config

class SettingsWindow(QWidget):
    STYLE_PATH: str = UiConfig.SETTINGSWINDOW_STYLE
    
    # Window
    WIN_WIDTH: int = 600
    WIN_HEIGHT: int = 400
    WINDOW_NAME: str = "Settings"
    
    # Icons
    SETTINGS_BUTTON_ICON: str = "image/icon/settings.png"
    
    # data
    settings = Settings()
    
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

        # Create UI elements
        self.combobox_open_style = self.make_dynamic_combobox(self.settings.TAB_OPEN_STYLE_OPTIONS)
        self.add_row("Information display mode", self.combobox_open_style, layout)
        self.combobox_open_style.setCurrentIndex(self.settings.tab_open_style_value)

        self.combobox_open_style.currentIndexChanged.connect(
            lambda index: self.on_user_change("tab_open_style_value", index)
        )

        # --- limit_count ---
        self.line_limit_count = self.make_resizable_lineedit()
        self.add_row("Number of sources", self.line_limit_count, layout)
        self.line_limit_count.setText(str(self.settings.limit_count))

        self.line_limit_count.textChanged.connect(
            lambda text: self.on_user_change("limit_count", text)
        )

        # --- min_page_rating ---
        self.line_min_page_rating = self.make_resizable_lineedit()
        self.add_row("Minimum source rating", self.line_min_page_rating, layout)
        self.line_min_page_rating.setText(str(self.settings.min_page_rating))

        self.line_min_page_rating.textChanged.connect(
            lambda text: self.on_user_change("min_page_rating", text)
        )

        # --- max_page_rating ---
        self.line_max_page_rating = self.make_resizable_lineedit()
        self.add_row("Maximum source rating", self.line_max_page_rating, layout)
        self.line_max_page_rating.setText(str(self.settings.max_page_rating))

        self.line_max_page_rating.textChanged.connect(
            lambda text: self.on_user_change("max_page_rating", text)
        )

        # --- checkbox_clear_input ---
        self.checkbox_clear_input = QCheckBox()
        self.add_row("Clear input after search", self.checkbox_clear_input, layout)
        self.checkbox_clear_input.setChecked(self.settings.clear_input_after_search)

        # ⚡ Connect using Qt.Checked comparison
        self.checkbox_clear_input.stateChanged.connect(
            lambda state: self.on_user_change("clear_input_after_search", state == Qt.Checked)
        )

        # --- combobox_language ---
        self.combobox_language = self.make_dynamic_combobox(self.settings.LANGUAGE_PREFERENCE_OPTIONS)
        self.add_row("Search language", self.combobox_language, layout)
        self.combobox_language.setCurrentIndex(self.settings.language_preference_value)

        self.combobox_language.currentIndexChanged.connect(
            lambda index: self.on_user_change("language_preference_value", index)
        )

        # --- checkbox_program_opinion ---
        self.checkbox_program_opinion = QCheckBox()
        self.add_row("Program opinion", self.checkbox_program_opinion, layout)
        self.checkbox_program_opinion.setChecked(self.settings.program_opinion)

        # ⚡ Connect using Qt.Checked comparison
        self.checkbox_program_opinion.stateChanged.connect(
            lambda state: self.on_user_change("program_opinion", state == Qt.Checked)
        )

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
        
    # Track changes in fields
    def on_user_change(self, key: str, new_value):
        old_value = getattr(self.settings, key)

        # Type conversion for int/float only, bool уже булеве
        try:
            if isinstance(old_value, int):
                new_value = int(new_value)
            elif isinstance(old_value, float):
                new_value = float(new_value)
        except ValueError:
            logger.info(f"Invalid type for {key}, revert")
            self.restore_old_value(key, old_value)
            return

        setattr(self.settings, key, new_value)

        # Validation
        if not self.settings.check_parameters():
            logger.info(f"Validation failed for {key}, reverting")
            setattr(self.settings, key, old_value)
            self.restore_old_value(key, old_value)
            return

        # Save settings
        save_to_json(self.settings, Config.SETTINGS_PATH)
        logger.info(f"Saved {key} = {new_value}")

    def restore_old_value(self, key: str, value):
        # Restore the old value in UI
        if key == "tab_open_style_value":
            self.combobox_open_style.blockSignals(True) # block signals to avoid recursion
            self.combobox_open_style.setCurrentIndex(value) # restore value
            self.combobox_open_style.blockSignals(False) # unblock signals
        elif key == "limit_count":
            self.line_limit_count.blockSignals(True)
            self.line_limit_count.setText(str(value))
            self.line_limit_count.blockSignals(False)
        elif key == "min_page_rating":
            self.line_min_page_rating.blockSignals(True)
            self.line_min_page_rating.setText(str(value))
            self.line_min_page_rating.blockSignals(False)
        elif key == "max_page_rating":
            self.line_max_page_rating.blockSignals(True)
            self.line_max_page_rating.setText(str(value))
            self.line_max_page_rating.blockSignals(False)
        elif key == "clear_input_after_search":
            self.checkbox_clear_input.blockSignals(True)
            self.checkbox_clear_input.setChecked(value)
            self.checkbox_clear_input.blockSignals(False)
        elif key == "language_preference_value":
            self.combobox_language.blockSignals(True)
            self.combobox_language.setCurrentIndex(value)
            self.combobox_language.blockSignals(False)
        elif key == "program_opinion":
            self.checkbox_program_opinion.blockSignals(True)
            self.checkbox_program_opinion.setChecked(value)
            self.checkbox_program_opinion.blockSignals(False)

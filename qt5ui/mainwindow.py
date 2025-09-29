# qt5ui/mainwindow.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QDesktopWidget
from PyQt5.QtCore import Qt

class TextLine:
    def __init__(self, placeholder=""):
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholder)

    def get_text(self):
        return self.line_edit.text()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Sursy")
        self.resize(800, 600)
        self.center()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.text_line_obj = TextLine("Enter text here")

        self.button = QPushButton("Take")
        self.button.clicked.connect(self.on_button_click)

        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.text_line_obj.line_edit)
        layout.addWidget(self.button)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def on_button_click(self):
        text = self.text_line_obj.get_text()
        self.label.setText(f"Your text: {text}")

    def get_text(self):
        return self.text_line_obj.get_text()
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

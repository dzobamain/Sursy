# main.py

import sys
from typing import List
from PyQt5.QtWidgets import QApplication

from qt5ui.mainwindow import MainWindow
from util.log import logger

def main(argv: List[str]) -> int:
    app: QApplication = QApplication(argv)
    window: MainWindow = MainWindow()
    
    if not window.init_success:
        return -1
    
    window.init_ui()
    window.show()
    app.exec_()

    return 0

if __name__ == "__main__":
    exit_code: int = main(sys.argv)
    logger.info("Program ended")
    sys.exit(exit_code)

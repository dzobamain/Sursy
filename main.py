# ./main.py

import sys
from PyQt5.QtWidgets import QApplication

from qt5ui.mainwindow import MainWindow
from util.log import logger

def main(argv) -> int:
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    app.exec_()

    return 0

if __name__ == "__main__":
    logger.info("Program started")
    exit_code = main(sys.argv[1:])
    logger.info("Program ended")
    sys.exit(exit_code)

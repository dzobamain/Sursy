# main.py

import sys
from PyQt5.QtWidgets import QApplication

from qt5ui.mainwindow import MainWindow
from util.log import logger

def main(argv) -> int:
    logger.info("Enter")
    
    app = QApplication(argv)
    window = MainWindow() # Create window object
    window.show() # Show the window
    app.exec_()
    
    logger.info("Program ended")

    return 0

if __name__ == "__main__":
    exit_code = main(sys.argv[1:])
    sys.exit(exit_code)

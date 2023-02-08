import sys
from PyQt6.QtWidgets import *

import main_window
from main_window import appWindow
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = appWindow()
    main_window.show()
    sys.exit(app.exec())

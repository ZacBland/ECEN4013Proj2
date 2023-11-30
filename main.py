from PyQt5.QtWidgets import QApplication

import sys

from ui import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ctx = Context()
    ctx.show()
    app.exec()
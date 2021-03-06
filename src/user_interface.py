#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import massTextUtils as utils
import Pages as pages


if __name__ == '__main__':
    app = QApplication([])
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.green)
    app.setPalette(palette)
    home_page = pages.MainScreen()
    sys.exit(app.exec_())

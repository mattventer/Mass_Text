#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import Pages as pages



if __name__ == '__main__':
    app = QApplication(sys.argv)
    home_page = pages.MainScreen()
    sys.exit(app.exec_())
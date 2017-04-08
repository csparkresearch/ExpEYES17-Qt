# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from __future__ import print_function

from PyQt4.QtGui import QWidget, QApplication
import sys

class componentWidget(QWidget):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w=componentWidget()

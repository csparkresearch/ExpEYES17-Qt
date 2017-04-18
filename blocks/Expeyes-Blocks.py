#!/usr/bin/python
# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-

from __future__ import print_function

license="""\
  Copyright (C) 2017 Georges Khaznadar <georgesk@debian.org>

  Application Expeyes-Blocks

  This application may be used under the terms of the
  GNU General Public License version 3.0 as published by
  the Free Software Foundation, or, at your preference,
   any later verion of the same.

  Expeyes-Blocks is built upon Qt4 GUI libraries, see "About Qt".

  This application is provided AS IS with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND
  FITNESS FOR A PARTICULAR PURPOSE.
"""

import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QTranslator, QLocale, QLibraryInfo
import eyeBlocks.mainwindow
import os

app = QApplication(sys.argv)

# Qt's lanquage files
qtTranslator=QTranslator()
qtTranslator.load("qt_" + QLocale.system().name(), QLibraryInfo.location(QLibraryInfo.TranslationsPath))
app.installTranslator(qtTranslator)

# this application's language files are in eyeBlocks module's directory
langPath=os.path.join(os.path.dirname(eyeBlocks.mainwindow.__file__), "lang")
myTranslator=QTranslator()
myTranslator.load(QLocale.system().name(), langPath)
app.installTranslator(myTranslator)

######## Creating the main window
window = eyeBlocks.mainwindow.BlockMainWindow()
window.show()
if len(sys.argv) > 1:
	window.loadFile(sys.argv[1])
sys.exit(app.exec_())

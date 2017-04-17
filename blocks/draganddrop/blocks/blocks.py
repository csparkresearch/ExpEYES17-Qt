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

import copy

from PyQt4.QtCore import QPoint, QRect, Qt, QSize, QString, QTimer

from PyQt4.QtGui import QWidget, QPixmap, QSizePolicy, QColor, \
		QPainter, QListWidget, QListWidgetItem, QMainWindow, \
		qApp, QFrame, QApplication, QHBoxLayout, QListView, QMessageBox

from templates.ui_blocks import Ui_MainWindow
from component import Component, InputComponent
from timecomponent import TimeComponent
#from modifcomponent import ModifComponent
#from channelcomponent import ChannelComponent


class BlockMainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		QMainWindow.__init__(self, parent)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.loadComponents()
		self.connectSignals()
		return

	def loadComponents(self, path=None):
		self.widget.clear()
		cList=Component.listFromRC()
		for c in cList:
			self.componentsList.newComponent(c)
		return

	def connectSignals(self):
		"""
		connecting signals to methods
		"""
		self.action_Quit.triggered.connect(self.close)
		self.actionSave.triggered.connect(self.save)
		self.actionSave_as.triggered.connect(self.saveAs)
		self.action_Open.triggered.connect(self.load)
		self.action_About.triggered.connect(self.about)
		self.actionAbout_Qt.triggered.connect(self.aboutQt)
		
	def about(self):
		"""
		brings up the About dialog
		"""
		QMessageBox.about(self,"About", license)
		return
		
	def aboutQt(self):
		"""
		brings up the About dialog
		"""
		QMessageBox.aboutQt(self,"About Qt")
		return
		
	def load(self):
		"""
		Loads a component composition
		"""
		return
		
	def save(self):
		"""
		Saves the current component composition
		"""
		return
		
	def saveAs(self, filename=None):
		"""
		Saves the current component composition in a new file
		@param filename name of the file, defaults to None
		"""
		return
		
if __name__ == '__main__':

	import sys

	app = QApplication(sys.argv)
	window = BlockMainWindow()
	#window.loadComponents()
	window.show()
	sys.exit(app.exec_())

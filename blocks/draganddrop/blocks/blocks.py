#!/usr/bin/python
# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
############################################################################
#
#  Copyright (C) 2017 Georges Khaznadar <georgesk@debian.org>
#
#
#  This file may be used under the terms of the GNU General Public
#  License version 3.0 as published by the Free Software Foundation,
#  or, at your preference, any later verion of the same.
#
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
############################################################################

from __future__ import print_function

import copy
from PyQt4 import QtCore, QtGui
from component import Component, acceptedFormats

class BlockWidget(QtGui.QWidget):

	def __init__(self, parent=None):
		super(BlockWidget, self).__init__(parent)

		self.comp = None #dragged component
		self.components = []
		self.hot = None # when it is a QPoint, something is hot there

		self.setAcceptDrops(True)
		self.setMinimumSize(400, 400)
		self.hotPx={
			"red": QtGui.QPixmap(":/hot/hot-red.svg"),
		}

	def clear(self):
		self.components = []
		self.hot=None
		self.update()

	def dragEnterEvent(self, event):
		if acceptedFormats(event):
		   event.accept()
		else:
			event.ignore()

	def dragMoveEvent(self, event):
		f=acceptedFormats(event)
		if f:
			data = event.mimeData().data(f[0])
			comp=Component.unserialize(data)
			offset=comp.hotspot
			print("GRRR===============", comp, event.pos(), -offset)
			for sp in comp.snapPoints:
				hovering=event.pos()-offset+sp
				print("GRRR", sp.text,"hover", hovering)
				
			event.setDropAction(QtCore.Qt.MoveAction)
			event.accept()
		else:
			event.ignore()
		return

	def dropEvent(self, event):
		comp=Component.unserializeFromEvent(event)
		if comp:
			self.components.append(comp)
			self.update(comp.rect)
			event.setDropAction(QtCore.Qt.MoveAction)
			event.accept()
		else:
			event.ignore()


	def mousePressEvent(self, event):
		comps=self.targetComps(event.pos())
		if not comps:
			return
		comp = comps[-1]
		index=self.components.index(comp)
		comp=copy.copy(comp)

		del self.components[index]

		self.update(comp.rect)

		comp.hotspot=QtCore.QPoint(event.pos() - comp.rect.topLeft())
		itemData = comp.serialize()
		drag=comp.makeDrag(self)

		if drag.exec_(QtCore.Qt.MoveAction) != QtCore.Qt.MoveAction:
			self.components.insert(index, self.comp)
			self.update()

	def paintEvent(self, event):
		painter = QtGui.QPainter()
		painter.begin(self)
		painter.fillRect(event.rect(), QtCore.Qt.white)
		
		l=[(c.rect, c.pixmap) for c in self.components]
		for rect, pixmap in l:
			painter.drawPixmap(rect, pixmap)

		# hot indicator
		if self.hot:
			# paint a circle around
			px=self.hotPx["red"]
			w,h = px.size().width(), px.size().height()
			painter.drawPixmap(
				QtCore.QRect(
					QtCore.QPoint(self.hot.x()-w/2, self.hot.y()-h/2),
					px.size()),
				px)
		painter.end()

	def targetComps(self, position):
		"""
		returns the list of components
		under a mouse click; the topmost component comes last.
		"""
		comps = [c for c in self.components if c.rect.contains(position)]
		return comps

class componentsList(QtGui.QListWidget):
	def __init__(self, parent=None):
		super(componentsList, self).__init__(parent)

		self.setDragEnabled(True)
		self.setViewMode(QtGui.QListView.IconMode)
		self.setIconSize(QtCore.QSize(60, 60))
		self.setSpacing(10)
		self.setAcceptDrops(True)
		self.setDropIndicatorShown(True)
		self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
				QtGui.QSizePolicy.Expanding))
		self.setMinimumSize(200, 400)
		self.setMaximumSize(200, 4000)

	def dragEnterEvent(self, event):
		if acceptedFormats(event):
			event.accept()
		else:
			event.ignore()

	def dragMoveEvent(self, event):
		if acceptedFormats(event):
			event.setDropAction(QtCore.Qt.MoveAction)
			event.accept()
		else:
			event.ignore()

	def dropEvent(self, event):
		comp=Component.unserializeFromEvent(event)
		if comp:
			# components of type 1 can be duplicated
			# so they should not be appended to the list
			if comp.mimetype.contains("image/x-Block-1"):
				pass
			elif comp.mimetype.contains("image/x-Block-2"):
				self.addPiece(comp)

			event.setDropAction(QtCore.Qt.MoveAction)
			event.accept()
		else:
			event.ignore()

	def newComponent(self, comp):
		item=self.addPiece(comp)
		self.insertItem(0, item)
		return

	def addPiece(self, comp):
		"""
		adds a Component instance,
		and returns the QListWidgetItem created
		"""
		ident=QtCore.QString(comp.ident)
		for i in range(self.count()):
			if self.item(i).component.ident == ident:
				self.item(i).setHidden(False)
				return
		blockItem = QtGui.QListWidgetItem(self)
		comp.toListWidgetItem(blockItem)
		return blockItem

	def currentComponent(self):
		item = self.currentItem()
		return Component.fromListWidgetItem(item)
		
		
	def startDrag(self, supportedActions):
		component=self.currentComponent()
		drag=component.makeDrag(self)

		if drag.exec_(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
			# components of type 1 can be duplicated
			# so they should not be hidden from the list
			if component.mimetype.contains("image/x-Block-1"):
				pass
			elif component.mimetype.contains("image/x-Block-2"):
				self.currentItem().setHidden(True)


class MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.BlockImage = QtGui.QPixmap()

		self.setupMenus()
		self.setupWidgets()

		self.setWindowTitle("Block")
		
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
		
	def loadComponents(self, path=None):
		self.componentsList.clear()
		self.BlockWidget.clear()
		cList=Component.listFromRC()
		for c in cList:
			self.componentsList.newComponent(c)
		return

	def setupMenus(self):
		fileMenu = self.menuBar().addMenu("&File")

		openAction = fileMenu.addAction("&Open...")
		openAction.setShortcut("Ctrl+O")

		saveAction = fileMenu.addAction("&Save...")
		openAction.setShortcut("Ctrl+S")

		exitAction = fileMenu.addAction("E&xit")
		exitAction.setShortcut("Ctrl+Q")


		openAction.triggered.connect(self.load)
		saveAction.triggered.connect(self.save)
		exitAction.triggered.connect(QtGui.qApp.quit)
		

	def setupWidgets(self):
		frame = QtGui.QFrame()
		frameLayout = QtGui.QHBoxLayout(frame)

		self.componentsList = componentsList()

		self.BlockWidget = BlockWidget()

		frameLayout.addWidget(self.componentsList)
		frameLayout.addWidget(self.BlockWidget)
		self.setCentralWidget(frame)


if __name__ == '__main__':

	import sys

	app = QtGui.QApplication(sys.argv)
	window = MainWindow()
	window.loadComponents()
	window.show()
	sys.exit(app.exec_())

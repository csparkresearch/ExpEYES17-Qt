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

from PyQt4.QtCore import QPoint, QRect, Qt, QSize, QString, QTimer

from PyQt4.QtGui import QWidget, QPixmap, QSizePolicy, QColor, \
		QPainter, QListWidget, QListWidgetItem, QMainWindow, \
		qApp, QFrame, QApplication, QHBoxLayout, QListView

from templates.ui_blocks import Ui_MainWindow
from component import Component, InputComponent
from timecomponent import TimeComponent
#from modifcomponent import ModifComponent
#from channelcomponent import ChannelComponent


class ComponentsList(QListWidget):
	def __init__(self, parent=None):
		super(ComponentsList, self).__init__(parent)

		self.setDragEnabled(True)
		self.setViewMode(QListView.IconMode)
		self.setIconSize(QSize(60, 60))
		self.setSpacing(10)
		self.setAcceptDrops(True)
		self.setDropIndicatorShown(True)
		return

	def dragEnterEvent(self, event):
		if Component.acceptedFormats(event):
			event.accept()
		else:
			event.ignore()
		return

	def dragMoveEvent(self, event):
		if Component.acceptedFormats(event):
			event.setDropAction(Qt.MoveAction)
			event.accept()
		else:
			event.ignore()
		return

	def dropEvent(self, event):
		comp, dataStream, className = Component.unserializeFromEvent(event)
		if comp:
			# components of type 1 can be duplicated
			# so they should not be appended to the list
			if comp.mimetype.contains("image/x-Block-1"):
				pass
			elif comp.mimetype.contains("image/x-Block-2"):
				self.addPiece(comp)

			event.setDropAction(Qt.MoveAction)
			event.accept()
		else:
			event.ignore()
		return

	def newComponent(self, comp):
		item=self.addPiece(comp)
		self.insertItem(0, item)
		return
		
	def hideItem(self, comp, state=True):
		"""
		Hides list items if they are same as a component

		:param comp: a component
		:type comp:
		:param state: when False, it will unhide; True by default
		:type state:
		:returns: index of the found item (-1 if none)
		"""
		found=-1
		ident=comp.ident
		if str(ident).startswith("1-"):
			# first group of components which can give multiple
			# instances: do nothing
			return found
		for i in range(self.count()):
			if self.item(i).component.ident == ident:
				self.item(i).setHidden(state)
				found=i
				break
		return found

	def addPiece(self, comp):
		"""
		adds a Component instance,
		and returns the QListWidgetItem created
		"""
		if self.hideItem(comp,False) >= 0: return
		blockItem = QListWidgetItem(self)
		comp.toListWidgetItem(blockItem)
		return blockItem

	def currentComponent(self):
		item = self.currentItem()
		return Component.fromListWidgetItem(item)
		
		
	def startDrag(self, supportedActions):
		component=self.currentComponent()
		drag=component.makeDrag(self)

		if drag.exec_(Qt.MoveAction) == Qt.MoveAction:
			# components of type 1 can be duplicated
			# so they should not be hidden from the list
			if component.mimetype.contains("image/x-Block-1"):
				pass
			elif component.mimetype.contains("image/x-Block-2"):
				self.currentItem().setHidden(True)
		return



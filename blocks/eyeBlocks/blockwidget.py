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

from PyQt4.QtCore import QPoint, QRect, Qt, QSize, QString, \
	QTimer, pyqtSignal

from PyQt4.QtGui import QWidget, QPixmap, QSizePolicy, QColor, \
		QPainter, QListWidget, QListWidgetItem, QMainWindow, \
		QListView, QDialog

from component import Component, InputComponent
from timecomponent import TimeComponent
#from modifcomponent import ModifComponent
#from channelcomponent import ChannelComponent
from inputdialog import Dialog as InputDialog


class BlockWidget(QWidget):
	"""
	This simple widget is used to paint component blocks, and
	manage interactions with the user.
	"""
	blocksChanged = pyqtSignal()
	
	def __init__(self, parent=None):
		super(BlockWidget, self).__init__(parent)

		self.comp = None #dragged component
		self.components = []
		self.hots = [] # list of matching snap points

		self.setAcceptDrops(True)
		self.setMinimumSize(400, 400)
		self.hotPx={
			"red": QPixmap(":/hot/hot-red.svg"),
		}

	def clear(self):
		self.components = []
		self.hots=[]
		self.update()

	def dragEnterEvent(self, event):
		if Component.acceptedFormats(event):
		   event.accept()
		else:
			event.ignore()

	def dragMoveEvent(self, event):
		f=Component.acceptedFormats(event)
		if f:
			data = event.mimeData().data(f[0])
			comp, dataStream, className = Component.unserialize(data)
			offset=comp.hotspot
			# temporarily erase previous hot marks
			previouslyHots=self.hots
			self.hots=[]
			match=False
			for sp in comp.snapPoints:
				hovering=event.pos()-offset+sp
				for flavors in Component.matchingFlavors:
					for m in self.matchingComponentSnap(hovering,sp,flavors):
						self.hots.append(m[0].rect.topLeft()+m[1])
						match=True
			if match or len(previouslyHots) != len(self.hots):
				self.update()
				
							
			event.setDropAction(Qt.MoveAction)
			event.accept()
		else:
			event.ignore()
		return

	def matchingComponentSnap(self, pos, snapPoint, flavors):
		"""
		finds components underlying a snap point, with given position
		and a couple of flavors
		:param pos: the current position of the snap point
		:type pos:
		:param snapPoint: the snap point
		:type snapPoint:
		:param flavors: a couple of texts for matching snap points
		:type flavors:
		:returns: a list of matching component and its snapPoint
		"""
		result=[]
		# to implement symmetry in the flavor's relation
		for f in flavors, (flavors[1], flavors[0]):
			if str(snapPoint.text).startswith(f[0]):
				for c in self.components:
					for s in c.snapPoints:
						if str(s.text).startswith(f[1]):
							gap=c.rect.topLeft()+s-pos
							if gap.manhattanLength() < 60:
								result.append((c, s))
		return result


	def dropEvent(self, event):
		comp, dataStream, className = Component.unserializeFromEvent(event)
		if comp:
			self.components.append(comp)
			self.update(comp.rect)
			self.connectSnaps()
			event.setDropAction(Qt.MoveAction)
			event.accept()
			self.blocksChanged.emit()
		else:
			event.ignore()

	def connectSnaps(self):
		"""
		moves components until every connected snaps overlap
		"""
		toMove=[] # list of components to move
		for c in self.components: c.reset()
		for c in self.components:
			c.touch()
			for s in c.snapPoints:
				p=c.rect.topLeft()+s
				for flavors in Component.matchingFlavors:
					for c1, s1 in self.matchingComponentSnap(p,s,flavors):
						# do not move already touched components
						if c1.touched_: continue
						toMove.append((c,s,c1,s1))
						c1.touch()
		for c,s,c1,s1 in toMove:
			delta=c.rect.topLeft()+s-c1.rect.topLeft()-s1
			c1.rect.translate(delta)
		self.update()
		QTimer.singleShot(1000, self.hideHots)
		return

	def hideHots(self):
		self.hots=[]
		self.update()

	def mousePressEvent(self, event):
		if event.buttons() == Qt.LeftButton:
			comps=self.targetComps(event.pos())
			if not comps:
				return
			comp = comps[-1]
			index=self.components.index(comp)
			comp=copy.copy(comp)

			del self.components[index]

			self.update(comp.rect)

			comp.hotspot=QPoint(event.pos() - comp.rect.topLeft())
			drag=comp.makeDrag(self)

			if drag.exec_(Qt.MoveAction) != Qt.MoveAction:
				self.components.insert(index, comp)
				self.update()
			else:
				self.blocksChanged.emit()

		elif event.buttons() == Qt.RightButton:
			b=self.blockAt(event.pos())
			if b:
				i = self.components.index(b)
				if isinstance(b, InputComponent):
					box=self.parent().parent().parent().boxModel
					d=InputDialog(self, box=box)
					if isinstance(b, TimeComponent):
						d.setTimeBase(b.delay, b.npoints)
					result=d.exec_()
					if result==QDialog.Accepted:
						index=d.tabWidget.currentIndex()
						label=str(d.tabWidget.tabText(index))
						if "Time" in label:
							t=TimeComponent.fromOther(b)
							t.delay, t.npoints, t.duration=d.timeBase()
							self.components[i]=t
							self.blocksChanged.emit()
				self.update()

	def blockAt(self, pos):
		"""
		:param pos: a QPoint instance
		:type pos:
		:returns: the component at the given position if any, else None
		"""
		result=None
		for c in self.components:
			if c.rect.contains(pos):
				mask=c.pixmap.mask()
				color=QColor(mask.toImage().pixel(
						pos-c.rect.topLeft())
				).getRgb()
				if color[0]==0:
					# not masked pixel
					return c	
		return None

	def paintEvent(self, event):
		painter = QPainter()
		painter.begin(self)
		painter.fillRect(event.rect(), Qt.white)
		
		for c in self.components:
			c.draw(painter)

		# hot indicators
		if self.hots:
			px=self.hotPx["red"]
			middle = QPoint(px.size().width()/2, px.size().height()/2)
		for hot in self.hots:
			# paint a circle around
			painter.drawPixmap(QRect(hot-middle,px.size()),px)
			
		painter.end()

	def targetComps(self, position):
		"""
		returns the list of components
		under a mouse click; the topmost component comes last.
		"""
		comps = [c for c in self.components if c.rect.contains(position)]
		return comps
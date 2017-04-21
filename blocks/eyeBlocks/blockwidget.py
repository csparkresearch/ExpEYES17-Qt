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
		"""The list of components"""
		self.snapped=[]
		"""The list of matching snap points"""
		self.hots = [] 
		"""List of matching snap points to highlight at some moment"""

		self.setAcceptDrops(True)
		self.setMinimumSize(400, 400)
		self.hotPx={
			"red": self.hotIcon("red"),
		}
		self.boxModel=None # the model of the box to compile to
		
	@staticmethod
	def hotIcon(color):
		"""
		gets a hot area with its middle and its icon
		
		:param color: some color
		:type color: str
		:returns: the center and the pixmap of a hot area
		:rtype: tuple(QPoint, QPixmap)
		"""
		px=QPixmap(":/hot/hot-%s.svg" %color)
		middle=QPoint(px.size().width()/2, px.size().height()/2)
		return middle, px

	def clear(self):
		self.components = []
		self.snapped=[]
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
					m=self.matchingComponentSnap(hovering,sp,flavors)
					if m:
						s=m[0] # nearest matchin snappoint
						self.hots.append(s.pos())
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
		:param pos: the current mouse position
		:type pos: QPoint
		:param snapPoint: the snap point
		:type snapPoint: SnapPoint
		:param flavors: a couple of texts for matching snap points, if a text is empty, it is a match-all flavor
		:type flavors: tuple(str, str)
		:returns: a list of matching snap points, ordered from the nearest ot the furthest
		:rtype: list(SnapPoint)
		"""
		"""
		def distance(sp):
			return (sp.pos()-pos).manhattanLength()
		"""
		def distance(*args):
			sp=args[0]
			return (sp.pos()-pos).manhattanLength()
			
		result=[]
		# to implement symmetry in the flavor's relation
		for f in flavors, (flavors[1], flavors[0]):
			if not f[0] or str(snapPoint.text).startswith(f[0]):
				for c in self.components:
					for s in c.snapPoints:
						if not f[1] or str(s.text).startswith(f[1]):
							if distance(s) < 60:
								result.append(s)
		result.sort(key=distance)
		return result


	def dropEvent(self, event):
		comp, dataStream, className = Component.unserializeFromEvent(event)
		if comp:
			self.components.append(comp)
			self.update(comp.rect)
			self.connectSnaps(comp)
			event.setDropAction(Qt.MoveAction)
			event.accept()
			self.blocksChanged.emit()
		else:
			event.ignore()
			
	def areSnappedComponents(self, c1, c2, symmetric=False):
		"""
		finds out whether two components are snapped together.
		Depends on self.snapped to be up to date
		
		:param c1: a component or its index in self.components
		:type c1: Component or int
		:param c2: a component or its index in self.components
		:type c2: Component or int
		:param symmetric: when true, the order of c1 and c2 does not matter; False by default
		:type symmetric: boolean
		:returns: tuple of connected snapPoints or None
		:rtype: tupe(SnapPoint, SnapPoint)
		"""
		result=None
		if type(c1)==int: c1=self.components[c1]
		if type(c2)==int: c2=self.components[c2]
		if c1.samePlace(c2): # a component is not snapped to itself
			return result
		# snapPoints for c1
		la=[s for s in self.snapped if s.parent.samePlace(c1)]
		# snapPoints for c2
		lb=[s for s in self.snapped if s.parent.samePlace(c2)]
		if la and lb:
			for sa in la:
				for sb in lb:
					if sa.pos() == sb.pos():
						if symmetric:
							result=(sa,sb)
							break
						else:
							if "-out-" in str(sa.text) and \
								"-in-" in str(sb.text):
								result=(sa,sb)
								break
		return result
		
	def allSnaps(self):
		"""
		:returns: a list of all snap points
		:rtype: list(SnapPoint)
		"""
		result=[]
		for c in self.components:
			for s in c.snapPoints:
				result.append(s)
		return result

	def notSnapped(self):
		"""
		:returns: a list of components with their snaps not connected
		:rtype: list(Component, SnapPoint)
		"""
		return [cs for cs in self.allSnaps() if cs not in self.snapped]
		
	def connectSnaps(self, distinguished=None):
		"""
		moves components until every connected snaps overlap.
		updates the list of connected snaps, self.snapped.
		When distinguished is not None, reorders moved components
		so they appear near the end of the component list.
		
		:param Component distinguished: a particular component, which can be moved or None (which means that every component can be moved)
		"""
		self.snapped=[]
		toMove=[] # list of components to move
		if distinguished:
			movable=[distinguished]
		else:
			movable=self.components
		for c in self.components: c.reset()
		for c in movable:
			c.touch()
			for s in c.snapPoints:
				p=c.rect.topLeft()+s
				for flavors in Component.matchingFlavors:
					m=self.matchingComponentSnap(p,s,flavors)
					if m:
						s1=m[0]
						# do not move already touched components
						if s1.parent.touched: continue
						toMove.append((s,s1))
						s1.parent.touch()
		for s,s1 in toMove: # the 
			delta=s1.pos()-s.pos()
			s.parent.rect.translate(delta)
			self.snapped.append(s); self.snapped.append(s1)
		if distinguished:
			# reorder the component list to put some components near the top
			onTop=[s1.parent for s,s1 in toMove]+[distinguished]
			self.components.sort(lambda x,y: 1 if x in onTop else -1)
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
			### delete the component
			del self.components[index]
			### delete broken snappoints
			brokensnapIndexes=[]
			for sp in comp.snapPoints:
				for i in range(len(self.snapped)):
					s = self.snapped[i]
					if sp.pos() == s.pos():
						brokensnapIndexes.append(i)
			# assert: brokensnapIndexes is a sorted list, ascending
			for i in brokensnapIndexes[::-1]: # descending iteration
				del self.snapped[i]
			### deletions done, erase the images
			self.update(comp.rect)

			comp.hotspot=QPoint(event.pos() - comp.rect.topLeft())
			drag=comp.makeDrag(self)

			if drag.exec_(Qt.MoveAction) != Qt.MoveAction:
				# the drag failed, restore the previous state
				self.components.insert(index, comp)
				self.connectSnaps()
				self.update()
			else:
				self.blocksChanged.emit()

		elif event.buttons() == Qt.RightButton:
			b=self.blockAt(event.pos())
			if b:
				i = self.components.index(b)
				if isinstance(b, InputComponent):
					box=self.boxModel
					d=InputDialog(self, box=box)
					if isinstance(b, TimeComponent):
						d.manageTime(b, self)
					else: # the instance is not yet customized
						d.manageVoltage(b, self)
		return
		
	def blockAt(self, pos):
		"""
		gets the block visible under the mouse cursor
		
		:param pos: position of the mouse
		:type pos: QPoint
		:returns: the component at the given position if any, else None
		:rtype: Component or subclass
		"""
		result=None
		for c in self.components:
			if c.rect.contains(pos):
				mask=c.pixmap.mask()
				color=QColor(mask.toImage().pixel(
						pos-c.rect.topLeft())
				).getRgb()
				if color[0]==0:
					# this pixel is not masked, so return
					return c	
		return None

	def paintEvent(self, event):
		"""
		routine to paint components of the list
		"""
		painter = QPainter()
		painter.begin(self)
		painter.fillRect(event.rect(), Qt.white)
		
		for c in self.components:
			c.draw(painter)

		# hot indicators
		if self.hots:
			middle,px=self.hotPx["red"]
		for hot in self.hots:
			painter.drawPixmap(QRect(hot-middle,px.size()),px)
			
		painter.end()

	def targetComps(self, position):
		"""
		returns the list of components
		under a mouse click; the topmost component comes last.
		"""
		comps = [c for c in self.components if c.rect.contains(position)]
		return comps

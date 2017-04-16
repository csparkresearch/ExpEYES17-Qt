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

import os, re
from PyQt4 import QtCore, QtGui
from xml.dom.minidom import parseString

import blocks_rc

def acceptedFormats(event):
	"""
	acceptable formats start with "image/x-Block-"
	returns a list of accepted formats.
	"""
	return [f for f in event.mimeData().formats() \
			if f.contains("image/x-Block-")]

class SnapPoint(QtCore.QPoint):
	def __init__(self, x, y, text):
		QtCore.QPoint.__init__(self, x, y)
		self.text=text
		return

	def __str__(self):
		return "snapPoint((%s,%s),%s)" %(self.x(), self.y(), self.text)
		
class Component(object):
	"""
	This class describes a programmation component, which can be
	organized with other instances. It features a widget, summarized
	by an icon, and each icon has some points which can be linked
	to other components.
	
	When a collection of components are organized on top of some
	canvas, they can be compiled into some usable program.
	"""
	def __init__(self, pixmap, ident, mimetype, rect=None, hotspot=None,
					snapPoints=[]):
		"""
		The constructor
		@param pixmap a drawing to make an icon, and able to suggest
		the function of the component
		@param ident an identifier
		@param mimetype a type which decides some behaviors in the user
		interface
		@param rect the surrounding rectangle; defaults to None, which
		will define rect as surrounding the given pixmap
		@param hotspot the position of the mouse during the drag of
		the pixmap
		"""
		super(Component, self).__init__()
		if rect:
			self.rect=rect
		else:
			self.rect=pixmap.rect()
		if hotspot:
			self.hotspot=hotspot
		else:
			self.hotspot=QtCore.QPoint(pixmap.width()/2, pixmap.height()/2)
		self.pixmap=pixmap
		self.ident=ident
		self.mimetype=mimetype
		self.snapPoints=snapPoints
		return
		
	def __str__(self):
		return "Component(\n  %s,\n  %s,\n  rect: %s,\n  hotspot: %s,\n  snaps: %s)" \
					%(self.ident, self.mimetype, self.rect, self.hotspot,
						self.snapPoints
					)		

	def serialize(self):
		"""
		serializes a component into a QDataStream
		returns data as a QByteArray instance
		"""
		itemData = QtCore.QByteArray()
		dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
		dataStream << self.pixmap << self.mimetype \
				<< self.hotspot << self.ident \
				<< QtCore.QVariant(len(self.snapPoints))
		for sp in self.snapPoints:
			dataStream << QtCore.QPoint(sp) << QtCore.QString(sp.text)
		return itemData
		
	@staticmethod
	def fromListWidgetItem(lwi):
		"""
		creates ans returns a Component instance read from
		a QListWidgetItem instance
		"""
		return lwi.component
		
	def toListWidgetItem(self, lwi):
		"""
		records custom data into a QListWidgetItem instance
		"""
		lwi.component=self
		lwi.setIcon(QtGui.QIcon(self.pixmap))
		"""
		byteArray=self.serialize()
		lwi.setData(QtCore.Qt.UserRole, byteArray)
		"""
		return
		
	@staticmethod
	def unserialize(data):
		"""
		unserialize frome a byteArray,
		@return a new Component instance
		"""
		dataStream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)
		pixmap = QtGui.QPixmap()
		mimetype = QtCore.QString()
		ident = QtCore.QString()
		hotspot = QtCore.QPoint()
		length = QtCore.QVariant()
		dataStream >> pixmap >> mimetype >> hotspot >> ident >> length
		length, report = length.toInt()
		sp=[]
		for i in range(length):
			point=QtCore.QPoint()
			text=QtCore.QString()
			dataStream >> point >> text
			sp.append(SnapPoint(point.x(), point.y(), text))
		return Component(pixmap,ident,mimetype,hotspot=hotspot,snapPoints=sp)
		
	@staticmethod
	def unserializeFromEvent(event):
		"""
		userialize given QEvent's data into a Component instance
		@param event a QEvent, presumably due to a drop.
		@return an instance of Component 
		"""
		f = acceptedFormats(event)
		if f:
			data = event.mimeData().data(f[0])
			result=Component.unserialize(data)
			result.rect = QtCore.QRect(
					(event.pos()-result.hotspot),
					result.pixmap.size()
			)
		else:
			result = None
		return result

	@staticmethod
	def listFromRC():
		"""
		gets a list of components from the application's QRC file
		"""
		componentDirPattern = re.compile(r"components(.)")
		result=[]
		# browse top-level directories of the resource file
		for rcDir in sorted(QtCore.QDir(":/").entryList()):
			# directory's name matches r"components(.)" ???
			m=componentDirPattern.match(rcDir)
			if not m:
				continue
			else:
				mimetype = "image/x-Block-"+m.group(1)
			d=QtCore.QDir(":/"+rcDir)
			# browse SVG files contained in those directories
			for entry in sorted(d.entryList()):
				imgPath=":/"+rcDir+"/"+entry
				img=QtGui.QPixmap(imgPath)
				sp=snapPoints(imgPath)
				result.append(Component(img, entry, mimetype, snapPoints=sp))
		return result
		
	def makeDrag(self, parent):
		"""
		creates and returns a QDrag object with the given parent
		@param parent a window, where a drag is starting
		@return the DQrag instance
		"""
		itemData = self.serialize()

		mimeData = QtCore.QMimeData()
		mimeData.setData(self.mimetype, itemData)

		drag = QtGui.QDrag(parent)
		drag.setMimeData(mimeData)
		drag.setHotSpot(self.hotspot)
		drag.setPixmap(self.pixmap)
		return drag
		
def snapPoints(rcpath):
	"""
	@result a list of snapPoints. Those are centers of circles
	available in the SVG picture, denoted byids which begin with
	"block-";those circles may be invisible in the pixmap.
	"""
	f=QtCore.QFile(rcpath)
	f.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text)
	svg=f.readAll()
	f.close()
	svgDoc=parseString(svg)
	firstgroup=svgDoc.getElementsByTagName("g")[0]
	trans=firstgroup.getAttribute("transform")
	xt,yt=re.match(r"translate\((.*),(.*)\)",trans).groups()
	xt=float(xt);yt=float(yt)
	circles=svgDoc.getElementsByTagName("circle")
	snapCircles=[c for c in circles \
				 if re.match(r"^block-",c.getAttribute("id"))]
	result=[]
	for c in circles:
		xc=float(c.getAttribute("cx"))
		yc=float(c.getAttribute("cy"))
		id_=c.getAttribute("id")
		result.append(SnapPoint(xc+xt, yc+yt, id_))
	return result
	
if __name__=="__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	Component.listFromRC()

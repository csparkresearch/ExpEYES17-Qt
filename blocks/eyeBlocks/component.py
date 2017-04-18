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

from templates import blocks_rc

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

	"""
	pairs of maching flavors for snap points
	"""
	matchingFlavors=[
		("block-in-signal", "block-out-signal"),
	]
	
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
		self.touched_=False
		return

	def reset(self):
		"""
		resets the touched_ flag
		"""
		self.touch(False)
		return

	@staticmethod
	def acceptedFormats(event):
		"""
		acceptable formats start with "image/x-Block-"
		returns a list of accepted formats.
		"""
		return [f for f in event.mimeData().formats() \
				if f.contains("image/x-Block-")]

	def touch(self, touched=True):
		"""
		sets the touch_ flag
		@param touched value for the flag; True by default
		"""
		self.touched_=touched
		return

	@classmethod
	def fromOther(cls, c):
		"""
		alternate constructor
		@param c a component
		"""
		self=cls(c.pixmap, c.ident, c.mimetype, c.rect, c.hotspot, c.snapPoints)
		self.initDefaults()	
		return self

	def initDefaults(self):
		"""
		abstract method to override by subclasses, to init more properties
		"""
		return

	def __str__(self):
		return "Component(\n  %s,\n  %s,\n  rect: %s,\n  hotspot: %s,\n  snaps: %s)" \
					%(self.ident, self.mimetype, self.rect, self.hotspot,
						self.snapPoints
					)

	def draw(self, painter):
		"""
		draws a component inside a widget with the help of a painter
		@param painter a working QPainter instance
		"""
		painter.drawPixmap(self.rect, self.pixmap)
		return
		
	def save(self, outstream):
		"""
		saving to an open binary stream
		"""
		itemData, dataStream = self.serialize()
		outstream.write("Class Name (%s bytes)\n" %len(self.className()))
		outstream.write("%s\n" %self.className())
		outstream.write("Blob (%s bytes)\n" %len(itemData))
		outstream.write(itemData)
		return
		
	def className(self):
		return re.match(
			r"<class '.*component\.(.*)'>",
			str(self.__class__)
		).group(1)

	def serialize(self):
		"""
		serializes a component into a QDataStream
		returns data as a QByteArray instance and a writeStream to feed it on
		"""
		itemData = QtCore.QByteArray()
		dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
		dataStream << QtCore.QString(self.className()) \
		        << self.rect << self.pixmap << self.mimetype \
				<< self.hotspot << self.ident \
				<< QtCore.QVariant(len(self.snapPoints))
		for sp in self.snapPoints:
			dataStream << QtCore.QPoint(sp) << QtCore.QString(sp.text)
		self.putMoreData(dataStream)
		return itemData, dataStream

	def putMoreData(self, dataStream):
		"""
		abstract metho to be overriden by subclasses
		"""
		return
		
	def getMoreData(self, dataStream):
		"""
		abstract metho to be overriden by subclasses
		"""
		return
		
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
		return
		
	@staticmethod
	def unserialize(data):
		"""
		unserialize frome a byteArray,
		@return a new Component instance, a dataStream to get further data,
		and the className to restore
		"""
		from timecomponent import TimeComponent
		from modifcomponent import ModifComponent
		from channelcomponent import ChannelComponent
		dataStream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)
		className=QtCore.QString()
		rect=QtCore.QRect()
		pixmap = QtGui.QPixmap()
		mimetype = QtCore.QString()
		ident = QtCore.QString()
		hotspot = QtCore.QPoint()
		length = QtCore.QVariant()
		dataStream >> className >> rect >> pixmap >> mimetype >> \
			hotspot >> ident >> length
		length, report = length.toInt()
		sp=[]
		for i in range(length):
			point=QtCore.QPoint()
			text=QtCore.QString()
			dataStream >> point >> text
			sp.append(SnapPoint(point.x(), point.y(), text))
		# carefully restore the class of the dropped object	
		result=eval(
			"%s(pixmap,ident,mimetype,rect=rect,hotspot=hotspot,snapPoints=sp)" %className
		)
		return result, dataStream, className
		
	@staticmethod
	def unserializeFromEvent(event):
		"""
		userialize given QEvent's data into a Component instance
		@param event a QEvent, presumably due to a drop.
		@return an instance of Component and a dataStream to get more data
		"""
		from timecomponent import TimeComponent
		from modifcomponent import ModifComponent
		from channelcomponent import ChannelComponent
		f = Component.acceptedFormats(event)
		if f:
			data = event.mimeData().data(f[0])
			result, dataStream, className = Component.unserialize(data)
			result.rect = QtCore.QRect(
					(event.pos()-result.hotspot),
					result.pixmap.size()
			)
			result=eval("%s.fromOther(result)" %className)
			result.getMoreData(dataStream)
		else:
			result = None; dataStream=None
		return result, dataStream, className

	@staticmethod
	def listFromRC():
		"""
		gets a list of components from the application's QRC file
		"""
		#import modifcomponent
		from modifcomponent import ModifComponent
		from channelcomponent import ChannelComponent

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
				if "input" in entry:
					result.append(InputComponent(img, entry, mimetype, snapPoints=sp))
				elif "modif" in entry:
					result.append(ModifComponent(img, entry, mimetype, snapPoints=sp))
				elif "channel" in entry or "abscissa" in entry:
					result.append(ChannelComponent(img, entry, mimetype, snapPoints=sp))
				else:
					print("Error, this should not happen:", entry)	
					result.append(Component(img, entry, mimetype, snapPoints=sp))
		return result
		
	def makeDrag(self, parent):
		"""
		creates and returns a QDrag object with the given parent
		@param parent a window, where a drag is starting
		@return the DQrag instance
		"""
		itemData, writeStream = self.serialize()

		mimeData = QtCore.QMimeData()
		mimeData.setData(self.mimetype, itemData)

		drag = QtGui.QDrag(parent)
		drag.setMimeData(mimeData)
		drag.setHotSpot(self.hotspot)
		drag.setPixmap(self.pixmap)
		return drag


		
def snapPoints(rcpath):
	"""
	@return a list of snapPoints. Those are centers of circles
	available in the SVG picture, denoted by ids which begin with
	"block-"; those circles may be invisible in the pixmap.
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

class InputComponent(Component):
	"""
	An abstract class which can be used for time, and voltage inputs
	"""	
	def __init__(*args,**kw):
		Component.__init__(*args,**kw)
	
if __name__=="__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	Component.listFromRC()

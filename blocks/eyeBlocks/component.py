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

import os, re, copy
from PyQt4 import QtCore, QtGui
from xml.dom.minidom import parseString

def _translate(context, text, disambig):
	return QtGui.QApplication.translate(context, unicode(text), disambig)
        

from templates import blocks_rc

class SnapPoint(QtCore.QPoint):
	"""
	defines a snap point where a component can stick to another one.
	Each snap point has a text attribute which rules its behavior to
	other snap points (see the variable matchingFlavors).
	
	:param relpos: the position of the snap point in the related pixmap
	:type relpos: QPoint
	:param text: the text which will define the flavor
	:type text: str
	:param parent: the component owning this snap point
	:type parent: Component or subclass
	"""
	def __init__(self, relpos, text, parent=None):
		QtCore.QPoint.__init__(self, relpos)
		self.text=text
		self.parent=parent
		return

	def __str__(self):
		return "snapPoint((%s,%s),%s)" %(self.x(), self.y(), self.text)
		
	def pos(self):
		"""
		:returns: the position of the snap point in the working area
		:rtype: QPoint
		"""
		return self.parent.rect.topLeft()+self
		
	
class Component(object):
	"""
	This class describes a programmation component, which can be
	organized with other instances. It features a widget, summarized
	by an icon, and each icon has some points which can be linked
	to other components.
	
	When a collection of components are organized on top of some
	canvas, they can be compiled into some usable program.
	
	:param pixmap: a drawing to make an icon, and able to suggest the function of the component
	:type pixmap: QPixmap
	:param ident: an identifier
	:type ident: QString
	:param mimetype: a type to decide some behaviors in the user interface
	:type mimetype: QString
	:param rect: the surrounding rectangle; defaults to None, which will define rect as surrounding the given pixmap
	:type rect: QRect
	:param hotspot: the position of the mouse during the drag of the pixmap
	:type hotspot: QPoint
	"""

	matchingFlavors=[
		("block-in-signal", "block-out-signal"),
		("block-in-signal-x", "block-out-time"),
	]
	"""
	pairs of maching flavors for snap points
	"""
	
	def __init__(self, pixmap, ident, mimetype, rect=None, hotspot=None,
					snapPoints=[]):
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
		for s in self.snapPoints:
			s.parent=self
		self.touched=False
		return

	def summary(self):
		"""
		:returns: a simple description for humans
		:rtype: str
		"""
		return "%s at (%s,%s)" % (self.className(),
					self.rect.topLeft().x(), self.rect.topLeft().y())
		
	def reset(self):
		"""
		resets the touched flag
		"""
		self.touch(False)
		return
		
	def samePlace(self, other):
		"""
		finds whether a component is at the same place than another
		
		:param other: anoter component
		:type other: Component or subclass
		:returns: True if both components are at the same place
		:rtype: boolean
		"""
		return self.rect==other.rect
		
	@staticmethod
	def acceptedFormats(event):
		"""
		acceptable formats start with "image/x-Block-".
		
		:param event: the current event.
		:type event: QEvent
		:returns: a list of accepted formats.
		:rtype: list(QString)
		"""
		return [f for f in event.mimeData().formats() \
				if f.contains("image/x-Block-")]

	def touch(self, touched=True):
		"""
		sets the touch flag

		:param touched: value for the flag; True by default
		:type touched: boolena
		"""
		self.touched=touched
		return

	@classmethod
	def fromOther(cls, c):
		"""
		alternate constructor

		:param c: a Component instance
		:type c: Component or subclass
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
		draws a component inside a widget with the help of a painter.

		:param painter: a working QPainter instance
		:type painter: QPainter
		"""
		painter.drawPixmap(self.rect, self.pixmap)
		return
		
	def save(self, outstream):
		"""
		saving to a writable stream
		
		:param outstream: a writable stream
		:type outstream: QtCore.QIODevice.WriteOnly
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
		serializes a component into a byte array.
		
		:returns: a byte array and a writable stream to feed it.
		:rtype: tuple(QByteArray,QIODevice.WriteOnly)
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
		
		:param dataStream: writable data stream connected to a byte array
		:type dataStream: QIODevice.WriteOnly
		"""
		return
		
	def getMoreData(self, dataStream):
		"""
		abstract metho to be overriden by subclasses
		
		:param dataStream: readable data stream connected to a byte array
		:type dataStream: QIODevice.ReadOnly
		"""
		return
		
	@staticmethod
	def fromListWidgetItem(lwi):
		"""
		creates ans returns a Component instance read from 
		a QListWidgetItem instance. Modifies its pixmap when
		the component may be customized later, in order to
		keep a clean print area.
		
		:param lwi: the item containing a component to Drag
		:type lwi: QListWidgetItem
		:returns: copy of a Component
		:rtype: Component or subclass
		"""
		result = copy.copy(lwi.component)
		if "input" in str(result.ident):
			result.pixmap=QtGui.QPixmap(":/misc/0-input.svg")
		elif "time" in str(result.ident):
			result.pixmap=QtGui.QPixmap(":/misc/0-timebase.svg")
		return result
		
	def toListWidgetItem(self, lwi):
		"""
		records custom data into a QListWidgetItem instance.
		
		:param lwi: the item containing a component to Drag
		:type lwi: QListWidgetItem
		"""
		lwi.component=self
		lwi.setIcon(QtGui.QIcon(self.pixmap))
		return
		
	@staticmethod
	def unserialize(data):
		"""
		unserialize frome a byteArray.
		
		:param data: a byte array
		:type data: QByteArray
		:returns: a new Component instance, a data stream to get further data, and the name of the class to restore.
		:rtype: tuple(Component or subclass, QIODevice.ReadOnly, QString)
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
			sp.append(SnapPoint(point, text, None))
		# carefully restore the class of the dropped object	
		result=eval(
			"%s(pixmap,ident,mimetype,rect=rect,hotspot=hotspot,snapPoints=sp)" %className
		)
		return result, dataStream, className
		
	@staticmethod
	def unserializeFromEvent(event):
		"""
		userialize given QEvent's data into a Component instance

		:param event: an event due to a drop.
		:type event: QEvent
		:returns: an instance of Component, a data stream to get more data, and the name of the class to restore.
		:rtype: tuple(Component or subclass, QIODevice.ReadOnly, QString)
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
		
		:returns: a list of components
		:rtype: list(Component or subclass)
		"""
		from timecomponent import TimeComponent
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
				elif "time" in entry:
					result.append(TimeComponent(img, entry, mimetype, snapPoints=sp))
				elif "channel" in entry or "abscissa" or "scope"in entry:
					result.append(ChannelComponent(img, entry, mimetype, snapPoints=sp))
				else:
					print(unicode(_translate("eyeBlocks.component","Error, this should not happen:",None)), entry)	
					result.append(Component(img, entry, mimetype, snapPoints=sp))
		return result
		
	def makeDrag(self, parent):
		"""
		creates and returns a QDrag object with the given parent

		:param parent: a window, where a drag is starting
		:type parent: QWidget
		:returns: a drag object
		:rtype: QDrag
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
	:returns: a list of snap points. Those are centers of circles available in the SVG picture, denoted by ids which begin with "block-"; those circles may be invisible in the pixmap.
	:rtype: list(SnapPoint)
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
		result.append(SnapPoint(QtCore.QPoint(xc+xt, yc+yt), id_))
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

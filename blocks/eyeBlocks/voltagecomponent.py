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

from PyQt4 import QtCore, QtGui
from component import InputComponent, Component

def _translate(context, text, disambig):
	return QtGui.QApplication.translate(context, unicode(text), disambig)
        

class VoltageComponent(InputComponent):
	"""
	A component to implement a voltage input
	"""

	def __init__(*args,**kw):
		InputComponent.__init__(*args,**kw)
		self=args[0]
		self.initDefaults()
		for a in ("name","ranges","rangeindex"):
			if a in kw:
				setattribute(self, a, kw[a])

	def initDefaults(self):
		self.name="A1"
		self.ranges=[(-5,5)]
		self.rangeindex = 0


	def draw(self, painter):
		super(VoltageComponent, self).draw(painter)
		lh=12 # lineheight
		x=10;y=15
		pos=self.rect.topLeft()
		titlePos=pos+QtCore.QPoint(x,y)
		x=15; y+=lh
		namePos=pos+QtCore.QPoint(x,y)
		y+=lh
		rangePos=pos+QtCore.QPoint(x,y)
		painter.drawText(titlePos,_translate("eyeBlocks.voltagecomponent","Voltage input",None))
		painter.drawText(namePos,_translate("eyeBlocks.timecomponent","%1",None).arg(self.name))
		painter.drawText(rangePos,_translate("eyeBlocks.timecomponent","range: %1V..%2V",None).arg(self.ranges[self.rangeindex][0]).arg(self.ranges[self.rangeindex][1]))

	def getMoreData(self, dataStream):
		name=QtCore.QString()
		ranges=QtCore.QString() # will require an evaluation
		rangeindex=QtCore.QVariant()
		dataStream >> name >> ranges >> rangeindex
		self.name=str(name)
		self.ranges=eval(str(ranges))
		self.rangindex, report=rangeindex.toInt()
		return

	def putMoreData(self, dataStream):
		dataStream << QtCore.QString(self.name) << QtCore.QString(str(self.ranges)) << QtCore.QVariant(self.rangeindex)
		return

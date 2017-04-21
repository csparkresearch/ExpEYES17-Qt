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
        

class TransmitComponent(InputComponent):
	"""
	A component to transmit a signal, while featuring side effects,
	like refreshing a voltage display, triggering the scope, multiplying
	or shifting the voltage, etc.
	
	:key bool display: if True, a voltage display will be added
	:key str css: a style sheet for the display
	:key function: a Python function with profile: f(float) -> float
	:key bool trigger: if True, the signal will trigger the scope
	"""

	def __init__(*args,**kw):
		InputComponent.__init__(*args,**kw)
		self=args[0]
		self.initDefaults()
		for a in ("display","css", "function", "trigger"):
			setattr(self, a, kw.get(a,None))
		if not self.css: self.css=""
		if not self.function: self.function=""

	def initDefaults(self):
		return


	def draw(self, painter):
		super(TransmitComponent, self).draw(painter)
		lh=12 # lineheight
		x=10;y=15
		pos=self.rect.topLeft()
		p=pos+QtCore.QPoint(x,y)
		painter.drawText(p,_translate("eyeBlocks.voltagecomponent","Display: %1",None).arg("%s" %self.display))
		x=15; y+=lh
		p=pos+QtCore.QPoint(x,y)
		try:
			code="fun=lambda x: %s" %self.function
			obj=compile(code,"fakemodule","single")
			exec(obj)
			result=callable(fun)
		except:
			result=False
		painter.drawText(p,_translate("eyeBlocks.voltagecomponent","Function: %1",None).arg("%s" %result))
		y+=lh
		p=pos+QtCore.QPoint(x,y)
		painter.drawText(p,_translate("eyeBlocks.voltagecomponent","Trigger: %1",None).arg("%s" %self.trigger))

	def getMoreData(self, dataStream):
		display=QtCore.QVariant()
		css=QtCore.QString()
		function=QtCore.QString() # will require an evaluation
		trigger=QtCore.QVariant()
		dataStream >> display >> css >> function >> trigger
		self.display=display.toBool()
		self.css=str(css)
		self.function=str(function)
		self.trigger=trigger.toBool()
		return

	def putMoreData(self, dataStream):
		dataStream << QtCore.QVariant(self.display) << QtCore.QString(self.css) << QtCore.QString(self.function) << QtCore.QVariant(self.trigger)
		return

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

from templates.ui_transmits import Ui_Dialog
from transmitcomponent import TransmitComponent

class Dialog(QtGui.QDialog, Ui_Dialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self,parent)
		Ui_Dialog.__init__(self)
		self.setupUi(self)
		return
		
		
	def manageTransmit(self, b, bw):
		"""
		manages the modification of a time component.
		
		:param b: an input component
		:type b: TransmitComponent
		:param bw: working area
		:type bw: BlockWidget
		"""
		self.displayCheck.setChecked(b.display)
		self.triggerCheck.setChecked(b.trigger)
		if b.css:
			self.cssEdit.clear() # removes the predefined style
			self.cssEdit.insertPlainText(b.css)
		self.lambdaEdit.setText(b.function)
		result=self.exec_()
		if result==QtGui.QDialog.Accepted:
			t=TransmitComponent.fromOther(b)
			t.display=self.displayCheck.checkState()==QtCore.Qt.Checked
			t.trigger=self.triggerCheck.checkState()==QtCore.Qt.Checked
			t.css=self.cssEdit.toPlainText()
			t.function=self.lambdaEdit.text()
			bw.components[bw.components.index(b)]=t
			bw.blocksChanged.emit()
			bw.update()
		return

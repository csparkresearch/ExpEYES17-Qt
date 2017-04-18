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

from templates.ui_inputs import Ui_Dialog

class Dialog(QtGui.QDialog, Ui_Dialog):
	def __init__(self, parent=None, box="expeyes-17"):
		QtGui.QDialog.__init__(self,parent)
		Ui_Dialog.__init__(self)
		self.setupUi(self)
		if box=="expeyes-17":
			import expeyes.eyes17 as eyes
			import expeyes.commands_proto as CP
			delays=[50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]
			samples=sorted([
				1+CP.MAX_SAMPLES/2, 1+CP.MAX_SAMPLES/5, 
				1+CP.MAX_SAMPLES/10, 1+CP.MAX_SAMPLES/20,
				1+CP.MAX_SAMPLES/50, 1+CP.MAX_SAMPLES/100,
				1+CP.MAX_SAMPLES/200, 1+CP.MAX_SAMPLES/500])
			for delay in delays:
				self.delayCombo.addItem(str(delay))
			for np in samples:
				self.sampleCombo.addItem(str(np))
			self.sampleCombo.setCurrentIndex(len(samples)-1)
			self.updateDuration()
			self.delayCombo.currentIndexChanged.connect(self.updateDuration)
			self.delayCombo.editTextChanged.connect(self.updateDuration)
			self.sampleCombo.currentIndexChanged.connect(self.updateDuration)
			self.sampleCombo.editTextChanged.connect(self.updateDuration)
		return
		
	def timeBase(self):
		"""
		get timebase data
		@return delay, samples, duration
		"""
		delay = int(self.delayCombo.currentText())
		samples = int(self.sampleCombo.currentText())
		duration = delay*(samples-1)
		return delay, samples, duration
		
	def setTimeBase(self, delay, samples):
		"""
		set timebase data
		"""
		duration=delay*(samples-1)
		
		for combo, value in (
			(self.durationCombo, duration),
			(self.delayCombo, delay),
			(self.sampleCombo, samples)):
			self.addToCombo(combo, value)
		return
		
	@staticmethod
	def addToCombo(combo, value):
		"""
		adds an integer value to a combo
		"""
		found=combo.findText(str(value))
		if found < 0:
			combo.addItem(str(value))
			found=combo.findText(str(value))
		combo.setCurrentIndex(found)
		return
		
	def updateDuration(self):
		"""
		computes the duration with the formula delay* (samples-1)
		"""
		delay=int(self.delayCombo.currentText())
		self.delayLabel.setText(self.humanDuration(delay))
		duration=(int(self.sampleCombo.currentText())-1) * delay
		self.addToCombo(self.durationCombo, duration)
		self.durationLabel.setText(self.humanDuration(duration))
		return
		
	@staticmethod
	def humanDuration(d):
		"""
		returns a string which humans can read easier
		"""
		v=d;
		u=u"µs"
		result=u
		if v > 500:
			v=1e-3*v
			u=u"ms"
		if v > 500:
			v=1e-3*v
			u=u"s"
		if u!=u"µs":
			result= u"µs (= %s %s)" %(v,u)
		return result
			
		

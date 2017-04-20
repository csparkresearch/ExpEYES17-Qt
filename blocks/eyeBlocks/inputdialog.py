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
		elif box=="expeyes-junior":
			import expeyes.eyesj as eyes
			delays=[50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]
			MAX_SAMPLES=1000
			samples=sorted([
				1+MAX_SAMPLES/2, 1+MAX_SAMPLES/5, 
				1+MAX_SAMPLES/10, 1+MAX_SAMPLES/20,
				1+MAX_SAMPLES/50])
			#### creates tabs for available entries ####
			# following the documentation of expeyes.eyesj:
			nbVoltageInputs=11
			tabData=(1+nbVoltageInputs)*[[]]
			### the list of combos permits to acces choosen ranges
			self.combos=(1+nbVoltageInputs)*[[None]]
			tabData[1]=["A1","-5V to +5V range Analog Input",[-5,5]]
			tabData[2]=["A2","-5V to +5V range Analog Input ",[-5,5]]
			tabData[3]=["IN1 ","Can function as Digital or 0 to 5V Analog Input",[0,5]]
			tabData[4]=["IN2","Can function as Digital or 0 to 5V Analog Input",[0,5]]
			tabData[5]=["SEN", "Like IN1 and IN2, but has a 5K external pullup resistor (Comp input)",[0,5]]
			tabData[6]=["SQR1-read","Input wired to SQR1 output",[0,5]]
			tabData[7]=["SQR2-read"," Input wired to SQR2 output",[0,5]]
			tabData[8]=["SQR1-control, 0 to 5V programmable Squarewave. Setting Freq = 0 means 5V","Freq = -1 means 0V",[0,5]]
			tabData[9]=["SQR2-control","0 to 5V programmable Squarewave",[0,5]]
			tabData[10]=["OD1","Read-back from Digital output OD1",[0,5]]
			tabData[11]=["CCS","Controls the 1mA constant current source. ",[0,5]]
			self.tabWidget.removeTab(1)
		##### for whatever box model, set common time features
		for delay in delays:
			self.delayCombo.addItem(str(delay))
		for np in samples:
			self.sampleCombo.addItem(str(np))
		self.sampleCombo.setCurrentIndex(len(samples)-1)
		self.updateDuration()
		##### for whatever box model, set common voltage features
		for i in range(1,1+nbVoltageInputs):
			# make a tab with a simple widget
			w=QtGui.QWidget()
			self.tabWidget.addTab (w, tabData[i][0])
			# with a vertical layout
			layout=QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom, w)
			# which contains a combo box for ranges
			self.combos[i]=QtGui.QComboBox()
			self.combos[i].addItem(str(tabData[i][2]))
			layout.addWidget(self.combos[i])
			# and a text edit for other informations
			t=QtGui.QTextEdit(self)
			t.setReadOnly(True)
			t.insertHtml("<h1>Expeyes-Junior</h1>")
			t.insertHtml("<br>")
			t.insertHtml("<h2>(fixed voltage ranges)</h2>")
			t.insertHtml("<br>")
			t.insertHtml(tabData[i][1])
			t.insertHtml("<br>")
			layout.addWidget(t)

		self.delayCombo.currentIndexChanged.connect(self.updateDuration)
		self.delayCombo.editTextChanged.connect(self.updateDuration)
		self.sampleCombo.currentIndexChanged.connect(self.updateDuration)
		self.sampleCombo.editTextChanged.connect(self.updateDuration)
		return
		
	def timeBase(self):
		"""
		get timebase data

		:returns: delay, samples, duration
		"""
		delay = int(self.delayCombo.currentText())
		samples = int(self.sampleCombo.currentText())
		duration = delay*(samples-1)
		return delay, samples, duration
		
	def forTimeBase(self, timeinput):
		"""
		set timebase data, and adapt tabs: the only tab remaining
		should be the time tab.
		
		:param timeinput: a timebase component
		:type timeinput: TimeInput
		"""
		duration=timeinput.delay*(timeinput.npoints-1)
		
		for combo, value in (
			(self.durationCombo, duration),
			(self.delayCombo, timeinput.delay),
			(self.sampleCombo, timeinput.npoints)):
			self.addToCombo(combo, value)
		self.tabWidget.setTabEnabled(0,True)
		for i in range(1, self.tabWidget.count()):
			self.tabWidget.setTabEnabled(i,False)
		return
		
	def manageTime(self, b, bw):
		"""
		manages the modification of a time component.
		
		:param b: a time component
		:type b: TimeComponent
		:param bw: working area
		:type bw: BlockWidget
		"""
		from timecomponent import TimeComponent
		self.forTimeBase(b)
		result=self.exec_()
		if result==QtGui.QDialog.Accepted:
			t=TimeComponent.fromOther(b)
			t.delay, t.npoints, t.duration=self.timeBase()
			bw.components[bw.components.index(b)]=t
			bw.blocksChanged.emit()
			bw.update()
		return

		
	def manageVoltage(self, b, bw):
		"""
		manages the modification of a time component.
		
		:param b: an input component
		:type b: InputComponent
		:param bw: working area
		:type bw: BlockWidget
		"""
		from voltagecomponent import VoltageComponent
		#enable only the voltage entries
		self.tabWidget.setTabEnabled(0,False)
		for i in range(1, self.tabWidget.count()):
			self.tabWidget.setTabEnabled(i,True)
		self.tabWidget.setCurrentIndex(1)
		result=self.exec_()
		if result==QtGui.QDialog.Accepted:
			v=VoltageComponent.fromOther(b)
			i=self.tabWidget.currentIndex()
			v.name=str(self.tabWidget.tabText(i))
			v.code=i # asserting codes are a sequence begining at 1!
			v.ranges=[eval(str(self.combos[i].currentText()))]
			v.rangeindex=0
			bw.components[bw.components.index(b)]=v
			bw.blocksChanged.emit()
			bw.update()
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
			
		

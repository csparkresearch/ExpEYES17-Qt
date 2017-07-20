# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from ..Qt import QtGui, QtCore
from ..templates import ui_plotTemplate as plotTemplate
from ..utilities.expeyesWidgetsNew import expeyesWidgets

import sys,time,os
import numpy as np

class AppWindow(QtGui.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	subsection = 'apps'
	helpfile = 'RCcircuit.html'
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		self.widgetLayout.setAlignment(QtCore.Qt.AlignTop)
		self.widgets.setMinimumWidth(250)
		
		self.TITLE('Controls')
		self.PUSHBUTTON('0V to 5V step' , self.ZeroToFive)
		self.PUSHBUTTON('5V to 0V step' , self.FiveToZero)
		#self.PUSHBUTTON('CC Charge' , self.CCCharge)
		self.SPACER(10)
		self.PUSHBUTTON('Calculate RC' , self.calcRC)
		self.tb = self.timebaseWidget(self.getSamples,self.setTimebase); self.widgetLayout.addWidget(self.tb)

		self.p.I.select_range('A1',8)
		self.samples = 200;self.timebase = 2
		self.xdata=None;self.ydata=None

		self.plot = self.newPlot([],detailedWidget=True,xMin=0,xMax = self.timebase*self.samples, bottomLabel = 'time',bottomUnits='S',leftLabel = 'Voltage',leftUnits='V',enableMenu=False,legend=True,autoRange='y')
		self.plot.setYRange(0,5)

		self.region = self.addRegion(self.plot,0,9*4./10)
		self.tb.slider.setValue(5) #4mS . optimum for 1uF 1K combination

	def getSamples(self):
		return self.samples
		
	def setTimebase(self,t):
		self.plot.setLimits(xMin=0,xMax = t*self.samples*1e-6)
		self.timebase = t
		T = t*self.samples*1e-6
		self.plot.setXRange(0, T)
		self.region.setRegion([0,4*T/5])
		
	def ZeroToFive(self):
		val,ok = QtGui.QInputDialog.getText(self,"Name this dataset","",text = "0->5")
		if ok :
			self.p.I.set_state(OD1=0)		# OD1 to LOW
			time.sleep(0.5)
			self.xdata, self.ydata = self.p.I.capture_action('A1',self.samples,self.timebase,'SET_HIGH')
			self.curve = self.addCurve(self.plot,val,self.randomColor())
			self.curve.setData(self.xdata*1e-3,self.ydata) #mS to Seconds
			
	def FiveToZero(self):
		val,ok = QtGui.QInputDialog.getText(self,"Name this dataset","",text = "5->0")
		if ok :
			self.p.I.set_state(OD1=1)		# OD1 to HIGH
			time.sleep(0.5)
			self.xdata, self.ydata = self.p.I.capture_action('A1',self.samples,self.timebase,'SET_LOW')
			self.curve = self.addCurve(self.plot,val,self.randomColor())
			self.curve.setData(self.xdata*1e-3,self.ydata) #mS to Seconds

	def CCCharge(self):
		val,ok = QtGui.QInputDialog.getText(self,"Name this dataset","",text = "CC")
		if ok :
			self.p.I.set_state(CCS=0)		# CCS disabled
			time.sleep(0.5)
			self.xdata, self.ydata = self.p.I.capture_action('CCS',self.samples,self.timebase,'SET_STATE',CCS=1)
			self.curve = self.addCurve(self.plot,val,self.randomColor())
			self.curve.setData(self.xdata*1e-3,self.ydata) #mS to Seconds

	def calcRC(self):
		msg = 'fit failed. please acquire some data first'
		if self.xdata is not None:
			start,end=self.region.getRegion()
			leftIndex = (np.abs(self.xdata*1e-3-start)).argmin()
			rightIndex = (np.abs(self.xdata*1e-3-end)).argmin()
			from expeyes import eyemath17
			#print (start,end,leftIndex,rightIndex)
			fa = eyemath17.fit_exp(self.xdata[leftIndex:rightIndex],self.ydata[leftIndex:rightIndex])
			if fa != None:
				pa = fa[1]
				rc = np.abs(1.0 / pa[1])
				msg = 'RC time constant = %5.2f mSec\nNew curve (%s_%5.2fmS) overlaid'%(rc,self.curve.name(),rc)
				fitcurve = self.addCurve(self.plot,'%s_%5.2fmS'%(self.curve.name(),rc),'#fff')
				fitcurve.setData(self.xdata[leftIndex:rightIndex]*1e-3,fa[0])
			else:
				msg = 'Failed to fit the curve with V=Vo*exp(-t/RC)'
		QtGui.QMessageBox.information(self, 'Fit Results', msg)








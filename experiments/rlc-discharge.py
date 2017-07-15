# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
try:
	from PyQt5 import QtGui,QtCore
except:
	from PyQt4 import QtGui,QtCore

from templates import ui_plotTemplate as plotTemplate
from utilities.expeyesWidgetsNew import expeyesWidgets

import sys,time,os
import numpy as np

class AppWindow(QtGui.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	subsection = 'apps'
	helpfile = 'RLCdischarge.html'
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		self.widgetLayout.setAlignment(QtCore.Qt.AlignTop)
		self.widgets.setMinimumWidth(250)
		
		self.TITLE('Controls')
		self.PUSHBUTTON('5V to 0V step' , self.FiveToZero)
		self.SPACER(10)
		self.PUSHBUTTON('Fit data' , self.calcRLC)
		self.tb = self.timebaseWidget(self.getSamples,self.setTimebase); self.widgetLayout.addWidget(self.tb)

		self.p.I.select_range('A1',8)
		self.samples = 200;self.timebase = 2
		self.xdata=None;self.ydata=None

		self.plot = self.newPlot([],detailedWidget=True,xMin=0,xMax = self.timebase*self.samples, bottomLabel = 'time',bottomUnits='S',leftLabel = 'Voltage',leftUnits='V',enableMenu=False,legend=True,autoRange='y')
		self.plot.setYRange(-5,5)

		self.region = self.addRegion(self.plot,0,9*4./10)
		self.tb.slider.setValue(3)

	def getSamples(self):
		return self.samples
		
	def setTimebase(self,t):
		self.plot.setLimits(xMin=0,xMax = t*self.samples*1e-6)
		self.timebase = t
		T = t*self.samples*1e-6
		self.plot.setXRange(0, T)
		self.region.setRegion([0,4*T/5])
		
	def FiveToZero(self):
		val,ok = QtGui.QInputDialog.getText(self,"Name this dataset","",text = "5->0")
		if ok :
			self.p.I.set_state(OD1=1)		# OD1 to HIGH
			time.sleep(0.5)
			self.xdata, self.ydata = self.p.I.capture_action('A1',self.samples,self.timebase,'SET_LOW')
			self.curve = self.addCurve(self.plot,val,self.randomColor())
			self.curve.setData(self.xdata*1e-3,self.ydata) #mS to Seconds

	def calcRLC(self):
		msg = 'fit failed. please acquire some data first'
		if self.xdata is not None:
			start,end=self.region.getRegion()
			leftIndex = (np.abs(self.xdata*1e-3-start)).argmin()
			rightIndex = (np.abs(self.xdata*1e-3-end)).argmin()
			from expeyes import eyemath17
			fa = eyemath17.fit_dsine(self.xdata[leftIndex:rightIndex],self.ydata[leftIndex:rightIndex],1)
			if fa != None:
				pa = fa[1]
				rc = 1.0 / pa[1]
				damping = pa[4] / (2*np.pi*pa[1]) # unitless damping factor
				msg = 'Resonant Frequency = %5.2f kHz\nDamping = %5.3f'%(pa[1], damping)
				fitcurve = self.addCurve(self.plot,'%s_%5.2fHz'%(self.curve.name(),pa[1]),'#fff')
				fitcurve.setData(self.xdata[leftIndex:rightIndex]*1e-3,fa[0])
			else:
				msg = 'Failed to fit the curve '
		QtGui.QMessageBox.information(self, 'Fit Results', msg)








# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from ..Qt import QtGui, QtCore
from ..templates import ui_plotTemplate as plotTemplate
from ..utilities.expeyesWidgetsNew import expeyesWidgets

import sys,time,os
import numpy as np
_translate = QtCore.QCoreApplication.translate

class AppWindow(QtGui.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	subsection = 'apps'
	helpfile = 'RLcircuit.html'
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		self.widgetLayout.setAlignment(QtCore.Qt.AlignTop)
		self.widgets.setMinimumWidth(250)
		
		self.TITLE(_translate("rl-circuit",'Controls'))
		self.PUSHBUTTON(_translate("rl-circuit",'0V to 5V step') , self.ZeroToFive)
		self.PUSHBUTTON(_translate("rl-circuit",'5V to 0V step') , self.FiveToZero)
		self.SPACER(10)
		self.TITLE(_translate("rl-circuit",'external resistance'))
		self.res = self.SPINBOX(decimals = True,suffix=u' \u03A9',range=[10,2000],value=1000)
		self.TITLE(_translate("rl-circuit",'Analyse data'))
		self.PUSHBUTTON(_translate("rl-circuit",'Calculate RL') , self.calcRL)
		self.tb = self.timebaseWidget(self.getSamples,self.setTimebase); self.widgetLayout.addWidget(self.tb)

		self.p.I.select_range('A1',8)
		self.p.I.select_range('A2',8)
		self.samples = 200;self.timebase = 2
		self.xdata=None;self.ydata=None

		self.plot = self.newPlot([],detailedWidget=True,xMin=0,xMax = self.timebase*self.samples, bottomLabel = _translate("rl-circuit",'time'),bottomUnits=_translate("rl-circuit",'S'),leftLabel = _translate("rl-circuit",'Voltage'),leftUnits='V',enableMenu=False,legend=True,autoRange='y')
		self.plot.setYRange(-5,5)

		self.region = self.addRegion(self.plot,0,9*4./10)
		self.tb.slider.setValue(1)

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

	def calcRL(self):
		msg = _translate("rl-circuit",'fit failed. please acquire some data first')
		if self.xdata is not None:
			start,end=self.region.getRegion()
			leftIndex = (np.abs(self.xdata*1e-3-start)).argmin()
			rightIndex = (np.abs(self.xdata*1e-3-end)).argmin()
			from expeyes import eyemath17
			self.p.I.set_state(OD1=1)			# Do some DC work to find the resistance of the Inductor
			time.sleep(.5)
			Rext = 	float(self.res.value())
			vtotal = 5.0				# Assume OD1 = 5 volts
			v = self.p.I.get_voltage('A2')
			if v > 4.8:					# Means user has connected OD1 to A2
				vtotal = v
			Vind = self.p.I.get_voltage('A1')     # voltage across the Inductor
			i = (vtotal - Vind)/Rext
			Rind = Vind/i
			fa = eyemath17.fit_exp(self.xdata[leftIndex:rightIndex],self.ydata[leftIndex:rightIndex])
			if fa != None:
				pa = fa[1]
				par1 = abs(1.0 / pa[1])
				msg = u_translate("rl-circuit",'L/R = %5.3f mSec\nRind = %5.0f \u03A9\nL = %5.1f mH')%(par1, Rind, (Rext+Rind)*par1)
				fitcurve = self.addCurve(self.plot,_translate("rl-circuit",'%s_%5.2fmS')%(self.curve.name(),par1),'#fff')
				fitcurve.setData(self.xdata[leftIndex:rightIndex]*1e-3,fa[0])
			else:
				msg = _translate("rl-circuit",'Failed to fit the curve with V=Vo*exp(-t/RC)')
		QtGui.QMessageBox.information(self, _translate("rl-circuit",'Fit Results'), msg)

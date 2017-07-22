# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from ..Qt import QtGui, QtCore
from ..templates import ui_plotTemplate as plotTemplate
from ..utilities.expeyesWidgetsNew import expeyesWidgets

import sys,time,os
import numpy as np

class AppWindow(QtGui.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	subsection = 'apps'
	helpfile = 'diode-iv.html'
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		self.widgetLayout.setAlignment(QtCore.Qt.AlignTop)
		self.widgets.setMinimumWidth(250)
		
		self.TITLE('Parameters')
		self.startVoltage=self.SPINBOX(decimals=True,prefix = 'Start Voltage: ',range=[0,4.9],value = 0)
		self.stopVoltage=self.SPINBOX(decimals=True,prefix = 'Stop Voltage: ',range=[0,4.9],value = 4)
		self.stepVoltage=self.SPINBOX(prefix = 'Steps: ',range=[5,1000],value = 100)

		self.SPACER(10)
		self.minimumTime=self.SPINBOX(prefix = 'acquisition time: ',suffix=' S',range=[0,2000],value = 5,tooltip="minimum acquisition time. 0 implies fastest possible")

		#Add a vertical spacer in the widgetLayout . about 0.5cm
		self.SPACER(20)
		self.TITLE('Initialize')
		self.PUSHBUTTON('Start Logging' , self.start)
		self.PUSHBUTTON('Stop Logging' , self.stop)
		self.SPACER(20)
		self.PUSHBUTTON('Fit Data' , self.fit_curve)
		self.activeCurve= None

		self.stepV = 0.1
		self.xdata=[];self.ydata = []
		
		self.p.I.select_range('A1',4)

		self.plot = self.newPlot([],detailedWidget=True,xMin=0,xMax = 4, bottomLabel = 'voltage',bottomUnits='V',leftLabel = 'current',leftUnits='A',enableMenu=False,legend=True,autoRange='y')
		self.plot.setYRange(0,5e-3)

		self.start_time = time.time()
		self.timer = self.newTimer()


	def update(self):
		setV = self.p.I.set_pv1(self.lastV)
		time.sleep(0.02)
		V = self.p.I.get_average_voltage('A1')
		I = (setV-V)/1e3
		self.xdata.append(V)
		self.ydata.append(I)
		if len(self.xdata)>3:
			self.activeCurve.setData(self.xdata,self.ydata)
		self.lastV+=self.stepV
		if self.lastV >= self.stopV:
			self.stop()

	def start(self):
		val,ok = QtGui.QInputDialog.getText(self,"Name this dataset","",text = "myDiode")
		if ok :
			self.activeCurve = self.addCurve(self.plot,val,self.randomColor())
			self.xdata=[];self.ydata = []
			start = self.startVoltage.value()
			self.stopV = self.stopVoltage.value()
			self.lastV = start
			self.stepV = (self.stopV-start)/self.stepVoltage.value()
			self.plot.setLimits(xMin = start,xMax = self.stopV+1);self.plot.setXRange(0,self.stopV+1)
			self.start_time = time.time()
			self.p.I.set_pv1(self.lastV); time.sleep(0.1)

			self.setInterval(self.timer,1e3*float(self.minimumTime.value())/self.stepVoltage.value(),self.update)

	def fit_curve(self):
		msg = 'fit failed. please acquire some data first'
		if self.xdata is not None and self.activeCurve is not None:
			from expeyes import eyemath17
			f = eyemath17.fit_exp(self.xdata, self.ydata)
			if f != None:
				k = 1.38e-23    # Boltzmann const
				q = 1.6e-19     # unit charge
				Io = f[1][0]
				a1 = f[1][1]
				T = 300.0		# Room temp in Kelvin
				n = q/(a1*k*T)

				msg = 'Fitted with Diode Equation :\nIo = %s\nIdeality factor = %5.2f'%(self.applySIPrefix(Io,'A',2),n)
				fitcurve = self.addCurve(self.plot,'%s\n%s\nIF=%5.1f'%(self.activeCurve.name(),self.applySIPrefix(Io,'A',2),n),'#fff')
				fitcurve.setData(self.xdata,f[0])
			else:
				msg = 'Failed to fit the curve '
		QtGui.QMessageBox.information(self, 'Fit Results', msg)

	def stop(self):
		self.timer.stop()
		self.timer.timeout.disconnect()
		pass

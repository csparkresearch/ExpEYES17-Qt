# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from ..Qt import QtGui, QtCore
from ..templates import ui_plotTemplate as plotTemplate
from ..utilities.expeyesWidgetsNew import expeyesWidgets

import sys,time,os
import numpy as np
import pyqtgraph as pg
_translate = QtCore.QCoreApplication.translate

class AppWindow(QtGui.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	subsection = 'apps'
	helpfile = 'iv-hysterisis.html'
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		self.widgetLayout.setAlignment(QtCore.Qt.AlignTop)
		self.widgets.setMinimumWidth(250)
		#Constants
		
		self.TITLE(_translate("diode-iv-hysterisis",'Parameters'))
		self.minVoltage=self.SPINBOX(decimals=True,prefix = _translate("diode-iv-hysterisis",'Minimum Voltage: '),range=[-5,0],value = -4)
		self.maxVoltage=self.SPINBOX(decimals=True,prefix = _translate("diode-iv-hysterisis",'Maximum Voltage: '),range=[0,5],value = 4)
		self.stepVoltage=self.SPINBOX(prefix = _translate("diode-iv-hysterisis",'Steps: '),range=[5,1000],value = 100)
		self.SPACER(10)
		self.startVoltage=self.SPINBOX(decimals=True,prefix = _translate("diode-iv-hysterisis",'Starting Voltage: '),range=[-5,5],value = 0)
		self.minimumTime=self.SPINBOX(prefix = _translate("diode-iv-hysterisis",'acquisition time: '),suffix=_translate("diode-iv-hysterisis",' S'),range=[0,2000],value = 5,tooltip="minimum acquisition time. 0 implies fastest possible")

		#Add a vertical spacer in the widgetLayout . about 0.5cm
		self.SPACER(20)
		self.TITLE(_translate("diode-iv-hysterisis",'Initialize'))
		self.PUSHBUTTON(_translate("diode-iv-hysterisis",'Start Acquisition') , self.start)
		self.PUSHBUTTON(_translate("diode-iv-hysterisis",'Stop Acquisition') , self.stop)
		self.activeCurve= None

		self.stepV = 0.1
		self.segment=''
		self.xdata=[];self.ydata = []
		
		self.p.I.select_range('A1',4)

		self.plot = self.newPlot([],detailedWidget=True,xMin=0,xMax = 4, bottomLabel = _translate("diode-iv-hysterisis",'voltage'),bottomUnits='V',leftLabel = _translate("diode-iv-hysterisis",'current'),leftUnits='A',enableMenu=False,legend=True,autoRange='y')
		self.plot.setYRange(-5e-3,5e-3)

		self.arrow = pg.ArrowItem(angle=-120,tipAngle = 80, headLen=5, tailLen=9, tailWidth=3, pen={'color': 'g', 'width': 1}) 
		self.plot.addItem(self.arrow)
		self.arrow.setPos(0,0)
		

		self.start_time = time.time()
		self.timer = self.newTimer()


	def update(self):
		setV = self.p.I.set_pv1(self.lastV)
		time.sleep(0.03)
		V = self.p.I.get_average_voltage('A1')
		I = (setV-V)/1e3
		self.xdata.append(V)
		self.ydata.append(I)
		if len(self.xdata)>3:
			self.arrow.setPos(V,I)
			self.activeCurve.setData(self.xdata,self.ydata)
		
		if self.segment=='up': #Hysterisis moving upwards to vMax
			self.lastV+=self.stepV
			if self.lastV >= self.maxV:
				self.segment='down'
		elif self.segment == 'down':
			self.lastV-=self.stepV
			if self.lastV <= self.minV:
				self.segment='up2'
		elif self.segment == 'up2':
			self.lastV+=self.stepV
			if self.lastV >= self.startV:
				self.segment=''			
				self.stop()

	def start(self):
		val,ok = QtGui.QInputDialog.getText(self,"Name this dataset","",text = "myDiode")
		if ok :
			self.activeCurve = self.addCurve(self.plot,val,self.randomColor())
			self.xdata=[];self.ydata = []
			self.minV = self.minVoltage.value()
			self.maxV = self.maxVoltage.value()
			self.startV = self.startVoltage.value()
			self.lastV = self.startV
			self.segment = 'up'
			
			self.stepV = 2*(self.maxV-self.minV)/self.stepVoltage.value()

			self.plot.setLimits(xMin = self.minV-0.5,xMax = self.maxV+0.5);self.plot.setXRange(self.minV-0.5,self.maxV+0.5)
			self.start_time = time.time()
			self.p.I.set_pv1(self.lastV); time.sleep(0.1)

			self.setInterval(self.timer,1e3*float(self.minimumTime.value())/self.stepVoltage.value(),self.update)

	def stop(self):
		self.timer.stop()
		self.timer.timeout.disconnect()
		pass

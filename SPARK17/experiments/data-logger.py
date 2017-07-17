# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from PyQt4 import QtGui,QtCore

from templates import ui_plotTemplate as plotTemplate
from utilities.expeyesWidgetsNew import expeyesWidgets

import sys,time,os
import numpy as np

class AppWindow(QtGui.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	subsection = 'apps'
	helpfile = 'pendulum-waveform.html'
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		self.widgetLayout.setAlignment(QtCore.Qt.AlignTop)
		self.widgets.setMinimumWidth(250)
		
		self.TITLE('Parameters: A3')
		self.totalTime=self.SPINBOX(prefix = 'Acquisition time: ',suffix=' S',range=[0,2000],value = 30,tooltip="Total time over which data should be recorded")
		self.minimumTime=self.SPINBOX(prefix = 'Time per sample: ',suffix=' mS',range=[0,2000],value = 2,tooltip="Minimum time per sample")

		self.SPACER(10)

		#Add a vertical spacer in the widgetLayout . about 0.5cm
		self.SPACER(20)
		self.TITLE('Initialize')
		self.PUSHBUTTON('Start Logging' , self.start)
		self.PUSHBUTTON('Stop Logging' , self.stop)
		self.valLabel = self.LABEL('Result:')
		self.valLabel.setStyleSheet('font-size:14pt')
		self.SPACER(20)
		self.PUSHBUTTON('Fit Data' , self.fit_curve)
		self.activeCurve= None

		self.xdata=[];self.ydata = []
		
		xmax = self.totalTime.value()
		self.endTime = 0
		self.plot = self.newPlot([],detailedWidget=True,xMin=0,xMax = xmax, bottomLabel = 'time',bottomUnits='S',leftLabel = 'voltage',leftUnits='V',enableMenu=False,legend=True,autoRange='y')
		self.plot.setYRange(-3,3)
		self.region = self.addRegion(self.plot,0,xmax*0.8)

		self.start_time = time.time()
		self.timer = self.newTimer()


	def update(self):
		v = self.p.I.get_average_voltage('A3')
		t = time.time()-self.start_time
		self.xdata.append(t)
		self.ydata.append(v)
		L = len(self.xdata)
		if L>3:
			self.activeCurve.setData(self.xdata,self.ydata)
			if L%100==0:
				self.valLabel.setText('Voltage:\t%s'%self.applySIPrefix(v,'V',2))

		if t>self.endTime:
			self.xmax=t+1
			self.plot.setLimits(xMax = self.xmax);self.plot.setXRange(0,self.xmax)
			self.stop()

	def start(self):
		val,ok = QtGui.QInputDialog.getText(self,"Name this dataset","",text = "A3#")
		if ok :
			self.activeCurve = self.addCurve(self.plot,val,self.randomColor())
			self.xdata=[];self.ydata = []
			self.xmax = self.totalTime.value()
			self.plot.setLimits(xMax = self.xmax);self.plot.setXRange(0,self.xmax)
			self.region.setRegion([0,self.xmax*0.8])
			self.start_time = time.time()
			self.endTime = self.start_time+self.xmax
			self.setInterval(self.timer,self.minimumTime.value(),self.update)


	def fit_curve(self):
		msg = 'fit failed. please acquire some data first'
		if self.xdata is not None:
			start,end=self.region.getRegion()
			xdata = np.array(self.xdata)
			leftIndex = (np.abs(xdata-start)).argmin()
			rightIndex = (np.abs(xdata-end)).argmin()
			from expeyes import eyemath17
			fa = eyemath17.fit_dsine(xdata[leftIndex:rightIndex],self.ydata[leftIndex:rightIndex],1)
			if fa != None:
				pa = fa[1]
				damping = pa[4] / (2*np.pi*pa[1]) # unitless damping factor
				msg = 'Resonant Frequency = %5.2f Hz\nDamping = %5.3f'%(pa[1], damping)
				fitcurve = self.addCurve(self.plot,'%s\n%s %5.3f'%(self.activeCurve.name(),self.applySIPrefix(pa[1],'Hz',1),damping),'#fff')
				fitcurve.setData(xdata[leftIndex:rightIndex],fa[0])
			else:
				msg = 'Failed to fit the curve '
		QtGui.QMessageBox.information(self, 'Fit Results', msg)

	def stop(self):
		self.timer.stop()
		self.timer.timeout.disconnect()
		pass

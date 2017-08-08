# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from ..Qt import QtGui, QtCore, QtWidgets
from ..templates import ui_plotTemplate as plotTemplate
from ..utilities.expeyesWidgetsNew import expeyesWidgets

import sys,time,os
import numpy as np
_translate = QtCore.QCoreApplication.translate

class AppWindow( QtWidgets.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	subsection = 'apps'
	helpfile = 'pendulum-waveform.html'
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		self.widgetLayout.setAlignment(QtCore.Qt.AlignTop)
		self.widgets.setMinimumWidth(250)
		
		self.TITLE(_translate("data-logger",'Parameters: A3'))
		self.totalTime=self.SPINBOX(prefix = _translate("data-logger",'Acquisition time: '),suffix=_translate("data-logger",' S'),range=[0,2000],value = 30,tooltip="Total time over which data should be recorded")
		self.minimumTime=self.SPINBOX(prefix = _translate("data-logger",'Time per sample: '),suffix=_translate("data-logger",' mS'),range=[0,2000],value = 2,tooltip="Minimum time per sample")

		self.SPACER(10)

		#Add a vertical spacer in the widgetLayout . about 0.5cm
		self.SPACER(20)
		self.TITLE(_translate("data-logger",'Initialize'))
		self.PUSHBUTTON(_translate("data-logger",'Start Logging') , self.start)
		self.PUSHBUTTON(_translate("data-logger",'Stop Logging') , self.stop)
		self.valLabel = self.LABEL(_translate("data-logger",'Result:'))
		self.valLabel.setStyleSheet('font-size:14pt')
		self.SPACER(20)
		self.PUSHBUTTON(_translate("data-logger",'Fit Data') , self.fit_curve)
		self.activeCurve= None

		self.xdata=[];self.ydata = []
		
		xmax = self.totalTime.value()
		self.endTime = 0
		self.plot = self.newPlot([],detailedWidget=True,xMin=0,xMax = xmax, bottomLabel = _translate("data-logger",'time'),bottomUnits=_translate("data-logger",'S'),leftLabel = _translate("data-logger",'voltage'),leftUnits='V',enableMenu=False,legend=True,autoRange='y')
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
				self.valLabel.setText(_translate("data-logger",'Voltage:\t%s')%self.applySIPrefix(v,'V',2))

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
		msg = _translate("data-logger",'fit failed. please acquire some data first')
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
				msg = _translate("data-logger",'Resonant Frequency = %5.2f Hz\nDamping = %5.3f')%(pa[1], damping)
				fitcurve = self.addCurve(self.plot,_translate("data-logger",'%s\n%s %5.3f')%(self.activeCurve.name(),self.applySIPrefix(pa[1],'Hz',1),damping),'#fff')
				fitcurve.setData(xdata[leftIndex:rightIndex],fa[0])
			else:
				msg = _translate("data-logger",'Failed to fit the curve ')
		QtGui.QMessageBox.information(self, _translate("data-logger",'Fit Results'), msg)

	def stop(self):
		self.timer.stop()
		self.timer.timeout.disconnect()
		pass

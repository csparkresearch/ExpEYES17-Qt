# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from PyQt4 import QtGui,QtCore

from templates import ui_plotTemplate as plotTemplate
from utilities.expeyesWidgetsNew import expeyesWidgets

import pyqtgraph as pg
import sys,time,functools

class AppWindow(QtGui.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		self.widgetLayout.setAlignment(QtCore.Qt.AlignTop)

		# ADD AN OSCILLOSCOPE PLOT TO THE plotLayout
		# This assumes self.plotLayout, and makes a dictionary self.curves with keys 'A1','A2','A3','MIC'
		#You should be able to access after executing this function. self.myCurves is a dictionary of curves with 4 Elements
		
		self.TITLE('4-Channel Oscilloscope')
		self.SCOPEPLOT(['A1','A2','A3','A1+A2'],rangeA1='4V',rangeA2='4V')   #You can also make up your own curve names. WORK IN PROGRESS [ e.g. A1+A2  should make a channel that automatically shows the sum]
		self.xaxis = self.plot.getAxis('bottom')

		self.TIMEBASE()
		self.TRIGGER()

		#Add a spacer
		self.SPACER(20)

		# ADD A SINE WIDGET SLIDER WITH NUMBERIC INPUT to the widgetLayout
		self.TITLE('Output Controls')
		self.SINE(value=2000)

		# Example 1 . 
		# autoCapture keeps calling 'CAPTURE' with no arguments. This will automatically plot the returned data with no user intervention
		
		#self.setInterval(50,self.autoCapture)
		
		# Example 2 . 
		# manualUpdate keeps calling 'CAPTURE' with self.processor as the argument. This will automatically forward the returned data to self.manualUpdateProcessor which can then call updatePlot if required
		self.paused = self.CHECKBOX('Pause')
		self.timer = self.newTimer()
		self.setTimeout(self.timer,100,self.manualUpdate)
		#self.setTimeout(1000,functools.partial(self.capture,'A1',200,3),self.update)


	def autoCapture(self):
		if self.p.busy:return
		self.CAPTURE()
		self.showStatus('capturing at :%s'%time.ctime())
	

	def manualUpdate(self):
		if self.p.busy or self.paused.isChecked():
			self.setTimeout(self.timer,100,self.manualUpdate)
			return

		self.CAPTURE(self.manualUpdateProcessor)
		self.showStatus('capturing at :%s'%time.ctime())

	def manualUpdateProcessor(self,*args,**kwargs):
		print ('######################################## Oscilloscope',self.allTimers)
		self.updatePlot(*args,**kwargs)
		print ('########################################')
		self.setTimeout(self.timer,100,self.manualUpdate)
		#print (args,kwargs)



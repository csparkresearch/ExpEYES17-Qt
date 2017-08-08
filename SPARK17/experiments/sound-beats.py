# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from ..Qt import QtGui, QtCore
from ..templates import ui_plot2Template as plotTemplate
from ..utilities.expeyesWidgetsNew import expeyesWidgets

import pyqtgraph as pg
from ..expeyes import eyemath17 as eyemath

import sys,time,functools,os
import numpy as np
_translate = QtCore.QCoreApplication.translate

class AppWindow(QtGui.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	subsection = 'apps'
	helpfile = 'sound-beats.html'
	counter=0
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		self.widgetLayout.setAlignment(QtCore.Qt.AlignTop)
		self.samples = 5000
		self.timebase = 2
		self.acquisition_channel = 'MIC'

		self.fftPlot = self.addPlot(yMin=-0,yMax=4, disableAutoRange = 'x',bottomLabel=_translate("sound-beats",'frequency'),bottomUnits='Hz',enableMenu=False,hideAxes='y')
		self.fftPlot.setXRange(2000,4000); self.fftPlot.setTitle(_TRANSLATE("sound-beats",'FFT'))
		self.pop = self.PUSHBUTTON(_translate("sound-beats",'Pop-up FFT'),self.popup)


		self.plot = self.newPlot([],xMin=0, bottomLabel = _translate("sound-beats",'time'),bottomUnits=_translate("sound-beats",'S'),leftLabel = _translate("sound-beats",'MIC(loudness)'),leftUnits='V',enableMenu=False,legend=True,autoRange='y')
		self.addCrosshair(self.plot,self.updateLabels,'y');self.plot.setTitle('_')
		self.MIC = self.addCurve(self.plot,_TRANSLATE("sound-beats",'MIC'),'#FFF')
		self.plot.setYRange(-3.2,3.2)
		self.popupFFT=None

		#self.fitLabel = pg.TextItem(anchor=(0,0));
		#self.phasorplot.addItem(self.fitLabel)
		#self.fitLabel.setPos(-4,4)
		self.plot2Layout.addWidget(self.fftPlot)
		self.pfft = self.addCurve(self.fftPlot,_TRANSLATE("sound-beats",'MIC_FFT'),'#FFF',False)
		
		#Add a vertical spacer in the widgetLayout . about 0.5cm
		self.SPACER(20)

		# ADD A SINE WIDGET SLIDER WITH NUMBERIC INPUT to the widgetLayout
		#self.TRIGGER()
		self.TITLE(_translate("sound-beats",'Timebase'))
		self.tb = self.timebaseWidget(self.getSamples,self.setTimebase); self.widgetLayout.addWidget(self.tb)
		#self.TITLE('Trigger')
		#self.activeTriggerWidget  =self.triggerWidget([self.acquisition_channel])
		self.widgetLayout.addWidget(self.activeTriggerWidget)
		self.trigLine = self.addInfiniteLine(self.plot,angle=0, movable=True,cursor = QtCore.Qt.SizeVerCursor,tooltip="Trigger level. Enable the trigger checkbox, and drag up/down to set the level",value = 0,ignoreBounds=False)
		self.trigLine.sigPositionChanged.connect(self.setTrigger)
		#self.activeTriggerWidget.chanBox.currentIndexChanged.connect(self.setTrigger)

		self.SPACER(10)

		self.TITLE(_translate("sound-beats",'Controls'))

		self.SW = self.SINE();self.SW.setValue(3300.)
		self.SQ = self.SQR1();self.SQ.setValue(3400.)
		
		self.tb.slider.setValue(1) 
		self.timer = self.newTimer()
		self.setTimeout(self.timer,100,self.update)
		self.p.sigPlot.connect(self.pt)
		#self.setTimeout(1000,functools.partial(self.capture,'A1',200,3),self.update)


		#self.triggerArrow = pg.ArrowItem(angle=-60,tipAngle = 90, headLen=10, tailLen=13, tailWidth=5, pen={'color': 'g', 'width': 1}) 
		#self.plot.addItem(self.triggerArrow)
		#self.triggerArrow.setPos(-1,0)

		#self.setTrigger()


	#def setTrigger(self):
	#	trigName = str(self.activeTriggerWidget.chanBox.currentText())
	#	self.trigger_level=self.trigLine.pos()
	#	trignum = self.activeTriggerWidget.chanBox.currentIndex()
	#	if trignum==-1 : #Index not found.
	#		return
	#	self.p.configure_trigger(0,self.acquisition_channel,self.trigger_level,resolution=10,prescaler=5)


	def updateLabels(self,evt):
		pos = evt[0]  ## using signal proxy turns original arguments into a tuple
		if self.plot.sceneBoundingRect().contains(pos) and len(self.x):
			mousePoint = self.plot.plotItem.vb.mapSceneToView(pos)
			index = mousePoint.x()
			self.plot.vLine.setPos(mousePoint.x())
			#self.plot.hLine.setPos(mousePoint.y())
			index = np.abs(self.x-mousePoint.x()).argmin()
			if index > 0 and index < len(self.x):
				self.plot.plotItem.titleLabel.setText("<span style='font-size: 12pt'>x=%s,   <span style='color: white'>y1=%0.1f</span>" % (self.applySIPrefix(self.x[index],_translate("sound-beats",'S')), self.y[index]))

	def getSamples(self):
		return self.samples
		
	def setTimebase(self,t):
		self.plot.setLimits(xMin=0,xMax = t*self.samples*1e-6)
		self.timebase = t
		T = t*self.samples*1e-6
		self.plot.setXRange(0, T)
		#self.region.setRegion([0,4*T/5])

	def update(self):
		self.channels_enabled=[1,0,0,0]
		
		#trig = self.activeTriggerWidget.enable.isChecked()
		self.p.capture_traces(1,self.samples,self.timebase,self.acquisition_channel,chans = self.channels_enabled)
		#The function doesn't end here. capture_traces will automatically call fetchData, which will then emit sigPlot with returned data, and self.pt is connected to sigPlot

		#self.p.capture1('A3',self.samples,self.timebase)

	def pt(self,vals):
		#print ('got plot',len(vals),vals.keys())
		plotnum=0
		self.x ,self.y = vals['A1']
		self.MIC.setData(self.x,self.y)
		try:
			self.fr,self.tr = eyemath.fft(self.y, self.timebase*0.001)
			if self.popupFFT:
				self.popupFFT.setData(self.fr,self.tr)
			self.pfft.setData(self.fr,self.tr)
		except Exception as e:
				print (_translate("sound-beats",'fft error'),e.message)

		self.counter+=1
		self.setTimeout(self.timer,100,self.update)

	def popup(self):
		plot,self.popupFFT = self.popupPlot(self.fr,self.tr)
		plot.getAxis('bottom').setLabel(_translate("sound-beats",'Frequency'))
		plot.getAxis('left').setLabel('')

# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from ..Qt import QtGui, QtCore
from ..templates import ui_plotTemplate as plotTemplate
from ..utilities.expeyesWidgetsNew import expeyesWidgets

import numpy as np

import sys,time,functools,os
_translate = QtCore.QCoreApplication.translate

class AppWindow(QtGui.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	subsection = 'apps'
	helpfile = 'clamping.html'
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		self.widgetLayout.setAlignment(QtCore.Qt.AlignTop)

		self.p.I.select_range('A1',8)
		self.p.I.select_range('A2',8)
		self.samples = 200
		self.timebase = 2
		
		self.plot = self.newPlot([],xMin=0,xMax = self.timebase*self.samples, bottomLabel = _translate("clamping",'time'),bottomUnits=_translate("clamping",'S'),leftLabel = _translate("clamping",'Voltage'),leftUnits='V',enableMenu=False,legend=True,enableYAxis=False)
		self.addCrosshair(self.plot,self.updateLabels,'y');self.plot.setTitle('_')
		self.A1 = self.addCurve(self.plot,'A1','#FFF')
		self.A2 = self.addCurve(self.plot,'A2','#F00')
		self.plot.setYRange(-7,7)

		#Add a vertical spacer in the widgetLayout . about 0.5cm
		self.SPACER(20)

		self.tb = self.timebaseWidget(self.getSamples,self.setTimebase); self.widgetLayout.addWidget(self.tb)
		self.tb.slider.setValue(2)
		# ADD A SINE WIDGET SLIDER WITH NUMBERIC INPUT to the widgetLayout
		self.TITLE(_translate("clamping",'Controls'))
		self.pvW=self.PV1()
		self.pvW.setValue(-3)


		self.SW = self.SINE();self.SW.setValue(1500.)
		

		self.timer = self.newTimer()
		self.setTimeout(self.timer,100,self.update)
		self.p.sigPlot.connect(self.pt)


	def updateLabels(self,evt):
		pos = evt[0]  ## using signal proxy turns original arguments into a tuple
		if self.plot.sceneBoundingRect().contains(pos):
			mousePoint = self.plot.plotItem.vb.mapSceneToView(pos)
			index = mousePoint.x()
			self.plot.vLine.setPos(mousePoint.x())
			#self.plot.hLine.setPos(mousePoint.y())
			index = np.abs(self.x-mousePoint.x()).argmin()
			if index > 0 and index < len(self.x):
				self.plot.plotItem.titleLabel.setText("<span style='font-size: 12pt'>x=%s,   <span style='color: white'>y1=%0.1f</span>,   <span style='color: red'>y2=%0.1f</span>" % (self.applySIPrefix(self.x[index],_translate("clamping",'S')), self.y1[index], self.y2[index]))

	def getSamples(self):
		return self.samples
		
	def setTimebase(self,t):
		self.plot.setLimits(xMin=0,xMax = t*self.samples*1e-6)
		self.timebase = t
		T = t*self.samples*1e-6
		self.plot.setXRange(0, T)
		#self.region.setRegion([0,4*T/5])

	def update(self):
		self.p.capture_traces(2,500,self.timebase,'A1',chans = [1,1,0,0])

	def pt(self,vals):
		#print ('got plot',len(vals),vals.keys())
		plotnum=0
		self.x,self.y1 = vals['A1']
		_,self.y2 = vals['A2']
		self.A1.setData(self.x,self.y1)
		self.A2.setData(self.x,self.y2)
		self.setTimeout(self.timer,100,self.update)

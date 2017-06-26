# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from PyQt4 import QtGui,QtCore

from templates import ui_plot2Template as plotTemplate
from utilities.expeyesWidgetsNew import expeyesWidgets
import pyqtgraph as pg

import sys,time,functools,os
import numpy as np

class AppWindow(QtGui.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	subsection = 'apps'
	helpfile = 'ac-circuits.html'
	counter=0
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		self.widgetLayout.setAlignment(QtCore.Qt.AlignTop)
		self.samples = 200
		self.timebase = 2

		self.p.I.select_range('A1',4)
		self.p.I.select_range('A2',4)
		self.fitresults=[None,None,None]
		self.phasorCheck = self.CHECKBOX('Follow crosshair')
		
		self.plot = self.newPlot([],xMin=0,xMax = self.timebase*self.samples, bottomLabel = 'time',bottomUnits='S',leftLabel = 'Voltage',leftUnits='V',enableMenu=False,legend=True,autoRange='y')
		self.addCrosshair(self.plot,self.updateLabels,'y');self.plot.setTitle('_')
		self.A1 = self.addCurve(self.plot,'A1','#FFF')
		self.A2 = self.addCurve(self.plot,'A2','#F00')
		self.A1A2 = self.addCurve(self.plot,'A1-A2','#0FF')
		self.plot.setYRange(-5,5)

		self.phasorplot = self.addPlot(xMin=-4,xMax=4,yMin=-4,yMax=4, disableAutoRange = 'xy',enableMenu=False,hideAxes='xy')
		self.fitLabel = pg.TextItem(anchor=(0,0));
		self.phasorplot.addItem(self.fitLabel)
		self.fitLabel.setPos(-4,4)
		self.plot2Layout.addWidget(self.phasorplot)
		self.pA1 = self.addCurve(self.phasorplot,'A1','#FFF',False)
		self.pA2 = self.addCurve(self.phasorplot,'A2','#F00',False)
		self.pA1A2 = self.addCurve(self.phasorplot,'A1-A2','#0FF',False)
		


		#Add a vertical spacer in the widgetLayout . about 0.5cm
		self.SPACER(20)

		# ADD A SINE WIDGET SLIDER WITH NUMBERIC INPUT to the widgetLayout
		#self.TRIGGER()
		self.TITLE('Controls')
		self.tb = self.timebaseWidget(self.getSamples,self.setTimebase); self.widgetLayout.addWidget(self.tb)
		self.SW = self.SINE();self.SW.setValue(200.)
		self.dataLabel = self.LABEL('results:')
		
		self.tb.slider.setValue(6) 
		self.timer = self.newTimer()
		self.setTimeout(self.timer,100,self.update)
		self.p.sigPlot.connect(self.pt)
		#self.setTimeout(1000,functools.partial(self.capture,'A1',200,3),self.update)

	def updateLabels(self,evt):
		pos = evt[0]  ## using signal proxy turns original arguments into a tuple
		if self.plot.sceneBoundingRect().contains(pos):
			mousePoint = self.plot.plotItem.vb.mapSceneToView(pos)
			index = mousePoint.x()
			self.plot.vLine.setPos(mousePoint.x())
			#self.plot.hLine.setPos(mousePoint.y())
			index = np.abs(self.x-mousePoint.x()).argmin()
			if index > 0 and index < len(self.x):
				self.plot.plotItem.titleLabel.setText("<span style='font-size: 12pt'>x=%s,   <span style='color: white'>y1=%0.1f</span>,   <span style='color: red'>y2=%0.1f</span>,   <span style='color: cyan'>y2=%0.1f</span>" % (self.applySIPrefix(self.x[index],'S'), self.y1[index], self.y2[index], self.y3[index]))
				self.updatePhasor()
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
		self.y3 = self.y1-self.y2
		self.A1.setData(self.x,self.y1)
		self.A2.setData(self.x,self.y2)
		self.A1A2.setData(self.x,self.y3)
		self.fitresults=[]
		msg='';num=0;colors=['white','red','cyan']
		for data in [self.y1,self.y2,self.y3]:
			try:
					fitres=self.sineFit(self.x,data)
					if fitres:
							amp=abs(fitres[0])
							freq=fitres[1]
							offset=fitres[2]
							ph=fitres[3]
							frequency = freq/1e6
							self.fitresults.append([amp,frequency,ph,offset])
							s = ('%5.2f V, %5.0f Hz %.2f')%(amp,frequency,ph)
							#self.myCurveWidgets[A].fit.setText(s)
			except Exception as e:
					self.fitresults.append(None)
					print ('fit error',e.message)
		self.counter+=1
		self.updatePhasor()
		self.setTimeout(self.timer,100,self.update)

	def updatePhasor(self):
		msg='';num=0;colors=['white','red','cyan']
		lx = self.plot.vLine.getPos()[0]
		#self.plot.hLine.setPos(mousePoint.y())
		#index = np.abs(self.x-lx).argmin()
		curves=[self.pA1,self.pA2,self.pA1A2]
		phaseInit = 0;frq=0;dPh=0
		msg2=u''
		if self.fitresults[0]:
			msg2 = u"<span style='color: magenta;font-size:12px;'>Frequency: %5.2f Hz</span><br>"%(self.fitresults[0][1])
		for data,b in zip(self.fitresults,['A1: Total Voltage:','A2: Voltage across R:','A1-A2: Voltage across LC:']):
			if data is not None:
				frq = data[1]
				if num==0:	phaseInit = data[2]
				elif num==2: dPh = phaseInit - data[2]
				ph = data[2]
				if self.phasorCheck.isChecked():
					ph = (data[2]+lx*360*frq)%360
				else:
					ph += (45-phaseInit)
				msg += "<span style='color: %s;font-size:11px;'>%5.2f V, %5.0f Hz, %.2f</span><br>"%(colors[num],data[0],frq,ph)
				msg2 += "<span style='color: %s;font-size:12px;'>%s %5.2f V</span><br>"%(colors[num],b,data[0])
				curves[num].setData([0,data[0]*np.cos(ph*np.pi/180)],[0,data[0]*np.sin(ph*np.pi/180)])
			num+=1
		self.fitLabel.setHtml(msg)
		msg2 += u"<span style='color: magenta;font-size:12px;'>Phase Shift: %5.2f deg</span><br>"%(dPh)
		self.dataLabel.setText(msg2)

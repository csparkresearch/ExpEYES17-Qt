# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from ..Qt import QtGui,QtCore,QtWidgets

from ..templates import ui_plotTemplate as plotTemplate
from ..utilities.expeyesWidgetsNew import expeyesWidgets
import numpy as np
import sys,time,functools,os

import pyqtgraph as pg
from collections import OrderedDict
_translate = QtCore.QCoreApplication.translate

class AppWindow(QtWidgets.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	subsection = 'apps'
	helpfile = 'oscilloscope.html'
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		self.widgetLayout.setAlignment(QtCore.Qt.AlignTop)

		from ..utilities.pg3d import pg3dWidgets
		self.PLOT3D = pg3dWidgets()
		self.num3d=0;self.MAX3D = 100;self.DATA3D=[];self.popup3d = None
		self.pop = self.PUSHBUTTON(_translate("scope3d",'Pop-up 3D'),self.popup3dPlot)


		self.timebase = 4
		self.samples = 200
		self.xmax = self.timebase*self.samples #assume 1mS

		stringaxis = pg.AxisItem(orientation='left')
		#ydict = {-4:'-4\n-2',-3:'-3',-2:'-2',-1:'-1',0:'0',1:'1',2:'2',3:'3',4:''}
		ydict = {-4:'',-3:'',-2:'',-1:'',0:'',1:'',2:'',3:'',4:''}
		stringaxis.setTicks([ydict.items()])
		stringaxis.setLabel(_translate("scope3d",'Voltage'),**{'color': '#FFF', 'font-size': '9pt'})
		stringaxis.setWidth(15)

		self.plot   = self.addPlot(xMin=0,xMax=self.xmax,yMin=-4,yMax=4, disableAutoRange = 'y',bottomLabel = _translate("scope3d",'time'),bottomUnits=_translate("scope3d",'S'),enableMenu=False,legend=True,leftAxis=stringaxis,enableYAxis=False,**kwargs)
		self.addCrosshair(self.plot,self.updateLabels,'y');self.plot.setTitle('_')
		self.plot.setMouseEnabled(False,True)
		self.plotLayout.addWidget(self.plot)
		self.myCurves=OrderedDict()
		self.myCurveWidgets = OrderedDict()
		self.cols={}
		num=0
		for a in ['A1','A2','A3','MIC']:
			if a not in self.currentRange:self.currentRange[a] = 4
			self.myCurves[a] = self.addCurve(self.plot,a,self.trace_colors[num])
			self.cols[a] = self.trace_colors[num]
			if(num==0 and kwargs.get('flexibleChan1',True)):
				self.myCurveWidgets[a] = self.flexibleChannelWidget(a,self.changeGain,self.p.I.allAnalogChannels,self.trace_colors[num])
			else :
				self.myCurveWidgets[a] = self.channelWidget(a,self.changeGain,self.trace_colors[num])
				if a!='A2': self.myCurveWidgets[a].enable.setChecked(False)  #Only enable A1,A2 on startup
			self.widgetLayout.addWidget(self.myCurveWidgets[a])
			num+=1
		self.makeLabels()

		self.changeGain('A1','4V')
		self.changeGain('A2','4V')

		#Add a vertical spacer in the widgetLayout . about 0.5cm
		self.SPACER(20)
		self.TIMEBASE()
		self.TRIGGER()

		# ADD A SINE WIDGET SLIDER WITH NUMBERIC INPUT to the widgetLayout
		self.TITLE(_translate("scope3d",'Output Controls'))
		self.PV1();self.PV2();
		self.SW = self.SINE();self.SW.setValue(1500.)
		self.SQR1();
		self.DOUTS()
		self.rbks = self.readbacksWidget(self.p)
		self.widgetLayout.addWidget(self.rbks)
		self.SPACER(20)
		
		self.sv = self.PUSHBUTTON(_translate("scope3d",'Save Data'),self.savePlots)
		self.paused = self.CHECKBOX(_translate("scope3d",'Pause'))
		self.lastUpdateTime = time.time()
		self.timer = self.newTimer()
		self.setTimeout(self.timer,100,self.update)
		self.p.sigPlot.connect(self.pt)
		self.p.sigGeneric.connect(self.resCapFreqCallback)

		self.timer2 = self.newTimer()
		self.setInterval(self.timer2,3000,self.checkAlive)

	def checkAlive(self):
		if time.time()-self.lastUpdateTime>3:
			print ('froze. restarted')
			self.setTimeout(self.timer,100,self.update)
			self.lastUpdateTime = time.time()
			

	def updateLabels(self,evt):
		pos = evt[0]  ## using signal proxy turns original arguments into a tuple
		if self.plot.sceneBoundingRect().contains(pos):
			mousePoint = self.plot.plotItem.vb.mapSceneToView(pos)
			index = mousePoint.x()
			self.plot.vLine.setPos(mousePoint.x())
			#self.plot.hLine.setPos(mousePoint.y())
			try:
				index = np.abs(self.x-mousePoint.x()).argmin()
			except:
				return
			msg = "<span >x=%s :[</span>"%self.applySIPrefix(self.x[index],_translate("scope3d",'S'))
			if index > 0 and index < len(self.x):
				for A in self.traceData:
					msg+="<span style='color: rgb%s'>%s:%0.1f </span>"%(self.cols[A],A,self.currentRange[A]*self.traceData[A][1][index]/4)
			msg+="]"
			self.plot.plotItem.titleLabel.setText(msg)

	def update(self):
		if self.p.busy or self.paused.isChecked():
			self.lastUpdateTime = time.time()
			self.setTimeout(self.timer,100,self.update)
			return
		self.traceOrder=[]  #This will store the order of the returned data
		a = self.myCurveWidgets['A1'].enable.isChecked() if 'A1' in self.myCurveWidgets else False
		b = self.myCurveWidgets['A2'].enable.isChecked() if 'A2' in self.myCurveWidgets else False
		c = self.myCurveWidgets['A3'].enable.isChecked() if 'A3' in self.myCurveWidgets else False
		d = self.myCurveWidgets['MIC'].enable.isChecked() if 'MIC' in self.myCurveWidgets else False
		self.chan1remap = str(self.myCurveWidgets['A1'].chan1Box.currentText())
		if c or d:
			self.traceOrder =[self.chan1remap,'A2','A3','MIC']
			self.active_channels=4
			if not d:
				self.active_channels=3
				self.traceOrder =[self.chan1remap,'A2','A3']
		elif b:
			self.traceOrder =[self.chan1remap,'A2']
			self.active_channels=2
		elif a:
			self.traceOrder =[self.chan1remap]
			self.active_channels=1
		else:
			self.active_channels=0

		self.channels_in_buffer=self.active_channels
		self.samples = self.max_samples_per_channel[self.active_channels]
		self.channels_enabled=[a,b,c,d]
		
		if self.active_channels:
			trig = self.activeTriggerWidget.enable.isChecked()
			timebase = self.activeTimebaseWidget.timebase
			chanRemap = str(self.myCurveWidgets['A1'].chan1Box.currentText())
			self.p.capture_traces(self.active_channels,self.samples,timebase,chanRemap,trigger = trig,chans = self.channels_enabled)
			#The function doesn't end here. capture_traces will automatically call fetchData, which will then emit sigPlot with returned data, and self.pt is connected to sigPlot
		

	def pt(self,vals):
		'''
		Data sent from worker thread.
		assume self.plot
		'''
		T = time.time()
		#self.showStatus(str(self.traceOrder))
		for a in self.myCurves:self.myCurves[a].clear()
		self.traceData={}
		keys = list(vals.keys())


		self.xmax = vals[keys[0]][0][:-1]
		self.plot.setLimits(xMin=0,xMax=vals[keys[0]][0][-1]);self.plot.setXRange(0,vals[keys[0]][0][-1])
		#print ('got plot',len(vals),vals.keys())
		plotnum=0
		traceGlobals={'np':np}


		
		for A in vals:
				R = self.currentRange[A]
				x = vals[A][0]
				self.x = x
				y = 4.*vals[A][1]/R
				self.y = y
				self.traceData[A] = [x,y]
				self.myCurves[A].setData(x,y)

				# make the fit
				if self.myCurveWidgets[A].fit.isChecked():
					try:
							fitres=self.sineFit(vals[A][0],vals[A][1])
							if fitres:
									amp=abs(fitres[0])
									freq=fitres[1]
									offset=fitres[2]
									ph=fitres[3]
									frequency = freq/1e6
									
									s = ('%5.2f V, %5.0f Hz')%(amp,frequency)
									self.myCurveWidgets[A].fit.setText(s)
					except Exception as e:
							#print (e.message)
							self.showStatus (e.message,True)
							pass
				else: self.myCurveWidgets[A].fit.setText(_translate("scope3d",'Fit'))
				#3d plot

				if ((self.popup3d is not None) and A=='A1'):
					self.num3d+=1
					if self.num3d>self.MAX3D:
						self.DATA3D[self.num3d%self.MAX3D]=self.y
					else:
						self.DATA3D.append(self.y)
					self.zgrid.translate(1./self.MAX3D,0,0,True)
					#self.zgrid.setSize( x=20, y=20, z=self.num3d)
					self.popup3d.setData(z=np.array(self.DATA3D))


		T = time.time()
		self.repositionLabels()
		#print ('plot called..............',time.time()-T)
		self.lastUpdateTime = time.time()
		self.setTimeout(self.timer,10,self.update)

	def resCapFreqCallback(self,name,res):
		#self.showStatus('%s : %s'%(name,str(res)))
		if 'capacitance' in name:
			if res<500e-6: ##500uF limit
				txt = _translate("scope3d",'CAP: ')+self.applySIPrefix(res,'F',2)
			else :
				txt = _translate("scope3d",'CAP: Inf')
			self.rbks.capLabel.setText(txt)
		elif 'resistance' in name:
			if res<10e6: ##10 meg
				txt = _translate("scope3d",'RES: ')+self.applySIPrefix(res,u"\u03A9",2)
			else :
				txt = _translate("scope3d",'RES: NaN')
			self.rbks.resLabel.setText(txt)
		elif 'freq' in name:
			if res<20e6: ##10 meg
				txt = _translate("scope3d",'FRQ: ')+self.applySIPrefix(res,'Hz',2)
			else :
				txt = _translate("scope3d",'FRQ: NaN')
			self.rbks.freqLabel.setText(txt)

	def popup3dPlot(self):
		plot,self.popup3d = self.PLOT3D.popup3dPlot()#x[:,0],y[,0:])
		self.popup3d.scale(20./self.MAX3D,20./len(self.x),10./4.)
		self.popup3d.translate(-10, -10, 0)
		self.zgrid = self.PLOT3D.gl.GLGridItem()
		self.zgrid.rotate(90, 0, 1, 0)
		plot.addItem(self.zgrid)




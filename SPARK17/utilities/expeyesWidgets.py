# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from .templates import ui_SliderAndSpinbox as SliderAndSpinbox
from .templates import ui_channelSelector as channelSelector

from PyQt4 import QtGui,QtCore
import pyqtgraph as pg
from collections import OrderedDict
import random

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class expeyesWidgets():
	"""
	This class contains methods that simplify setting up and running
	an experiment.
	
	feature list : 
	
	"""

	plotDict = {}
	timers = []
	trace_colors=[(0,255,0),(255,0,0),(255,255,100),(10,255,255)]+[(50+200*random.random(),50+200*random.random(),150+100*random.random()) for a in range(10)]
	trace_names = ['A1','A2','A3','MIC']
	curves={}
	gainAvailables = ['A1','A2']
	MAX_SAMPLES=2000
	max_samples_per_channel=[0,MAX_SAMPLES/4,MAX_SAMPLES/4,MAX_SAMPLES/4,MAX_SAMPLES/4]
	def __init__(self,*args,**kwargs):
		#sys.path.append('/usr/share/seelablet')
		pass
	

	####################################################################################
	#  EXTREMELY HIGH-LEVEL FUNCTIONS. THESE MAKE TOO MANY ASSUMPTIONS AND CAN ONLY BE #
	#  CALLED IF THIS CLASS IS INHERITED INTO AN ENVIRONMENT WITH THE FOLLOWING        #
	#   - plotLayout (If you wish to use 'newPlot'
	#   - plotLayout, p (interface) (If you wish to use 'W1','SQR1','PV1' etc ..)
	####################################################################################
	class constants:
		gainAvailables = ['A1','A2']

	def SINE(self):
		widget = self.addSine(self.p)
		self.widgetLayout.addWidget(widget)
		return widget
	def SQR1(self):
		widget = self.addSqr1(self.p)
		self.widgetLayout.addWidget(widget)
		return widget
	def PV1(self):
		widget = self.addPV1(self.p)
		self.widgetLayout.addWidget(widget)
		return widget
	def PV2(self):
		widget = self.addPV2(self.p)
		self.widgetLayout.addWidget(widget)
		return widget

	def SCOPEPLOT(self,curvenames):
		self.xmax = 1e-3 #assume 1mS
		self.plot   = self.addPlot(xMin=0,xMax=self.xmax,yMin=-4,yMax=4, disableAutoRange = 'y',bottomLabel = 'time',bottomUnits='S',enableMenu=False,legend=True)
		self.plot.setMouseEnabled(False,True)
		self.plotLayout.addWidget(self.plot)
		self.myCurves=OrderedDict();num=0
		self.myCurveWidgets = OrderedDict()

		for a in curvenames:
			self.myCurves[a] = self.addCurve(self.plot,a,self.trace_colors[num])
			self.myCurveWidgets[a] = self.channelWidget(self.p,a,self.trace_colors[num])
			self.widgetLayout.addWidget(self.myCurveWidgets[a])
			num+=1
		self.p.sigPlot.connect(self.updatePlot)


	def CAPTURE(self):
		if self.p.busy:
			print ('busy')
			return
		self.traceOrder=[]  #This will store the order of the returned data
		a = self.myCurveWidgets['A1'].enable.isChecked() if 'A1' in self.myCurveWidgets else False
		b = self.myCurveWidgets['A2'].enable.isChecked() if 'A2' in self.myCurveWidgets else False
		c = self.myCurveWidgets['A3'].enable.isChecked() if 'A3' in self.myCurveWidgets else False
		d = self.myCurveWidgets['MIC'].enable.isChecked() if 'MIC' in self.myCurveWidgets else False
		if c or d:
			self.traceOrder =['A1','A2','A3','MIC']
			self.active_channels=4
			if not d:
				self.active_channels=3
				self.traceOrder =['A1','A2','A3']
		elif b:
			self.traceOrder =['A1','A2']
			self.active_channels=2
		elif a:
			self.traceOrder =['A1']
			self.active_channels=1
		else:
			self.active_channels=0

		self.channels_in_buffer=self.active_channels
		self.samples = self.max_samples_per_channel[self.active_channels]
		self.channels_enabled=[a,b,c,d]
		
		if self.active_channels:
			#self.CH.capture_traces(self.active_channels,self.samples,self.timebase,self.chan1remap,trigger = self.trigBox.isChecked(),chans = self.channels_enabled)
			self.p.capture_traces(self.active_channels,self.samples,2,'A1',trigger = False,chans = self.channels_enabled)

	
	def updatePlot(self,vals):
		'''
		Data sent from worker thread.
		assume self.plot
		'''
		print (self.traceOrder)
		for a in self.myCurves:self.myCurves[a].clear()
		self.traceData={}
		keys = vals.keys()
		self.xmax = vals[keys[0]][0][:-1]
		self.plot.setLimits(xMin=0,xMax=vals[keys[0]][0][-1]);self.plot.setXRange(0,vals[keys[0]][0][-1])
		#print ('got plot',len(vals),vals.keys())
		plotnum=0
		for A in vals:
				#R = self.currentRange[A]
				x = vals[A][0]
				y = vals[A][1] # 4.*vals[A][1]/R
				self.traceData[A] = [x,y]
				self.myCurves[A].setData(x,y)

	class channelWidget(QtGui.QWidget,channelSelector.Ui_Form,constants):
		'''
		assumes self.p
		'''
		def __init__(self,handler,name,col=None):
			super(expeyesWidgets.channelWidget, self).__init__()
			self.setupUi(self)
			self.p = handler
			self.name = name
			self.enable.setText(self.name)
			if self.name not in self.gainAvailables:
				self.gain.setEnabled(False)
			else:
				QtCore.QObject.connect(self.gain, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.gainChanged)
			if col : self.enable.setStyleSheet("color:rgb%s"%str(col))

		def gainChanged(self,val):
			val = float(val[:-1]) #remove 'V'
			self.p.select_range(self.name,val)


	def SPACER(self,size):
		self.widgetLayout.addItem(QtGui.QSpacerItem(size, size, QtGui.QSizePolicy.Minimum))


	def setTimeout(self,delay,fn):
		'''
		Execute a function after a certain time interval
		'''
		timer = QtCore.QTimer()
		timer.singleShot(delay,fn)
		self.timers.append(timer)
		return timer

	def setInterval(self,delay,fn):
		'''
		Execute a function every x milliseconds
		'''
		timer = QtCore.QTimer()
		timer.timeout.connect(fn)
		timer.start(delay)
		self.timers.append(timer)
		return timer


	def windUp(self):
		for a in reversed(self.timers):
			a.stop()
			self.timers.remove(a)
			print ('deleted',a)
		time.sleep(0.2)
		for a in reversed(self.timers):
			a.stop()
			self.timers.remove(a)
			print ('deleted',a)
		self.p.sigPlot.disconnect(self.updatePlot)
	####################################################################################
		
	def addPlot(self,**kwargs):
		if 'leftAxis' in kwargs: kwargs['axisItems'] = {'left':kwargs.pop('leftAxis')}
		plot=pg.PlotWidget(enableMenu = False)
		plot.setMouseEnabled(False,True)
		if 'x' in kwargs.get('disableAutoRange',''):plot.disableAutoRange(axis = plot.plotItem.vb.XAxis)
		if 'y' in kwargs.get('disableAutoRange',''):
			plot.disableAutoRange(axis = plot.plotItem.vb.YAxis)
			print ('YAxis disabled')
		if kwargs.get('legend',False):plot.addLegend(offset=(-10,30))

		plot.getAxis('left').setGrid(170);
		plot.getAxis('bottom').setGrid(170); plot.getAxis('bottom').setLabel('time', units='S')
		limitargs = {a:kwargs.get(a) for a in ['xMin','xMax','yMin','yMax'] if a in kwargs}
		plot.setLimits(**limitargs);
		plot.setXRange(kwargs.get('xMin',0),kwargs.get('xMax',10));
		plot.setYRange(kwargs.get('yMin',-5),kwargs.get('yMax',-5));
		self.plotDict[plot] = []
		self.curves[plot] = []
		return plot

	def addCurve(self,plot,name,col):
		C=pg.PlotCurveItem(name = name,pen = col)
		self.plot.addItem(C)
		self.curves[plot].append(C)
		return C
		
		
	def addInfiniteLine(self,plot,**kwargs):
		line = pg.InfiniteLine(angle=kwargs.get('angle',0), movable=kwargs.get('movable',True))
		if 'cursor' in kwargs:line.setCursor(QtGui.QCursor(kwargs.get('cursor'))); 
		if 'tooltip' in kwargs:line.setToolTip(kwargs.get('tooltip'))

		if 'value' in kwargs:line.setPos(kwargs.get('value'))
		plot.addItem(line, ignoreBounds=kwargs.get('ignoreBounds'))
		return line


	class utils:
		def __init__(self):
			pass

		def applySIPrefix(self,value, unit='',precision=2 ):
				neg = False
				if value < 0.:
					value *= -1; neg = True
				elif value == 0.:  return '0 '  # Mantissa & exponent both 0
				exponent = int(np.log10(value))
				if exponent > 0:
					exponent = (exponent // 3) * 3
				else:
					exponent = (-1*exponent + 3) // 3 * (-3)

				value *= (10 ** (-exponent) )
				if value >= 1000.:
					value /= 1000.0
					exponent += 3
				if neg:
					value *= -1
				exponent = int(exponent)
				PREFIXES = "yzafpnum kMGTPEZY"
				prefix_levels = (len(PREFIXES) - 1) // 2
				si_level = exponent // 3
				if abs(si_level) > prefix_levels:
					raise ValueError("Exponent out range of available prefixes.")
				return '%.*f %s%s' % (precision, value,PREFIXES[si_level + prefix_levels],unit)


	def addPV1(self,handler):
		return self.sliderWidget(min = -5,max = 5, label = 'PV1' ,units = 'V', callback = handler.set_pv1) 

	def addPV2(self,handler):
		return self.sliderWidget(min = -3.3,max = 3.3, label = 'PV2' , units = 'V',callback = handler.set_pv2) 

	def addSQR1(self,handler):
		return self.sliderWidget(min = 5,max = 50000, label = 'SQR1' ,units = 'Hz', callback = handler.set_sqr1) 

	def addSine(self,handler):
		W = self.sliderWidget(min = 5,max = 5000, label = 'W1' ,units = 'Hz', callback = handler.set_sine)
		return W


	class sliderWidget(QtGui.QWidget,SliderAndSpinbox.Ui_Form,utils):
		'''
		slider : 10x the range of dial. End values are divided by ten before passing to callback. This is because QSlider does not have a Double option
		spinbox : numeric entry widget . double precision
		
		keyword arguments : min , max , callback, label
		'''
		def __init__(self,**kwargs):
			super(expeyesWidgets.sliderWidget, self).__init__()
			self.setupUi(self)
			self.callback = kwargs.get('callback',None)
			self.label.setText(kwargs.get('label','_'))
			self.min = kwargs.get('min',0)
			self.max = kwargs.get('max',100)
			self.spinbox.setSuffix(kwargs.get('units',''))
			self.spinbox.setMinimum(self.min);self.spinbox.setMaximum(self.max);
			self.slider.setMinimum(self.min*10);self.slider.setMaximum(self.max*10);

			self.slider.valueChanged.connect(self.sliderChanged)
			self.spinbox.valueChanged.connect(self.spinboxChanged)

		def sliderChanged(self,val):
			self.spinbox.setValue(val/10.)
			if self.slider.hasFocus():
				self.callback(val/10.)

		def spinboxChanged(self,val):
			self.slider.setValue(val*10.)
			if self.spinbox.hasFocus():
				self.callback(val)





	def connectSlot(self,signal, newhandler=None, oldhandler=None):
		while True:
			try:
				if oldhandler is not None:
					signal.disconnect(oldhandler)
				else:
					signal.disconnect()
			except TypeError:
				break
		if newhandler is not None:
			signal.connect(newhandler)
		



# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from .templates import ui_SliderAndSpinbox as SliderAndSpinbox
from .templates import ui_channelSelector as channelSelector
from .templates import ui_flexibleChannelSelector as flexibleChannelSelector
from .templates import ui_triggerWidget as triggerWidgetUi
from .templates import ui_timebaseWidget as timebaseWidgetUi

from PyQt4 import QtGui,QtCore
import pyqtgraph as pg
import numpy as np
from collections import OrderedDict
import random,functools,os


try:
	import scipy.optimize as optimize
except ImportError:
	optimize = None
else:
	optimize = optimize

try:
	import scipy.fftpack as fftpack
except ImportError:
	fftpack = None
else:
	fftpack = fftpack



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
	widgetArray = []
	trace_colors=[(0,255,0),(255,0,0),(255,255,100),(10,255,255)]+[(50+200*random.random(),50+200*random.random(),150+100*random.random()) for a in range(10)]
	trace_names = ['A1','A2','A3','MIC']
	curves={}
	gainAvailables = ['A1','A2']
	MAX_SAMPLES=2000
	max_samples_per_channel=[0,MAX_SAMPLES/4,MAX_SAMPLES/4,MAX_SAMPLES/4,MAX_SAMPLES/4]
	samples = MAX_SAMPLES/4

	Ranges12 = ['16 V', '8 V','4 V', '2.5 V','1.5 V', '1 V', '.5 V', '.25 V']	# Voltage ranges for A1 and A2
	rangevals12 = [16.,8.,4.,2.5,1.5,1.,0.5,0.25]
	Ranges34 = ['4 V', '2 V', '1 V', '.5V']					# Voltage ranges for A3 and MIC
	rangevals34 = [4,2,1,0.5]

	currentRange={'A1':4,'A2':4,'A3':4,'MIC':4}
	trig=None
	activeTriggerWidget = None
	activeTimebaseWidget = None
	def __init__(self,*args,**kwargs):
		#sys.path.append('/usr/share/seelablet')
		pass

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

	

	####################################################################################
	#  EXTREMELY HIGH-LEVEL FUNCTIONS. THESE MAKE TOO MANY ASSUMPTIONS AND CAN ONLY BE #
	#  CALLED IF THIS CLASS IS INHERITED INTO AN ENVIRONMENT WITH THE FOLLOWING        #
	#   - plotLayout (If you wish to use 'newPlot'
	#   - plotLayout, p (interface) (If you wish to use 'W1','SQR1','PV1' etc ..)
	####################################################################################
	class constants:
		gainAvailables = ['A1','A2']

	def SINE(self,**kwargs):
		widget = self.addSine(self.p,**kwargs)
		self.widgetLayout.addWidget(widget)
		return widget
	def SQR1(self,**kwargs):
		widget = self.addSQR1(self.p,**kwargs)
		self.widgetLayout.addWidget(widget)
		return widget
	def PV1(self,**kwargs):
		widget = self.addPV1(self.p,**kwargs)
		self.widgetLayout.addWidget(widget)
		return widget
	def PV2(self,**kwargs):
		widget = self.addPV2(self.p,**kwargs)
		self.widgetLayout.addWidget(widget)
		return widget


	def SCOPEPLOT(self,curvenames,**kwargs):
		self.xmax = 1e-3 #assume 1mS

		stringaxis = pg.AxisItem(orientation='left')
		#ydict = {-4:'-4\n-2',-3:'-3',-2:'-2',-1:'-1',0:'0',1:'1',2:'2',3:'3',4:''}
		ydict = {-4:'',-3:'',-2:'',-1:'',0:'',1:'',2:'',3:'',4:''}
		stringaxis.setTicks([ydict.items()])
		stringaxis.setLabel('Voltage',**{'color': '#FFF', 'font-size': '9pt'})
		stringaxis.setWidth(15)

		self.plot   = self.addPlot(xMin=0,xMax=self.xmax,yMin=-4,yMax=4, disableAutoRange = 'y',bottomLabel = 'time',bottomUnits='S',enableMenu=False,legend=True,leftAxis=stringaxis,**kwargs)
		self.plot.setMouseEnabled(False,True)
		self.plotLayout.addWidget(self.plot)
		self.myCurves=OrderedDict()
		self.myCurveWidgets = OrderedDict()
		num=0
		for a in curvenames:
			self.myCurves[a] = self.addCurve(self.plot,a,self.trace_colors[num])
			if(num==0 and kwargs.get('flexibleChan1',True)):
				self.myCurveWidgets[a] = self.flexibleChannelWidget(a,self.changeGain,self.p.I.allAnalogChannels,self.trace_colors[num])
			else :self.myCurveWidgets[a] = self.channelWidget(a,self.changeGain,self.trace_colors[num])
			self.widgetLayout.addWidget(self.myCurveWidgets[a])
			num+=1
		self.makeLabels()
		if 'rangeA1' in kwargs:self.changeGain('A1',kwargs.pop('rangeA1'))
		if 'rangeA2' in kwargs:self.changeGain('A2',kwargs.pop('rangeA2'))
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
			#self.CH.capture_traces(self.active_channels,self.samples,self.timebase,self.chan1remap,trigger = self.trigBox.isChecked(),chans = self.channels_enabled)
			trig = False
			timebase = 2
			chanRemap = 'A1'
			if self.activeTriggerWidget:
				trig = self.activeTriggerWidget.enable.isChecked()
			if self.activeTimebaseWidget:
				timebase = self.activeTimebaseWidget.timebase
			chanRemap = str(self.myCurveWidgets['A1'].chan1Box.currentText())
			self.p.capture_traces(self.active_channels,self.samples,timebase,chanRemap,trigger = trig,chans = self.channels_enabled)

	
	def updatePlot(self,vals):
		'''
		Data sent from worker thread.
		assume self.plot
		'''
		#self.showStatus(str(self.traceOrder))
		for a in self.myCurves:self.myCurves[a].clear()
		self.traceData={}
		keys = vals.keys()
		self.xmax = vals[keys[0]][0][:-1]
		self.plot.setLimits(xMin=0,xMax=vals[keys[0]][0][-1]);self.plot.setXRange(0,vals[keys[0]][0][-1])
		#print ('got plot',len(vals),vals.keys())
		plotnum=0
		for A in vals:
				R = self.currentRange[A]
				x = vals[A][0]
				y = 4.*vals[A][1]/R
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
							print (e.message)
							self.showStatus (e.message,True)
							pass
				else: self.myCurveWidgets[A].fit.setText('Fit')

		self.repositionLabels()

	def makeLabels(self):
		self.labelTexts={}
		xshift=self.xaxis.range[0]
		positions = np.linspace(-4,4,9)
		for a in self.myCurveWidgets:
			self.labelTexts[a]=[]
			vpd=self.currentRange[a]/4
			for ypos in positions:
				txt ='''<span style="color: rgb%s; font-size: 8pt;">%.2f </span>'''%(self.myCurveWidgets[a].col,ypos*vpd)
				lbl = pg.TextItem(html=txt, anchor=(-.5,0),angle=45);lbl.setPos(xshift, ypos)
				self.plot.addItem(lbl)
				self.labelTexts[a].append(lbl)
			xshift+=self.xaxis.range[1]*.03

	def renameLabels(self):
		positions = np.linspace(-4,4,9)
		for a in self.myCurveWidgets:
			vpd=self.currentRange[a]/4
			num=0;
			for ypos in positions:
				txt ='''<span style="color: rgb%s; font-size: 8pt;">%.2f </span>'''%(self.myCurveWidgets[a].col,ypos*vpd)
				self.labelTexts[a][num].setHtml(txt)
				num+=1


	def repositionLabels(self):
		xshift=self.xaxis.range[0]
		positions = np.linspace(-4,4,9)
		for a in self.myCurveWidgets:
				vpd=self.currentRange[a]/4
				num=0
				state = self.myCurveWidgets[a].enable.isChecked()
				for ypos in positions:
					if state:self.labelTexts[a][num].setVisible(True)
					else:self.labelTexts[a][num].setVisible(False)
					self.labelTexts[a][num].setPos(xshift, ypos)
					num+=1
				if state:xshift+=self.xaxis.range[1]*.03


	def changeGain(self,chan,val):
		val = float(val[:-1]) #remove 'V'
		chan  = str(chan)
		print (chan,val)
		if chan in ['A1','A2']:
			#v = self.rangevals12[val]
			self.currentRange[chan] = val
			self.p.select_range(chan,val)
		else:
			self.currentRange[chan] = val
		self.renameLabels()

	##########################controls##########################

	class channelWidget(QtGui.QWidget,channelSelector.Ui_Form,constants):
		def __init__(self,name,callback,col=None):
			super(expeyesWidgets.channelWidget, self).__init__()
			self.setupUi(self)
			self.col = col
			self.name = name
			self.callback = callback
			self.enable.setText(self.name)
			QtCore.QObject.connect(self.gain, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), functools.partial(self.callback,self.name))
			if col : self.enable.setStyleSheet("color:rgb%s"%str(col))


	class flexibleChannelWidget(QtGui.QWidget,flexibleChannelSelector.Ui_Form,constants):
		def __init__(self,name,callback,chans,col=None):
			super(expeyesWidgets.flexibleChannelWidget, self).__init__()
			self.setupUi(self)
			self.col = col
			self.chan1Box.addItems(chans)
			self.name = name
			self.callback = callback
			QtCore.QObject.connect(self.gain, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), self.modifiedCallback)
			if col : self.chan1Box.setStyleSheet("color:rgb%s"%str(col))

		def modifiedCallback(self,val):
			self.callback(self.chan1Box.currentText(),val)



	def SPACER(self,size):
		self.widgetLayout.addItem(QtGui.QSpacerItem(size, size, QtGui.QSizePolicy.Minimum))

	def TITLE(self,text):
		self.SPACER(5)
		line = QtGui.QFrame()
		line.setFrameShape(QtGui.QFrame.HLine);	line.setMinimumSize(QtCore.QSize(0, 8));line.setFrameShadow(QtGui.QFrame.Sunken)
		label = QtGui.QLabel(text)
		label.setStyleSheet("color:rgb(100,255,255)")
		self.widgetLayout.addWidget(label)
		self.widgetLayout.addWidget(line)


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
		self.trig=None
		self.activeTriggerWidget=None
		self.activeTimebaseWidget = None
		self.p.sigPlot.disconnect(self.updatePlot)
	####################################################################################
		
	def addPlot(self,**kwargs):
		if 'leftAxis' in kwargs: kwargs['axisItems'] = {'left':kwargs.pop('leftAxis')}
		plot=pg.PlotWidget(**kwargs)
		plot.setMouseEnabled(False,True)
		if 'x' in kwargs.get('disableAutoRange',''):
			plot.disableAutoRange(axis = plot.plotItem.vb.XAxis)
		if 'y' in kwargs.get('disableAutoRange',''):
			plot.disableAutoRange(axis = plot.plotItem.vb.YAxis)
		if kwargs.get('legend',False):plot.addLegend(offset=(-10,30))
		self.xaxis = plot.getAxis('bottom')

		plot.getAxis('left').setGrid(170);
		self.xaxis.setGrid(170); self.xaxis.setLabel('time', units='S')
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
		
		
	###############################  TRIGGERING THE OSCILLOSCOPE ######################
	def TRIGGER(self):
		self.TITLE('Trigger')
		self.activeTriggerWidget  =self.triggerWidget(self.trace_names)
		self.widgetLayout.addWidget(self.activeTriggerWidget)
		self.trigLine = self.addInfiniteLine(self.plot,angle=0, movable=True,cursor = QtCore.Qt.SizeVerCursor,tooltip="Trigger level. Enable the trigger checkbox, and drag up/down to set the level",value = 0,ignoreBounds=False)
		self.trigLine.sigPositionChanged.connect(self.setTrigger)
		self.activeTriggerWidget.pushButton.clicked.connect(self.locateTrigger)

		self.activeTriggerWidget.chanBox.currentIndexChanged.connect(self.setTrigger)

		self.triggerArrow = pg.ArrowItem(angle=-60,tipAngle = 90, headLen=10, tailLen=13, tailWidth=5, pen={'color': 'g', 'width': 1}) 
		self.plot.addItem(self.triggerArrow)
		self.triggerArrow.setPos(-1,0)

		self.setTrigger()

	class triggerWidget(QtGui.QWidget,triggerWidgetUi.Ui_Form):
		'''
		slider : 10x the range of dial. End values are divided by ten before passing to callback. This is because QSlider does not have a Double option
		spinbox : numeric entry widget . double precision
		
		keyword arguments : min , max , callback, label
		'''
		def __init__(self,chans):
			super(expeyesWidgets.triggerWidget, self).__init__()
			self.setupUi(self)
			self.chanBox.addItems(chans)

	def setTrigger(self):
		trigName = str(self.activeTriggerWidget.chanBox.currentText())
		self.trigger_level=self.currentRange[trigName]*self.trigLine.pos()[1]/4.
		trignum = self.activeTriggerWidget.chanBox.currentIndex()
		if trignum==-1 : #Index not found.
			return
		self.p.configure_trigger(trignum,trigName,self.trigger_level,resolution=10,prescaler=5)


	def addInfiniteLine(self,plot,**kwargs):
		line = pg.InfiniteLine(angle=kwargs.get('angle',0), movable=kwargs.get('movable',True))
		if 'cursor' in kwargs:line.setCursor(QtGui.QCursor(kwargs.get('cursor'))); 
		if 'tooltip' in kwargs:line.setToolTip(kwargs.get('tooltip'))

		if 'value' in kwargs:line.setPos(kwargs.get('value'))
		plot.addItem(line, ignoreBounds=kwargs.get('ignoreBounds'))
		return line

	def locateTrigger(self):
		self.trigAnimationPos = 0
		try: self.trigTimer.stop()
		except:pass
		self.trigTimer = self.setInterval(10,self.animateTrigger)

	def animateTrigger(self):
		_,y=self.trigLine.getPos()
		self.trigAnimationPos+=1e-6
		self.triggerArrow.setPos(self.trigAnimationPos,y)
		if self.trigAnimationPos>=100e-6:
			self.triggerArrow.setPos(-1,0)
			self.trigTimer.stop()
		
		
	############################### ############################### 


	###############################  TIMEBASE CONTROL FOR THE OSCILLOSCOPE ######################

	def TIMEBASE(self):
		self.TITLE('Time Base')
		self.activeTimebaseWidget  =self.timebaseWidget(self.getSamples)
		self.widgetLayout.addWidget(self.activeTimebaseWidget)

	def getSamples(self):
		return self.samples

	class timebaseWidget(QtGui.QWidget,timebaseWidgetUi.Ui_Form):
		def __init__(self,getSamples):
			super(expeyesWidgets.timebaseWidget, self).__init__()
			self.setupUi(self)
			self.getSamples = getSamples
			self.timebase = 2

		def valueChanged(self,val):
			vals = [2,4,6,8,10,20,50,100,200,500]
			self.timebase = vals[val]
			T = self.getSamples()*self.timebase
			self.value.setText('%s'%pg.siFormat(T*1e-6, precision=3, suffix='S', space=True))


	############################### ############################### 

	###############################  PUSHBUTTON WIDGET ######################

	def PUSHBUTTON(self,name, callback,**kwargs):
		widget  =self.pushButtonWidget(name, callback,**kwargs)
		self.widgetArray.append(widget)
		self.widgetLayout.addWidget(widget)

	class pushButtonWidget(QtGui.QPushButton):
		def __init__(self,name,callback,**kwargs):
			super(expeyesWidgets.pushButtonWidget, self).__init__()
			self.setText(name)
			self.callback = callback
			self.clicked.connect(self.callback)

	###############################  IMAGE WIDGET ######################

	def IMAGE(self,path):
		if not os.path.exists(path): 
			print ('Path not found',path)
			return
		try:
			self.TITLE(path)
			label = QtGui.QLabel() 
			self.widgetLayout.addWidget(label)
			label.setScaledContents(True)
			pixmap = QtGui.QPixmap(path)
			#print (label.size())
			#scaledPixmap = pixmap.scaled(label.size(), QtCore.Qt.KeepAspectRatio)
			label.setPixmap(pixmap.scaledToHeight(50))
			#x = QtGui.QIcon(path)
			#a = QtGui.QListWidgetItem(x,fname)
			#self.listWidget.addItem(a)
		except Exception as e:
			print (e)

	def addPV1(self,handler,**kwargs):
		return self.sliderWidget(min = -5,max = 5, label = 'PV1' ,units = 'V', callback = handler.set_pv1,**kwargs) 

	def addPV2(self,handler,**kwargs):
		return self.sliderWidget(min = -3.3,max = 3.3, label = 'PV2' , units = 'V',callback = handler.set_pv2,**kwargs) 

	def addSQR1(self,handler,**kwargs):
		return self.sliderWidget(min = 5,max = 50000, label = 'SQR1' ,units = 'Hz', callback = handler.set_sqr1,**kwargs) 

	def addSine(self,handler,**kwargs):
		W = self.sliderWidget(min = 5,max = 5000, label = 'W1' ,units = 'Hz', callback = handler.set_sine,**kwargs)
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

			if 'value' in kwargs:
				v = kwargs.get('value')
				v = min( max(self.min,v) ,self.max )
				self.spinbox.setValue(v)
				self.slider.setValue(v*10)
				self.callback(v)


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
		
	def save(self):
		from . import plotSaveWindow
		info = plotSaveWindow.AppWindow(self,self.curves[self.plot],self.plot)
		info.show()

	def showStatus(self,txt,err=False):
		self.p.sigStat.emit(txt,err)

	#-------------------------- Sine Fit ------------------------------------------------
	def sineFunc(self,x, a1, a2, a3,a4):
	    return a4 + a1*np.sin(abs(a2*(2*np.pi))*x + a3)

	def sineFit(self,xReal,yReal,**kwargs):
		if not optimize:return None
		N=len(xReal)
		OFFSET = (yReal.max()+yReal.min())/2.
		yhat = fftpack.rfft(yReal-OFFSET)
		idx = (yhat**2).argmax()
		freqs = fftpack.rfftfreq(N, d = (xReal[1]-xReal[0])/(2*np.pi))
		frequency = kwargs.get('freq',freqs[idx])  
		frequency/=(2*np.pi) #Convert angular velocity to freq
		amplitude = kwargs.get('amp',(yReal.max()-yReal.min())/2.0)
		phase=kwargs.get('phase',0) #.5*np.pi*((yReal[0]-offset)/amplitude)
		guess = [amplitude, frequency, phase,0]
		try:
			(amplitude, frequency, phase,offset), pcov = optimize.curve_fit(self.sineFunc, xReal, yReal-OFFSET, guess)
			offset+=OFFSET
			ph = ((phase)*180/(np.pi))
			if(frequency<0):
				#print ('negative frq')
				return False

			if(amplitude<0):
				ph-=180

			if(ph<0):ph = (ph+720)%360
			freq=1e6*abs(frequency)
			amp=abs(amplitude)
			pcov[0]*=1e6
			#print (pcov)
			if(abs(pcov[-1][0])>1e-6):
				False
			return [amp, freq, offset,ph]
		except:
			return False

from .templates import ui_SliderAndSpinbox as SliderAndSpinbox
from PyQt4 import QtGui,QtCore
import pyqtgraph as pg



class expeyesWidgets():
	"""
	This class contains methods that simplify setting up and running
	an experiment.
	
	feature list : 
	
	"""

	plotDict = {}
	timers = []
	trace_colors=[(0,255,0),(255,0,0),(255,255,100),(10,255,255)]
	trace_names = ['A1','A2','A3','MIC']
	curves={}
	def __init__(self,*args,**kwargs):
		#sys.path.append('/usr/share/seelablet')
		pass
	
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
		W = self.sliderWidget(min = 5,max = 5000, label = 'SINE' ,units = 'Hz', callback = handler.set_sine)
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

		



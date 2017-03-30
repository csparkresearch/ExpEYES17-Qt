from templates import ui_SliderAndSpinbox as SliderAndSpinbox
from PyQt4 import QtGui,QtCore
import pyqtgraph as pg


class expeyesWidgets():
	"""
	This class contains methods that simplify setting up and running
	an experiment.
	
	feature list : 
	
	"""

	plotDict = {}
	def __init__(self,*args,**kwargs):
		#sys.path.append('/usr/share/seelablet')
		pass
	
	def addPlot(self,**kwargs):
		if 'leftAxis' in kwargs: kwargs['axisItems'] = {'left':kwargs.pop('leftAxis')}
		plot=pg.PlotWidget(enableMenu = False)
		plot.setMouseEnabled(False,True)
		if 'x' in kwargs.get('disableAutoRange',''):plot.disableAutoRange(axis = plot.plotItem.vb.XAxis)
		if 'y' in kwargs.get('disableAutoRange',''):plot.disableAutoRange(axis = plot.plotItem.vb.YAxis)
		plot.getAxis('left').setGrid(170);
		plot.getAxis('bottom').setGrid(170); plot.getAxis('bottom').setLabel('time', units='S')
		limitargs = {a:kwargs.get(a) for a in ['xMin','xMax','yMin','yMax'] if a in kwargs}
		plot.setLimits(**limitargs);
		plot.setXRange(kwargs.get('xMin',0),kwargs.get('xMax',10));
		plot.setYRange(kwargs.get('yMin',-5),kwargs.get('yMax',-5));
		self.plotDict[plot] = []
		return plot
		

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

		



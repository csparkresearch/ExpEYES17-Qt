from PyQt4 import QtGui,QtCore

from templates import ui_plotTemplate as plotTemplate
from utilities.expeyesWidgetsNew import expeyesWidgets


import sys,time,functools

class AppWindow(QtGui.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		self.widgetLayout.setAlignment(QtCore.Qt.AlignTop)

		self.p.sigPlot.connect(self.drawPlot)
		self.p.sigGeneric.connect(self.genericDataReceived)
		self.p.sigError.connect(self.handleError)

		
		# ADD AN OSCILLOSCOPE PLOT TO THE plotLayout
		# This assumes self.plotLayout, and makes a dictionary self.curves with keys 'A1','A2','A3','MIC'
		#You should be able to access after executing this function. self.myCurves is a dictionary of curves with 4 Elements
		stringaxis = pg.AxisItem(orientation='left')
		#ydict = {-4:'-4\n-2',-3:'-3',-2:'-2',-1:'-1',0:'0',1:'1',2:'2',3:'3',4:''}
		ydict = {-4:'',-3:'',-2:'',-1:'',0:'',1:'',2:'',3:'',4:''}
		stringaxis.setTicks([ydict.items()])
		stringaxis.setLabel('Voltage',**{'color': '#FFF', 'font-size': '9pt'})
		stringaxis.setWidth(15)
		
		self.SCOPEPLOT(['A1','A2','A3','MIC'],leftAxis = stringaxis)   #You can also make up your own curve names.
		self.xaxis = self.plot.getAxis('bottom')


		#Add a spacer
		self.SPACER(20)

		# ADD A SINE WIDGET SLIDER WITH NUMBERIC INPUT to the widgetLayout
		self.SINE()
		self.SQR1()
		self.PV1()
		self.PV2()

		
		self.setInterval(100,self.tmp)
		#self.setTimeout(1000,functools.partial(self.capture,'A1',200,3),self.update)

	def tmp(self):
		if self.CH.busy:return
		self.CAPTURE()
		print ('capturing')
	

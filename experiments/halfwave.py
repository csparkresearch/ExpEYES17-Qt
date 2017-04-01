from PyQt4 import QtGui,QtCore

from templates import ui_plotTemplate as plotTemplate
from utilities.expeyesWidgets import expeyesWidgets


import sys,time,functools

class AppWindow(QtGui.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		self.widgetLayout.addWidget(self.addSine(self.p))
		self.xmax = 1e-3 #assume 1mS
		self.plot   = self.addPlot(xMin=0,xMax=self.xmax,yMin=-4,yMax=4, disableAutoRange = 'y',bottomLabel = 'time',bottomUnits='S',enableMenu=False,legend=True)
		self.plot.setMouseEnabled(False,True)
		self.plotLayout.addWidget(self.plot)

		self.C1 = self.addCurve(self.plot,'A1',self.trace_colors[0])
		self.C2 = self.addCurve(self.plot,'A2',self.trace_colors[1])
		
		self.setInterval(1000,functools.partial(self.tmp,1,2,3))

	def tmp(self,a,b,c):
		print (a,b,c)
		

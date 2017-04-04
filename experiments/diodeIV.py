# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from PyQt4 import QtGui,QtCore

from templates import ui_plotTemplate as plotTemplate
from utilities.expeyesWidgetsNew import expeyesWidgets


import sys,time,functools,os
import numpy as np

class AppWindow(QtGui.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		self.widgetLayout.setAlignment(QtCore.Qt.AlignTop)

		
		self.plot = self.newPlot([],xMin=0,xMax=5,yMin=-4,yMax=4, disableAutoRange = 'y',bottomLabel = 'time',bottomUnits='S',enableMenu=False,legend=True)
		self.c1 = self.addCurve(self.plot, 'trace 1' ,'#FFF')
		self.c2 = self.addCurve(self.plot, 'trace 2' ,'#FF0')
		self.c3 = self.addCurve(self.plot, 'trace 3' ,'#F0F')
		x=np.linspace(0,np.pi*2,1000)
		self.c1.setData(x,np.sin(x))
		self.c2.setData(x,3*np.sin(x))
		self.c3.setData(x,5*np.sin(x))
		#Add a vertical spacer in the widgetLayout . about 0.5cm
		self.SPACER(20)

		self.TITLE('Controls')
		self.PV1()
		self.IMAGE(os.path.join('pics','halfwave.png'))
		
		self.setInterval(200,self.update)
		#self.setTimeout(1000,functools.partial(self.capture,'A1',200,3),self.update)

	def update(self):
		print ('update',time.ctime())
		#self.CAPTURE()  #This assumes self.TRIGGER , self.SCOPEPLOT etc were used to initialize. Uses default values wherever possible
	

# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from ..Qt import QtGui, QtCore
from ..templates import ui_plotTemplate as plotTemplate
from ..utilities.expeyesWidgetsNew import expeyesWidgets

from ..expeyes.SENSORS.supported import supported,nameMap
from ..expeyes.sensorlist import sensors as sensorHints

import sys,time,functools,os
import numpy as np

class AppWindow(QtGui.QWidget, plotTemplate.Ui_Form,expeyesWidgets):
	subsection = 'apps'
	helpfile = 'sensor-logger.html'
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.p = kwargs.get('handler',None)
		self.widgetLayout.setAlignment(QtCore.Qt.AlignTop)
		self.widgets.setMinimumWidth(250)
		#Constants
		self.active_device_counter= 0
		self.acquireList={}
		self.POINTS=1000
		self.updatepos=0
		self.xdata=range(self.POINTS)
		self.fps=0;self.lastTime=time.time();self.updatepos=0

		
		self.TITLE('Initialize')
		self.scanButton = self.PUSHBUTTON('Auto Scan')
		self.scanMenu = QtGui.QMenu(); self.scanMenu.setMinimumWidth(self.widgets.width())
		self.scanMenu.addAction('Run Scan', self.autoScan)
		self.scanMenu.addSeparator()
		#self.scanMenu.addAction('Exit', self.askBeforeQuit)
		self.scanButton.setMenu(self.scanMenu)
		self.sensorEntries = {}
		
		self.sensorWidgets = {}

		#Add a vertical spacer in the widgetLayout . about 0.5cm
		self.SPACER(20)
		self.TITLE('Controls')

		self.samplesBtn=QtGui.QSpinBox()
		self.samplesBtn.setRange(10,50000);self.samplesBtn.setPrefix('Samples :');self.samplesBtn.setValue(self.POINTS)
		self.samplesBtn.editingFinished.connect(self.changeSamples)
		self.widgetLayout.addWidget(self.samplesBtn)

		self.PUSHBUTTON('Start Logging' , self.start)
		self.PUSHBUTTON('Stop Logging' , self.stop)
		

		self.plot = self.newPlot([],detailedWidget=True,xMin=0,xMax = self.POINTS, disableAutoRange = 'y',bottomLabel = 'time',bottomUnits='S',enableMenu=False,legend=True)
		self.plot.setYRange(-1000,1000)


		self.start_time = time.time()
		self.timer = self.newTimer()
		#self.setTimeout(1000,functools.partial(self.capture,'A1',200,3),self.update)

	def changeSamples(self):
		val = self.samplesBtn.value()
		self.POINTS = val
		self.xdata=range(self.POINTS)
		for a in self.acquireList:
			item = self.acquireList[a]
			item.ydata = np.zeros((item.handle.NUMPLOTS,self.POINTS))
		self.updatepos = 0
		self.plot.setLimits(xMax = self.POINTS);self.plot.setXRange(0,self.POINTS)


	def autoScan(self):
		lst = self.p.I.I2C.scan()
		for a in self.sensorEntries:
			self.sensorEntries[a][0].setParent(None)
		self.sensorEntries={}
		for a in lst:
			if a in supported:
				action = self.scanMenu.addAction(sensorHints.get(a,['Unknown'])[0]+':%s'%hex(a), functools.partial(self.addSensor,supported[a],a))
				self.sensorEntries[a] = [action,supported[a]]
		self.scanMenu.exec_() #Re-open menu

	class plotItem:
		def __init__(self,handle,ydata,curves):
			self.handle = handle
			self.ydata = ydata
			self.curves=curves

	def addSensor(self,cls,addr):
		print(cls,addr)
		if addr in self.acquireList:
			QtGui.QMessageBox.critical(self,"Address already being logged","The Selected sensor address (%s) is already in use.\nPlease click on `Start Logging` to fetch data"%hex(addr),QtGui.QMessageBox.Ok)
			return
		bridge = cls.connect(self.p.I.I2C,address = addr)
		if bridge:
			self.createMenu(bridge)
			if bridge.NUMPLOTS:
				if hasattr(bridge,'name'):	label = bridge.name
				else: label =''
				colStr = lambda col: hex(col[0])[2:]+hex(col[1])[2:]+hex(col[2])[2:]

				if len(label):self.plot.setLabel('left', label)
				curves=[self.addCurve(self.plot,'%s[%s]'%(label[:10],bridge.PLOTNAMES[a]),self.randomColor()) for a in range(bridge.NUMPLOTS)]
				self.acquireList[addr] = self.plotItem(bridge,np.zeros((bridge.NUMPLOTS,self.POINTS)), curves)
				self.active_device_counter+=1
				self.updatepos=0


	def createMenu(self,bridge):
		label = self.TITLE(bridge.name[:15],removable=True,removeCallback = functools.partial(self.deleteSensor,bridge.ADDRESS))
		menuButton = self.PUSHBUTTON('Options')
		menu = QtGui.QMenu()
		menuButton.setMenu(menu)

		#sub_menu = QtGui.QMenu('%s:%s'%(hex(bridge.ADDRESS),bridge.name[:15]))
		for i in bridge.params: 
			mini=menu.addMenu(i) 
			for a in bridge.params[i]:
				Callback = functools.partial(getattr(bridge,i),a)
				mini.addAction(str(a),Callback)
		menu.addSeparator()
		#menu.addAction('Remove This Sensor',functools.partial(self.deleteSensor,bridge.ADDRESS))
		#self.sensorWidgets[bridge.ADDRESS] = [menuButton]
		label.addAssociatedWidget(menuButton)

	def deleteSensor(self,addr):
		item = self.acquireList.pop(addr)
		for a in item.curves:
			self.removeCurve(self.plot,a)
			self.plot.leg.removeItem(a.name())
		
	class data:
		def __init__(self):
			self.x=np.zeros(2000)
			self.y=np.zeros(2000)
			self.samples = 0
		def getX(self):
			return self.x[:self.samples]
		def getY(self):
			return self.y[:self.samples]


	def update(self):
		#print ('update',time.ctime())
		#if self.pauseBox.isChecked():return
		for addr in self.acquireList:
			item = self.acquireList[addr]
			need_data=False
			for a in item.curves:
				a.checked = a.isEnabled()
				if a.checked: 
					need_data=True
			if need_data:			
				vals=item.handle.getRaw()
				if not vals:continue
				for X in range(len(item.curves)):
					item.ydata[X][self.updatepos] = vals[X]
				if self.updatepos%20==0:
					for a in range(len(item.curves)):
						if item.curves[a].checked:item.curves[a].setData(self.xdata,item.ydata[a])
		#N2.readADC(10)
		if len(self.acquireList):
			self.updatepos+=1
			if self.updatepos>=self.POINTS:self.updatepos=0
		
			now = time.time()
			dt = now - self.lastTime
			self.lastTime = now
			if self.fps is None:
				self.fps = 1.0/dt
			else:
				s = np.clip(dt*3., 0, 1)
				self.fps = self.fps * (1-s) + (1.0/dt) * s
			if not self.updatepos%100 :self.plot.setTitle('%0.2f fps' % (self.fps) )



	def start(self):
		self.start_time = time.time()
		self.setInterval(self.timer,1,self.update)

		#self.c1 = self.addCurve(self.plot, 'trace 1' ,'#FFF')
		#self.c2 = self.addCurve(self.plot, 'trace 2' ,'#FF0')
		#self.c3 = self.addCurve(self.plot, 'trace 3' ,'#F0F')
		#self.c4 = self.addCurve(self.plot, 'trace 4' ,'#F0F')
		#self.removeCurve(self.plot,self.c4)


	def stop(self):
		self.timer.stop()
		self.timer.timeout.disconnect()
		pass

from __future__ import print_function
import os,string,time
from collections import OrderedDict
import time, os,functools,importlib
from CommunicationHandlerQt import communicationHandler
import numpy as np
from PyQt4 import QtGui,QtCore
import pyqtgraph as pg
import pyqtgraph.exporters

from templates import ui_layoutNew as layoutNew
from utilities.fileBrowser import fileBrowser
from utilities.expeyesWidgets import expeyesWidgets


import sys,time

class AppWindow(QtGui.QMainWindow, layoutNew.Ui_MainWindow,expeyesWidgets):
	sigExec = QtCore.pyqtSignal(str,object,object)
	xmax = 20 #mS
	expts = OrderedDict([
	('Half-wave rectifier','halfwave'),
	('Oscilloscope','scope'),
	 ])


	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.statusBar = self.statusBar()
		global app
		self.fileBrowser = fileBrowser(thumbnail_directory = 'ExpEYES_thumbnails',app=app)#,clickCallback = self.showNewPlot)
		self.saveLayout.addWidget(self.fileBrowser)

		### Prepare the communication handler, and move it to a thread.
		self.CH = communicationHandler()
		self.worker_thread = QtCore.QThread()
		self.CH.moveToThread(self.worker_thread)
		self.sigExec.connect(self.CH.process)

		self.CH.sigStat.connect(self.showStatus)
		self.CH.sigGeneric.connect(self.genericDataReceived)

		self.worker_thread.start()
		self.worker_thread.setPriority(QtCore.QThread.HighPriority)

		if self.CH.connected==False:
			self.showStatus("System Status | Device not found. Dummy mode.",True)
		else:
			self.showStatus("System Status | Connected to device. Version : %s"%str(self.CH.get_version()))

		if self.CH.I.timestamp is not None:self.setWindowTitle(self.CH.I.generic_name + ' : '+self.CH.I.H.version_string.decode("utf-8")+' : '+str(self.CH.I.timestamp))
		else:self.setWindowTitle(self.CH.I.generic_name + ' : '+self.CH.I.H.version_string.decode("utf-8")+' : Not calibrated')

		self.exitBtn = QtGui.QPushButton("EXIT")
		self.exitBtn.clicked.connect(self.askBeforeQuit)
		self.exitBtn.setStyleSheet("height: 10px;padding:3px;color: #FF2222;")
		self.statusBar.addPermanentWidget(self.exitBtn)
		

		#### Set initial configuration
		#self.setGainA1(2);self.setGainA2(2)

		### Test some new widgets
		#Do not provide callbacks to the eyes17 instance. It will break the threaded environment
		
		for a in self.expts:
			self.menuLoad.addAction(a,functools.partial(self.launchExperiment,a))
		self.expt=None
		self.actionSave.triggered.connect(self.save)

	def save(self):
		print ('wrong save fnction. inheritance not working properly. save from expeyesWidgetsNew must be called')

	def launchExperiment(self,name):
		fname = self.expts[name]
		if name not in self.expts:
			print ('missing experiment',name)
			return
		if self.expt: #Close any running instance
			try:
				self.expt.windUp()
				self.expt.close()
				self.expt.destroy()
			except Exception as e:print (e.message)

		FILE = importlib.import_module('experiments.'+fname)
		self.expt = FILE.AppWindow(handler = self.CH)
		
		#from experiments.halfwave import AppWindow
		#self.expt = AppWindow(handler = self.CH)
		self.experimentLayout.addWidget(self.expt)
		self.expt.show()
		print (name,fname)

	def tabChanged(self,index):
		print (index)

	def setTrigger(self,value):
			self.trigger_level=self.currentRange['A1']*value.pos()[1]/4.
			self.CH.configure_trigger(self.trigger_channel,self.triggerChannelName,self.trigger_level,resolution=10,prescaler=5)

	def closeEvent(self, evnt):
		#evnt.ignore()
		#self.askBeforeQuit()
		if self.worker_thread.isRunning():
			self.worker_thread.quit()
			self.worker_thread.wait()
	
	def askBeforeQuit(self):
		reply = QtGui.QMessageBox.question(self, 'Warning', 'Really quit?', QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
		if reply == QtGui.QMessageBox.Yes:
			global app
			app.quit()

	def showStatus(self,msg,error=None):
		if error: self.statusBar.setStyleSheet("color:#FF0000")
		else: self.statusBar.setStyleSheet("color:#000000")
		self.statusBar.showMessage(msg)



	##############  HANDLE DATA RETURNED FROM WORKER THREAD   #####################

	def genericDataReceived(self,name,res):
		if name == 'get_states':
			for nm,wid in zip(['IN2','SQR1_OUT','OD1_OUT','SEN','CCS'],[self.DIN_IN2,self.DIN_SQR1,self.DIN_OD1,self.DIN_SEN,self.DIN_CCS]):
				wid.setStyleSheet('''background-color: %s;'''%('#0F0' if res[nm] else '#F00'))
		elif name == 'configure_trigger':
			pass
		else:
			print (name,res)

	def handleError(self,name,err):
		self.showStatus(name+err,True)
		print ('packet drop',name,err)
		if 'fetch' in name: self.timer.singleShot(10,self.update)

	##############  HANDLE DATA RETURNED FROM WORKER THREAD   #####################


	def clearPlot(self):
		self.x = [];self.y=[];
		for a in self.curves[self.plot]:a.clear()

	def loadPlot(self,fname):
		self.showStatus("Loaded data from file | %s"%fname)
		self.fileBrowser.loadFromFile( self.plot,self.curves[self.plot],fname ) 
		self.tabWidget.setCurrentIndex(0)





if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = AppWindow()
	myapp.show()
	sys.exit(app.exec_())



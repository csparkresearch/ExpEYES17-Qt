# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
# cspark_expeyes - Qt based Application stack to support ExpEYES-17.
#
# Source Link : https://github.com/csparkresearch/ExpEYES17-Qt
#
# Copyright (C) 2016 by Jithin B.P. <jithinbp@gmail.com>
# Contributors:
# - Jithin B.P
# - Georges Khaznadar
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



from __future__ import print_function

from .Qt import QtGui,QtCore,QtWidgets

import os,string,time,sys

from .utilities.expeyesWidgetsNew import expeyesWidgets
from .templates import ui_layoutNew as layoutNew
from collections import OrderedDict

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s


class AppWindow(QtWidgets.QMainWindow,expeyesWidgets, layoutNew.Ui_MainWindow):
	sigExec = QtCore.pyqtSignal(str,object,object)
	sigHelp = QtCore.pyqtSignal(str)
	xmax = 20 #mS
	TandM = OrderedDict([
	('Oscilloscope','simplescope'),
	('I2C Sensor Data Logger','sensorLogger'),
	('Data-Logger','data-logger'),
	 ])

	electrical = OrderedDict([
	('RC Circuits','rc-circuit'),
	('RL Circuits','rl-circuit'),
	('RLC Discharge','rlc-discharge'),
	('RLC Steady State','rlc-steady'),
	 ])

	electronics = OrderedDict([
	('Half-wave rectifier','halfwave'),
	('Full-wave rectifier','fullwave'),
	('Diode IV','diode-IV'),
	('Diode IV Hysterisis','diode-IV-hysterisis'),
	('Diode Clipping','clipping'),
	('Diode Clamping','clamping'),
	('Transistor CE','transistor-CE'),
	 ])


	ics = OrderedDict([
	('Operational amplifiers','opamps'),
	('Clock Divider','simplescope'),       ## the help file is overriden
	 ])

	physics = OrderedDict([
	('AC Generator','acgen'),
	('Simple Pendulum','pendulum'),
	('Ultrasound Echo SR04','sr04-dist'),
	('Interference of Sound','sound-beats'),
	('Plotting etc','example'),
	 ])

	schoolLevel = OrderedDict([
	('Transformer','simplescope'),
	 ])


	helpfileOverride = OrderedDict([
	('Clock Divider','clock-divider.html'),
	('Transformer','transformer.html'),
	 ])

	exptGroups = OrderedDict([
	('Test And Measurement',TandM),
	('Electrical',electrical),
	('Electronics',electronics),
	('Op-amps and more',ics),
	('Physics',physics),
	('School Level',schoolLevel)
	])

	defaultExperiment = 'Oscilloscope'

	allExpts = {}
	for a in exptGroups:
		allExpts.update(exptGroups[a])

	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.statusBar = self.statusBar()
		global app
		self.experimentTabIndex = 1
		from .utilities.fileBrowser import fileBrowser

		self.fileBrowser = fileBrowser(thumbnail_directory = 'ExpEYES_thumbnails',app=kwargs.get('app',None))#,clickCallback = self.showNewPlot)
		self.saveLayout.addWidget(self.fileBrowser)

		try:
			from .utilities.helpBrowser import helpBrowser
			self.helpBrowser = helpBrowser()
			self.helpLayout.addWidget(self.helpBrowser)
			helpPath = os.path.join(os.path.dirname(sys.argv[0]),'help','MD_HTML','index.html')
			self.helpBrowser.setFile(helpPath)
			self.tabWidget.setCurrentIndex(0)
			self.showStatus("System Status | Connecting to device...",True)

		except Exception as e:
			print ('failed to import help browser. check QtWebkit Version',e)
			self.helpBrowser = None
		### Prepare the communication handler, and move it to a thread.
		from .CommunicationHandlerQt import communicationHandler
		self.CH = communicationHandler(connectHandler = self.deviceConnected,disconnectHandler = self.deviceDisconnected, connectionDialogHandler= self.connectionDialog)
		self.worker_thread = QtCore.QThread()
		self.CH.moveToThread(self.worker_thread)
		self.sigExec.connect(self.CH.process)

		self.CH.sigStat.connect(self.showStatus)
		#self.CH.sigGeneric.connect(self.genericDataReceived)

		self.worker_thread.start()
		self.worker_thread.setPriority(QtCore.QThread.HighPriority)


		############ MAKE AN EXIT BUTTON AND STYLE IT. SHOULD IDEALLY BE DONE IN THE LAYOUT.UI FILE USING QT4-DESIGNER.
		self.exitBtn = QtWidgets.QPushButton("EXIT")
		self.exitBtn.clicked.connect(self.askBeforeQuit)
		self.exitBtn.setStyleSheet("height: 10px;padding:3px;color: #FF2222;")
		self.statusBar.addPermanentWidget(self.exitBtn)

		self.menuLoad = QtWidgets.QMenu(self.menuBar)
		self.menuLoad.setObjectName(_fromUtf8("menuLoad"))

		self.allMenus = []
		for grp in self.exptGroups:
			menu = QtWidgets.QMenu(self.menuBar)
			menu.setTitle(grp)
			for a in self.exptGroups[grp]:
				#print ('adding',grp,a)
				menu.addAction(a,functools.partial(self.launchExperiment,a))
			self.menuBar.addAction(menu.menuAction())
			self.allMenus.append(menu)


		self.expt=None
		self.actionSave.triggered.connect(self.savePlots)

	def connectionDialog(self):
		reply = QtWidgets.QMessageBox.question(self, 'Connection', 'New Device Found. Connect?', QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
		if reply == QtWidgets.QMessageBox.Yes:
			print (reply)
			self.CH.connectToDevice()
			#self.selectDevice()
		
	def deviceConnected(self):
		if self.CH.I.timestamp is not None:self.setWindowTitle(self.CH.I.generic_name + ' : '+self.CH.I.H.version_string.decode("utf-8")+' : '+str(self.CH.I.timestamp))
		else:self.setWindowTitle(self.CH.I.generic_name + ' : '+self.CH.I.H.version_string.decode("utf-8")+' : Not calibrated')
		if self.CH.I.connected:
			self.showStatus("System Status | Connected to device. Version : %s"%str(self.CH.get_version()))
			self.launchExperiment(self.defaultExperiment)
			self.tabWidget.setCurrentIndex(1)
		else:
			self.tabWidget.setCurrentIndex(0)
			self.showStatus("System Status | Device not found. Dummy mode.",True)
		
	def deviceDisconnected(self):
		self.tabWidget.setCurrentIndex(0)
		self.showStatus("System Status | Device disconnected.",True)
		if self.expt: #Close any running instance
			try:
				try:self.expt.windUp()
				except Exception as e:print (e.message)
				self.expt.close()
				self.expt.destroy()
				self.experimentLayout.removeWidget(self.expt)
				self.expt.deleteLater()
				#self.expt = None
			except Exception as e:print (e.message)
		QtGui.QMessageBox.critical(self, "Device Disconnected", "A communication error occurred, or the device was unexpectedly removed. Please reconnect the hardware.")
		
	def savePlots(self):
		print ('wrong save fnction. inheritance not working properly. save from expeyesWidgetsNew must be called. This is defined in expeyesWidgetsNew')

	def launchExperiment(self,name):
		fname = self.allExpts[name]
		if name not in self.allExpts:
			print ('missing experiment',name)
			return
		if self.expt: #Close any running instance
			try:
				try:self.expt.windUp()
				except Exception as e:print (e.message)
				self.expt.close()
				self.expt.destroy()
				self.experimentLayout.removeWidget(self.expt)
				self.expt.deleteLater()
				#self.expt = None
			except Exception as e:print (str(e))

		FILE = importlib.import_module('.experiments.'+fname,package='SPARK17')
		self.expt = FILE.AppWindow(handler = self.CH)
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.experimentTab),name)
		
		#from experiments.halfwave import AppWindow
		#self.expt = AppWindow(handler = self.CH)
		self.experimentLayout.addWidget(self.expt)
		self.expt.show()
		try:
			if name in self.helpfileOverride:
				helpPath = os.path.join(os.path.dirname(sys.argv[0]),'help','MD_HTML','apps',self.helpfileOverride[name])
				self.helpBrowser.setFile(helpPath)
				#print ('help override',helpPath)
			elif hasattr(self.expt,'subsection'):
				helpPath = os.path.join(os.path.dirname(sys.argv[0]),'help','MD_HTML',self.expt.subsection,self.expt.helpfile)
				self.helpBrowser.setFile(helpPath)
		except Exception as e:
			print ('help widget not loaded. install QtWebkit',e)

	def tabChanged(self,val):
		pass
		
	def closeEvent(self, evnt):
		evnt.ignore()
		#self.askBeforeQuit()
		if self.worker_thread.isRunning():
			self.worker_thread.quit()
			self.worker_thread.wait()
		sys.exit(0)
	
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

	'''
	def genericDataReceived(self,name,res):
		if name == 'get_states':
			for nm,wid in zip(['IN2','SQR1_OUT','OD1_OUT','SEN','CCS'],[self.DIN_IN2,self.DIN_SQR1,self.DIN_OD1,self.DIN_SEN,self.DIN_CCS]):
				wid.setStyleSheet("background-color: %s;"%('#0F0' if res[nm] else '#F00'))
		else:
			pass
	'''
	def handleError(self,name,err):
		self.showStatus(name+err,True)
		print ('packet drop',name,err)

	##############  HANDLE DATA RETURNED FROM WORKER THREAD   #####################


	def clearPlot(self):
		self.x = [];self.y=[];
		for a in self.curves[self.plot]:a.clear()

	def loadPlot(self,fname):
		self.showStatus("Loaded data from file | %s"%fname)
		self.fileBrowser.loadFromFile( self.plot,self.curves[self.plot],fname ) 
		self.tabWidget.setCurrentIndex(self.experimentTabIndex)

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	# Create and display the splash screen
	splash_pix = QtGui.QPixmap(os.path.join(os.path.dirname(sys.argv[0]),os.path.join('templates','splash.png')))
	splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
	splash.setMask(splash_pix.mask())
	splash.show()
	for a in range(10):
		app.processEvents()
		time.sleep(0.01)

	import time, os,functools,importlib
	from .CommunicationHandlerQt import communicationHandler
	import numpy as np
	import pyqtgraph as pg
	import pyqtgraph.exporters

	myapp = AppWindow(app=app)
	myapp.show()
	splash.finish(myapp)
	sys.exit(app.exec_())



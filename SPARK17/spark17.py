# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
# cspark_expeyes - Qt based Application stack to support ExpEYES-17.
#
# Source Link : https://github.com/csparkresearch/ExpEYES17-Qt
#
# Copyright (C) 2016, 2017 by Jithin B.P. <jithinbp@gmail.com>
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

import time,functools,importlib
import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters


from .utilities.expeyesWidgetsNew import expeyesWidgets
from .templates import ui_layoutNew as layoutNew
from collections import OrderedDict

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

_translate = QtCore.QCoreApplication.translate

class AppWindow(QtWidgets.QMainWindow,expeyesWidgets, layoutNew.Ui_MainWindow):
	sigExec = QtCore.pyqtSignal(str,object,object)
	sigHelp = QtCore.pyqtSignal(str)
	xmax = 20 #mS


	def __init__(self, parent=None, path={}, **kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.statusBar = self.statusBar()
		self.curPath = path["current"]
		self.path=path
		
		global app
		# the following class static variables must be initialized
		# *after* the initialization of translation domains, so they
		# are initialized during the first and only instantiation of
		# an object of AppWindow
		AppWindow.TandM = OrderedDict([
			(_translate("app",'Oscilloscope'),'simplescope'),
			(_translate("app",'I2C Sensor Data Logger'),'sensorLogger'),
			(_translate("app",'Data-Logger'),'data-logger'),
		])

		AppWindow.electrical = OrderedDict([
			(_translate("app",'RC Circuits'),'rc-circuit'),
			(_translate("app",'RL Circuits'),'rl-circuit'),
			(_translate("app",'RLC Discharge'),'rlc-discharge'),
			(_translate("app",'RLC Steady State'),'rlc-steady'),
		])

		AppWindow.electronics = OrderedDict([
			(_translate("app",'Half-wave rectifier'),'halfwave'),
			(_translate("app",'Full-wave rectifier'),'fullwave'),
			(_translate("app",'Diode IV'),'diode-IV'),
			(_translate("app",'Diode IV Hysterisis'),'diode-IV-hysterisis'),
			(_translate("app",'Diode Clipping'),'clipping'),
			(_translate("app",'Diode Clamping'),'clamping'),
			(_translate("app",'Transistor CE'),'transistor-CE'),
		])


		AppWindow.ics = OrderedDict([
			(_translate("app",'Operational amplifiers'),'opamps'),
			(_translate("app",'Clock Divider'),'simplescope'),	   ## the help file is overriden
		])

		AppWindow.physics = OrderedDict([
			(_translate("app",'AC Generator'),'acgen'),
			(_translate("app",'Simple Pendulum'),'pendulum'),
			(_translate("app",'Ultrasound Echo SR04'),'sr04-dist'),
			(_translate("app",'Interference of Sound'),'sound-beats'),
			(_translate("app",'Plotting etc'),'example'),
		])

		AppWindow.schoolLevel = OrderedDict([
			(_translate("app",'Transformer'),'simplescope'),
		])


		AppWindow.helpfileOverride = OrderedDict([
			(_translate("app",'Clock Divider'),'clock-divider.html'),
			(_translate("app",'Transformer'),'transformer.html'),
		])

		AppWindow.exptGroups = OrderedDict([
			(_translate("app",'Test And Measurement'),AppWindow.TandM),
			(_translate("app",'Electrical'),AppWindow.electrical),
			(_translate("app",'Electronics'),AppWindow.electronics),
			(_translate("app",'Op-amps and more'),AppWindow.ics),
			(_translate("app",'Physics'),AppWindow.physics),
			(_translate("app",'School Level'),AppWindow.schoolLevel)
		])

		AppWindow.defaultExperiment = 'Oscilloscope'

		AppWindow.allExpts = {}
		for a in AppWindow.exptGroups:
			AppWindow.allExpts.update(AppWindow.exptGroups[a])


		self.experimentTabIndex = 1
		from .utilities.fileBrowser import fileBrowser

		self.fileBrowser = fileBrowser(thumbnail_directory = 'ExpEYES_thumbnails',app=kwargs.get('app',None))#,clickCallback = self.showNewPlot)
		self.saveLayout.addWidget(self.fileBrowser)

		try:
			from .utilities.helpBrowser import helpBrowser
			self.helpBrowser = helpBrowser()
			self.helpLayout.addWidget(self.helpBrowser)
			self.helpBrowser.setFile(os.path.join(self.path["help"],"index.html"))
			self.tabWidget.setCurrentIndex(0)
			self.showStatus(_translate("app","System Status | Connecting to device..."),True)

		except Exception as e:
			print (_translate("app",'failed to import help browser. check QtWebkit Version'),e)
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
		reply = QtWidgets.QMessageBox.question(self, _translate("app",'Connection'), _translate("app",'New Device Found. Connect?'), QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
		if reply == QtWidgets.QMessageBox.Yes:
			print (reply)
			self.CH.connectToDevice()
			#self.selectDevice()
		
	def deviceConnected(self):
		if self.CH.I.timestamp is not None:self.setWindowTitle(self.CH.I.generic_name + ' : '+self.CH.I.H.version_string.decode("utf-8")+' : '+str(self.CH.I.timestamp))
		else:self.setWindowTitle(self.CH.I.generic_name + ' : '+self.CH.I.H.version_string.decode("utf-8")+_translate("app",' : Not calibrated'))
		if self.CH.I.connected:
			self.showStatus(_translate("app","System Status | Connected to device. Version : %s") %str(self.CH.get_version()))
			self.launchExperiment(self.defaultExperiment)
			self.tabWidget.setCurrentIndex(1)
		else:
			self.tabWidget.setCurrentIndex(0)
			self.showStatus(_translate("app","System Status | Device not found. Dummy mode."),True)
		
	def deviceDisconnected(self):
		self.tabWidget.setCurrentIndex(0)
		self.showStatus(_translate("app","System Status | Device disconnected."),True)
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
		QtGui.QMessageBox.critical(self, _translate("app","Device Disconnected"),
								   _translate("app","A communication error occurred, or the device was unexpectedly removed. Please reconnect the hardware."))

	def savePlots(self):
		print (_translate("app",'wrong save fnction. inheritance not working properly. save from expeyesWidgetsNew must be called. This is defined in expeyesWidgetsNew'))

	def launchExperiment(self,name):
		fname = self.allExpts[name]
		if name not in self.allExpts:
			print (_translate("app",'missing experiment'),name)
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
				helpPathApp = os.path.join(self.path["help"],"apps",self.helpfileOverride[name])
				self.helpBrowser.setFile(helpPathApp)
			elif hasattr(self.expt,'subsection'):
				helpPathSub = os.path.join(self.path["help"],self.expt.subsection,self.expt.helpfile)
				self.helpBrowser.setFile(helpPathSub)
		except Exception as e:
			print (_translate("app",'help widget not loaded. install QtWebkit'),e)

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
		reply = QtGui.QMessageBox.question(self, _translate("app",'Warning'), _translate("app",'Really quit?'), QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
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
		print (_translate("app",'packet drop'),name,err)

	##############  HANDLE DATA RETURNED FROM WORKER THREAD   #####################


	def clearPlot(self):
		self.x = [];self.y=[];
		for a in self.curves[self.plot]:a.clear()

	def loadPlot(self,fname):
		self.showStatus("Loaded data from file | %s"%fname)
		self.fileBrowser.loadFromFile( self.plot,self.curves[self.plot],fname ) 
		self.tabWidget.setCurrentIndex(self.experimentTabIndex)

def translators(langDir, lang=None):
	"""
	create a list of translators
	@param langDir a path containing .qm translation
	@param lang the preferred locale, like en_IN.UTF-8, fr_FR.UTF-8, etc.
	@result a list of QtCore.QTranslator instances
	"""
	if lang==None:
			lang=QtCore.QLocale.system().name()
	result=[]
	qtTranslator=QtCore.QTranslator()
	qtTranslator.load("qt_" + lang,
			QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath))
	result.append(qtTranslator)

	# path to the translation files (.qm files)
	sparkTranslator=QtCore.QTranslator()
	sparkTranslator.load(lang, langDir);
	result.append(sparkTranslator)
	return result

def firstExistingPath(l):
	"""
	Returns the first existing path taken from a list of
	possible paths.
	@param l a list of paths
	@return the first path which exists in the filesystem, or None
	"""
	for p in l:
		if os.path.exists(p):
			return p
	return None

def common_paths():
	"""
	Finds common paths
	@result a dictionary of common paths
	"""
	path={}
	curPath = os.path.dirname(os.path.realpath(__file__))
	path["current"] = curPath
	sharedPath = "/usr/share/expeyes17"
	path["translation"] = firstExistingPath(
			[os.path.join(p, "lang") for p in
			 (curPath, sharedPath,)])
	path["template"] = firstExistingPath(
			[os.path.join(p,'templates') for p in
			 (curPath, sharedPath,)])
	path["splash"] = firstExistingPath(
			[os.path.join(p,'templates','splash.png') for p in
			 (curPath, sharedPath,)])
	lang=QtCore.QLocale.system().name()
	shortLang=lang[:2]
	path["help"] = firstExistingPath(
			[os.path.join(p,'MD_HTML') for p in
			 (os.path.join(curPath,"help_"+lang),
			  os.path.join(sharedPath,"help_"+lang),
			  os.path.join(curPath,"help_"+shortLang),
			  os.path.join(sharedPath,"help_"+shortLang),
			  os.path.join(curPath,"help"),
			  os.path.join(sharedPath,"help"),
			  )
			 ])
	return path

def main_run():
	path = common_paths()
	app = QtWidgets.QApplication(sys.argv)
	for t in translators(path["translation"]):
		app.installTranslator(t)

	# Create and display the splash screen
	splash_pix = QtGui.QPixmap(path["splash"])
	splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
	splash.setMask(splash_pix.mask())
	splash.show()
	for a in range(10):
		app.processEvents()
		time.sleep(0.01)

	myapp = AppWindow(app=app, path=path)
	myapp.show()
	splash.finish(myapp)
	sys.exit(app.exec_())

if __name__ == "__main__":
	main_run()

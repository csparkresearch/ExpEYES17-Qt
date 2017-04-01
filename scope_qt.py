from __future__ import print_function
import os,string,time
from collections import OrderedDict
import time, os
from CommunicationHandlerQt import communicationHandler
import numpy as np
from PyQt4 import QtGui,QtCore
import pyqtgraph as pg
import pyqtgraph.exporters

from templates import ui_layout as layout
from utilities.fileBrowser import fileBrowser
from utilities.expeyesWidgets import expeyesWidgets


import sys,time

class AppWindow(QtGui.QMainWindow, layout.Ui_MainWindow,expeyesWidgets):
	sigExec = QtCore.pyqtSignal(str,object,object)
	xmax = 20 #mS
	expts = OrderedDict([
	('Select Experiment',''),
	('Control PVS','change-pvs'),
	('Study of AC Circuits','ac-circuit'),
	('RC Circuit','RCcircuit'),
	('RL Circuit','RLcircuit'),
	('RLC Discharge','RLCdischarge'),
	('EM Induction','induction'),
	('Diode IV','diode_iv'),
	('Transistor CE','transistor'),
	('AM and FM', 'amfm'),
	('Frequency Response','freq-response'),
	('Velocity of Sound','velocity-sound'),
	('Interference of Sound', 'interference-sound'),
	('Capture Burst of Sound','sound-burst'),
	('Driven Pendulum','driven-pendulum'),
	('Rod Pendulum','rodpend'),
	('Pendulum Wavefrorm','pendulum'),
	('PT100 Sensor', 'pt100'),
	('Stroboscope', 'stroboscope'),
	('Data Logger', 'logger'),
	('HY-SRF05 Echo module', 'gecho'),
	('Calibrate','calibrate')
	 ])
	chan4 = [ [1, [], [],0,[],0,0,0,None,None,0.0, 2],\
		  [0, [], [],0,[],0,0,0,None,None,0.0, 2],\
		  [0, [], [],0,[],0,0,0,None,None,0.0, 0],\
		  [0, [], [],0,[],0,0,0,None,None,0.0, 0] \
		] # Source, t, v, fitflag, vfit, amp, freq, phase, widget1, widget2, display offset in volts
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
		self.CH.sigPlot.connect(self.drawPlot)
		self.CH.sigGeneric.connect(self.genericDataReceived)
		self.CH.sigError.connect(self.handleError)

		self.worker_thread.start()
		self.worker_thread.setPriority(QtCore.QThread.HighPriority)

		if self.CH.connected==False:
			self.showStatus("System Status | Device not found. Dummy mode.",True)
		else:
			self.showStatus("System Status | Connected to device. Version : %s"%str(self.CH.get_version()))

		if self.CH.I.timestamp is not None:self.setWindowTitle(self.CH.I.generic_name + ' : '+self.CH.I.H.version_string.decode("utf-8")+' : '+str(self.CH.I.timestamp))
		else:self.setWindowTitle(self.CH.I.generic_name + ' : '+self.CH.I.H.version_string.decode("utf-8")+' : Not calibrated')

		self.experimentBox.addItems(self.expts.keys())
		self.exitBtn = QtGui.QPushButton("EXIT")
		self.exitBtn.clicked.connect(self.askBeforeQuit)
		self.exitBtn.setStyleSheet("height: 10px;padding:3px;color: #FF2222;")
		self.statusBar.addPermanentWidget(self.exitBtn)

		
		stringaxis = pg.AxisItem(orientation='left')
		#ydict = {-4:'-4\n-2',-3:'-3',-2:'-2',-1:'-1',0:'0',1:'1',2:'2',3:'3',4:''}
		ydict = {-4:'',-3:'',-2:'',-1:'',0:'',1:'',2:'',3:'',4:''}
		stringaxis.setTicks([ydict.items()])
		stringaxis.setLabel('Voltage',**{'color': '#FFF', 'font-size': '9pt'})
		stringaxis.setWidth(15)
		
		self.plot   = self.addPlot(xMin=0,xMax=self.xmax,yMin=-4,yMax=4, disableAutoRange = 'y',bottomLabel = 'time',bottomUnits='S',leftAxis = stringaxis,enableMenu=False)
		self.plot.setMouseEnabled(False,True)
		self.plot_area.addWidget(self.plot)
		self.xaxis = self.plot.getAxis('bottom')

		self.channels_enabled=[1,1,1,1]
		self.channelButtons = [self.A1,self.A2,self.A3,self.MIC]
		self.chan1Box.setStyleSheet("QComboBox::down-arrow{  top: 1px;left: 1px;}border-radius: 3px;border: 1px solid rgb%s"%str(self.trace_colors[0]))
		for a,col in zip(self.channelButtons,self.trace_colors):
			a.setStyleSheet("color:rgb%s"%str(col))

		self.MAX_SAMPLES=2000
		self.max_samples_per_channel=[0,self.MAX_SAMPLES/4,self.MAX_SAMPLES/4,self.MAX_SAMPLES/4,self.MAX_SAMPLES/4]
		self.samples = [self.MAX_SAMPLES/4];self.timebase=2;self.chan1remap='A1'
		self.chan1Box.addItems(self.CH.I.allAnalogChannels)
		
		self.plot.addLegend(offset=(-10,30))
		for name,col in zip(self.trace_names,self.trace_colors):
			self.addCurve(self.plot,name,col)

		##### SET GAIN COMBOBOX VALUES
		self.Ranges12 = ['16 V', '8 V','4 V', '2 V', '1 V', '.5V']	# Voltage ranges for A1 and A2
		self.rangevals12 = [16,8,4,2.5,1.5,1,0.5]
		self.Ranges34 = ['4 V', '2 V', '1 V', '.5V']					# Voltage ranges for A3 and MIC
		self.rangevals34 = [4,2,1,0.5]

		self.currentRange=[4,4,4,4]
		##### SET GAIN COMBOBOX VALUES

		##### SET TIMING INTERVAL BOX CONTENTS
		for a in [self.edge1chan,self.edge2chan]: 
			a.addItems(self.CH.I.digital_inputs)
		for x in range(4):
				item = QtGui.QTableWidgetItem();self.timingResults.setItem(x, 0, item);item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
				item = QtGui.QTableWidgetItem();self.timingResults.setItem(x, 1, item);item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)



		for a in [self.Edge1chan,self.Edge2chan]: 
			a.addItems(self.CH.I.digital_inputs)
		for x in range(4):
				item = QtGui.QTableWidgetItem();self.TimingResults.setItem(x, 0, item);item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
				item = QtGui.QTableWidgetItem();self.TimingResults.setItem(x, 1, item);item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)




		##### SET TIMING INTERVAL BOX CONTENTS

		self.trig = self.addInfiniteLine(self.plot,angle=0, movable=True,cursor = QtCore.Qt.SizeVerCursor,tooltip="Trigger level. Enable the trigger checkbox, and drag up/down to set the level",value = 0,ignoreBounds=False)

		self.currentPeak = None
		self.trigger = False
		self.trigger_channel=0
		self.triggerChannelName='A1'
		self.trigger_level=0
		self.trig.sigPositionChanged.connect(self.setTrigger)
		self.setTrigger(self.trig)
		self.labelTexts={}
		self.setLabels()

		#### Set initial configuration
		self.setGainA1(2);self.setGainA2(2)

		self.auto_refresh_position=0
		self.MIC.setChecked(True)
		self.timer = QtCore.QTimer()
		self.timer.singleShot(10,self.update)

		### Test some new widgets
		#Do not provide callbacks to the eyes17 instance. It will break the threaded environment
		self.controlLayout.addWidget(self.addSine(self.CH))
		self.controlLayout.addWidget(self.addSQR1(self.CH))
		self.controlLayout.addWidget(self.addPV1(self.CH) )
		self.controlLayout.addWidget(self.addPV2(self.CH))
		#self.loadExperiment()


	def loadExperiment(self):
		self.tabWidget.setCurrentIndex(2); time.sleep(0.3)
		from experiments.halfwave import AppWindow
		self.expt = AppWindow(handler = self.CH.I)
		self.experimentLayout.addWidget(self.expt)
		self.expt.show()

	def tabChanged(self,index):
		print (index)
		if index!=2: #changed from experiments tab. remove it.
			for a in reversed(self.timers):
				a.stop()
				self.timers.remove(a)

	def setTrigger(self,value):
			self.trigger_level=self.currentRange[0]*value.pos()[1]/4.
			self.CH.configure_trigger(self.trigger_channel,self.triggerChannelName,self.trigger_level,resolution=10,prescaler=5)

	def setLabels(self):
		for a in self.labelTexts:
			for b in self.labelTexts[a]:
				self.plot.removeItem(b)		
		self.labelTexts={}

		xshift=self.xaxis.range[0]
		positions = np.linspace(-4,4,9)
		for a in range(4):
			self.labelTexts[a]=[]
			V = self.currentRange[a]
			#name = self.trace_names[a]
			#source = self.CH.I.analogInputSources[name]
			vpd=V/4
			for ypos in positions:
				txt ='''<span style="color: rgb%s; font-size: 8pt;">%.2f </span>'''%(self.trace_colors[a],ypos*vpd)
				lbl = pg.TextItem(html=txt, anchor=(-.5,0),angle=45);lbl.setPos(xshift, ypos)
				self.plot.addItem(lbl)
				self.labelTexts[a].append(lbl)
			xshift+=self.xaxis.range[1]*.03

	def repositionLabels(self):
		xshift=self.xaxis.range[0]
		positions = np.linspace(-4,4,9)
		for a in range(4):
				V = self.currentRange[a]
				vpd=V/4
				num=0
				for ypos in positions:
					if self.channelButtons[a].isChecked():self.labelTexts[a][num].setVisible(True)
					else:self.labelTexts[a][num].setVisible(False)
					self.labelTexts[a][num].setPos(xshift, ypos)
					num+=1
				if self.channelButtons[a].isChecked():xshift+=self.xaxis.range[1]*.03


	def autoScale(self,plot,xMin,xMax,yMin,yMax):
			plot.setLimits(xMin=xMin,xMax=xMax,yMin=yMin,yMax=yMax);plot.setXRange(xMin,xMax);self.plot.setYRange(yMin,yMax)


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

	def waveSlider(self,f):
		self.WGBOX.setValue(f)

	def setWave(self,f):
		self.CH.set_wave(f)
		
	def setGainA1(self,val):
		v = self.rangevals12[val]
		self.currentRange[0] = v
		self.CH.select_range('A1',v)
		self.setLabels()
		
	def setGainA2(self,val):
		v = self.rangevals12[val]
		self.currentRange[1] = v
		self.CH.select_range('A2',v)
		self.setLabels()
	def setGainA3(self,val):
		v = self.rangevals34[val]
		self.currentRange[2] = v
		self.setLabels()
	def setGainMIC(self,val):
		v = self.rangevals34[val]
		self.currentRange[3] = v
		self.setLabels()

	def update(self):
		if self.tabWidget.currentIndex()!=0: #oscilloscope window inactive
			if self.tabWidget.currentIndex()==1:
				self.CH.get_states()
			#Add stuff for other tabs
			self.timer.singleShot(100,self.update)
			return
		elif self.pauseBox.isChecked(): #Paused scope
			self.timer.singleShot(100,self.update)
			return
		a = self.A1.isChecked()
		b = self.A2.isChecked()
		c = self.A3.isChecked()
		d = self.MIC.isChecked()
		if c or d:
			self.active_channels=4
			if not d: self.active_channels=3
		elif b:
			self.active_channels=2
		elif a:
			self.active_channels=1
		else:
			self.active_channels=0

		self.channels_in_buffer=self.active_channels
		self.samples = self.max_samples_per_channel[self.active_channels]
		self.channels_enabled=[a,b,c,d]
		
		if self.active_channels:
			self.CH.capture_traces(self.active_channels,self.samples,self.timebase,self.chan1remap,trigger = self.trigBox.isChecked(),chans = self.channels_enabled)
		else:
			self.timer.singleShot(10,self.update)

	##########################TIMING##########################
	def measure_interval(self):
		for a in range(4):
			i=self.timingResults.item(a,0);	i.setText('')
			i=self.timingResults.item(a,1);	i.setText('')
		i=self.timingResults.item(0,0);	i.setText('Timeout')

		t1,t2 = self.CH.I.MeasureMultipleDigitalEdges(self.edge1chan.currentText(),self.edge2chan.currentText(),self.edge1edge.currentText(),self.edge2edge.currentText(),self.edge1Count.currentIndex()+1,self.edge2Count.currentIndex()+1,self.timeoutBox.value()/1000.)
		pos=0
		if t1!=None:
			for a in t1:
				i=self.timingResults.item(pos,0);	i.setText(pg.siFormat(a, precision=3, suffix='S', space=True));		pos+=1
		pos=0
		if t2!=None:
			for a in t2:
				i=self.timingResults.item(pos,1);i.setText(pg.siFormat(a, precision=3, suffix='S', space=True));	pos+=1
			#self.sigExec.emit('set_wave',[self.WGBOX.value(),'sine'],{})
	def DoubleInputInterval(self):
		for a in range(4):
			i=self.TimingResults.item(a,0);	i.setText('')
			i=self.TimingResults.item(a,1);	i.setText('')
		i=self.TimingResults.item(0,0);	i.setText('Timeout')

		t1,t2 = self.CH.I.DoublePinEdges(self.Edge1chan.currentText(),self.Edge2chan.currentText(),self.Edge1edge.currentText(),self.Edge2edge.currentText(),self.Edge1Count.currentIndex()+1,self.Edge2Count.currentIndex()+1,self.TimeoutBox.value()/1000.)
		pos=0
		if t1!=None:
			for a in t1:
				i=self.TimingResults.item(pos,0);	i.setText(pg.siFormat(a, precision=3, suffix='S', space=True));		pos+=1
		pos=0
		if t2!=None:
			for a in t2:
				i=self.TimingResults.item(pos,1);i.setText(pg.siFormat(a, precision=3, suffix='S', space=True));	pos+=1
			#self.sigExec.emit('set_wave',[self.WGBOX.value(),'sine'],{})


	
	##########################controls##########################
	def setTimebase(self,tg):
		vals = [2,4,6,8,10,20,50,100,200,500]
		self.timebase = vals[tg]
		T = self.samples*self.timebase
		self.tgLabel.setText('%s'%pg.siFormat(T*1e-6, precision=3, suffix='S', space=True))

	def setSineAmp(self,val):
		if val in [0,1,2]: #sine wave
			self.sigExec.emit('set_wave',[self.WGBOX.value(),'sine'],{})
			self.sigExec.emit('set_sine_amp',[val],{})
		elif val in [3,4,5]: #triangular wave
			self.sigExec.emit('set_wave',[self.WGBOX.value(),'tria'],{})
			self.sigExec.emit('set_sine_amp',[val-3],{})
		else:
			pass

	def setCH1Remap(self,s):
		self.chan1remap = str(s)

	##############  HANDLE DATA RETURNED FROM WORKER THREAD   #####################
	def drawPlot(self,vals):
		'''
		Data sent from worker thread. Communication handler
		'''
		self.clearPlot()
		self.xmax = vals[0][:-1]
		self.plot.setLimits(xMin=0,xMax=vals[0][-1]);self.plot.setXRange(0,vals[0][-1])
		for A in range(len(vals)/2): #integer division
			if self.channels_enabled[A]:
				R = self.currentRange[A]
				x =vals[A*2]
				y = 4.*vals[A*2+1]/R
				self.curves[self.plot][A].setData(x,y)
		#t=time.time()
		self.repositionLabels()
		#print (time.time()-t)
		self.timer.singleShot(10,self.update)

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
		print ('packet drop')
		if 'fetch' in name: self.timer.singleShot(10,self.update)

	##############  HANDLE DATA RETURNED FROM WORKER THREAD   #####################


	def clearPlot(self):
		self.x = [];self.y=[];
		for a in self.curves[self.plot]:a.clear()

	def loadPlot(self,fname):
		self.showStatus("Loaded data from file | %s"%fname)
		self.fileBrowser.loadFromFile( self.plot,self.curves[self.plot],fname ) 
		self.tabWidget.setCurrentIndex(0)


	def save(self):
		from utilities import plotSaveWindow
		info = plotSaveWindow.AppWindow(self,self.curves[self.plot],self.plot)
		info.show()




if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = AppWindow()
	myapp.show()
	sys.exit(app.exec_())



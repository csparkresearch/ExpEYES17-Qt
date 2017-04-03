# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
import layout,os,string,time,glob
from collections import OrderedDict
import expeyes.eyes17 as eyes, expeyes.eyemath as eyemath, time, os, commands

import numpy as np
from PyQt4 import QtGui,QtCore
import pyqtgraph as pg
import pyqtgraph.exporters

import sys,time

class AppWindow(QtGui.QMainWindow, layout.Ui_MainWindow):
	signalStatus = QtCore.pyqtSignal()
	xmax = 20 #mS
	_browserPath = '.'
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

		self.p = eyes.open()
		if self.p.connected==False:
			self.showStatus("System Status | Device not found. Dummy mode.",True)
		else:
			self.showStatus("System Status | Connected to device. Version : SJ-1.0")#%s")%self.p.get_version())

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
		
		self.plot=pg.PlotWidget(enableMenu = False,axisItems={'left': stringaxis})
		self.plot.setMouseEnabled(False,True)
		self.plot.disableAutoRange(axis = self.plot.plotItem.vb.YAxis)
		self.plot_area.addWidget(self.plot)
		self.plot.getAxis('left').setGrid(170);
		self.plot.getAxis('bottom').setGrid(170); self.plot.getAxis('bottom').setLabel('mS')
		self.plot.setLimits(xMin=0,xMax=self.xmax,yMin=-4,yMax=4);self.plot.setXRange(0,self.xmax);self.plot.setYRange(-4,4)

		self.trace_colors=[(0,255,20),(255,0,0),(255,255,100),(10,255,255)]
		self.trace_names = ['A1','A2','A3','MIC']
		self.channelButtons = [self.A1,self.A2,self.A3,self.MIC]
		for a,col in zip(self.channelButtons,self.trace_colors):
			a.setStyleSheet("color:rgb%s"%str(col))
		
		self.plot.addLegend(offset=(-10,30))
		self.curves = []
		for name,col in zip(self.trace_names,self.trace_colors):
			C=pg.PlotCurveItem(name = name,pen = col)
			self.plot.addItem(C)
			self.curves.append(C)
		#X=np.linspace(0,20,1000)
		#self.curves[0].setData(X,3.1*np.sin(60*2*np.pi*.05*X+np.pi/10)*np.exp(-X/5))
		#self.curves[1].setData(X,3.1*np.sin(2*np.pi*.05*X+np.pi/2+np.pi/10))
		#self.curves[2].setData(X,[0]*1000)
		#self.curves[3].setData(X,[0]*1000)
		
		self.trig = pg.InfiniteLine(angle=0, movable=True)
		self.trig.setPos(0)
		self.plot.addItem(self.trig, ignoreBounds=False)
		self.currentPeak = None

		self.addLabels()
		self.thumbList={}
		self.thumbnailWorker = self.createThumbnailWorker()
		self.thumbnailWorker.generate()

		
		self.timer = QtCore.QTimer()
		self.timer.singleShot(10,self.update)

	def addLabels(self):
		self.labelTexts=[]
		self.vpd=[1,1,1,1]
		positions = np.linspace(-4,4,9)
		for ypos in positions:
			txt = ''
			for a in range(4):
				if self.channelButtons[a].isChecked():
					txt+='''<span style="color: rgb%s; font-size: 7pt;">%.2f </span>'''%(self.trace_colors[a],ypos*self.vpd[a])
			lbl = pg.TextItem(html=txt, anchor=(0,1));lbl.setPos(0, ypos)
			self.plot.addItem(lbl)
			self.labelTexts.append(lbl)
		

	'''
	def closeEvent(self, evnt):
		evnt.ignore()
		self.askBeforeQuit()
	'''
	
	def askBeforeQuit(self):
		reply = QtGui.QMessageBox.question(self, 'Warning', 'Really quit?', QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
		if reply == QtGui.QMessageBox.Yes:
			global app
			app.quit()

	def clearPlot(self):
		self.x = [];self.y=[];
		for a in self.curves:a.clear()

	def showStatus(self,msg,error=None):
		if error: self.statusBar.setStyleSheet("color:#FF0000")
		else: self.statusBar.setStyleSheet("color:#000000")
		self.statusBar.showMessage(msg)

	def update(self):
		try:
			pass
		except:
			self.showStatus("System Status | Read Error",True)
		#self.trig.setBounds([-4,4])
		#self.curve.setData(self.x,self.y[:-1], stepMode=True, fillLevel=0, brush=(26, 197, 220,100))

	def save(self):
		import plotSaveWindow
		info = plotSaveWindow.AppWindow(self,self.curves,self.plot)
		info.show()

	def loadPlot(self,sel):
		fname = self.thumbList[str(sel.text())][1]
		print fname

	def changeDirectory(self):
		dirname = QtGui.QFileDialog.getExistingDirectory(self,"Load a folder containing Experiments", os.path.expanduser("./"),  QtGui.QFileDialog.ShowDirsOnly)
		if not dirname:return
		self._browserPath=str(dirname)
		self.browserPath.setText(self._browserPath)
		self.thumbnailWorker.setDir(self._browserPath)

		for a in self.thumbList:
			print 'removing',self.thumbList[a][0]
			self.thumbs.takeItem(self.thumbs.row(self.thumbList[a][0]))
		self.thumbList={}

		self.signalStatus.emit()
		
	def createThumbnailWorker(self):
		worker = WorkerObject(directory=self._browserPath)
		self.worker_thread = QtCore.QThread()
		worker.moveToThread(self.worker_thread)
		worker.signalStatus.connect(self.updateStatus)
		worker.loadIcon.connect(self.loadIcon)
		self.signalStatus.connect(worker.generate)
		self.worker_thread.start()
		return worker

	def updateStatus(self,txt):
		self.browserPath.setText(txt)

	def loadIcon(self,thumbpath,filepath,filename):
		print 'loading icon'
		if not os.path.exists(thumbpath):return
		x = QtGui.QIcon(thumbpath)
		a = QtGui.QListWidgetItem(x,filename)
		self.thumbs.addItem(a)
		self.thumbList[filename] = [a,filepath]

class WorkerObject(QtCore.QObject):
	signalStatus = QtCore.pyqtSignal(str)
	loadIcon = QtCore.pyqtSignal(str,str,str)

	def __init__(self, parent=None,**kwargs):
		super(self.__class__, self).__init__(parent)
		self.directory = kwargs.get('directory','.')

		self.P2=pg.PlotWidget(enableMenu = False)
		self.curves = []
		self.trace_colors=[(0,255,20),(255,0,0),(255,255,100),(10,255,255)]
		for col in self.trace_colors:
			C=pg.PlotCurveItem();C.setPen(color=col, width=3)
			self.P2.addItem(C)
			self.curves.append(C)

	def setDir(self,directory):
		self.directory = directory

	def loadFromFile(self,plot,curves,filename):
		print 'load',filename
		try:
			try:                                                        #Load text file with columns
				ar = np.loadtxt(filename)
			except:                                                     #If that fails , assume first row contains headers
				with open(filename) as f:
					header = f.readline()
					try:                                                #parse headers and set them as axis labels
						header = header.replace(' ',',')
						p=header.split(',')
						plot.getAxis('bottom').setLabel(p[0])
						plot.getAxis('left').setLabel(p[1])
					except:
						pass
				ar = np.loadtxt(filename,skiprows=1)                    #skip the header row and start loading

			for A in range(len(ar[0])/2): #integer division
				self.x =ar[:,A*2]
				self.y =ar[:,A*2+1]
				curves[A].setData(self.x,self.y)
		except Exception as e:
			print (e)

	@QtCore.pyqtSlot()
	def generate(self):
		self.textfiles = []
		homedir = os.path.expanduser('~')
		thumbdir = os.path.join(homedir,'.seelab/thumbs')
		thumbFormat = 'png'
		self.exporter = pg.exporters.ImageExporter(self.P2.plotItem)


		for a in os.listdir(self.directory):
			pcs = a.split('.')
			if pcs[-1] in ['dat','csv']:  #check if extension is acceptable 
				print pcs
				fname = string.join(pcs[:-1],'.')
				timestamp = int(os.path.getctime(a))
				thumbpath = os.path.join(thumbdir,fname+str(timestamp)+'.'+thumbFormat)
				filepath = os.path.join(self.directory,a)
				if not os.path.exists(thumbpath):  #need to create fresh thumbnail
					self.signalStatus.emit('Generating thumbnail for %s'%(filepath))
					map(os.remove, glob.glob(os.path.join(thumbdir,fname)+'*.'+thumbFormat)) #remove old thumbnails (different timestamp) if any
					#self.loadFromFile(self.P2,self.curves,filepath) 
					#self.exporter.export(thumbpath)
				time.sleep(1)
				self.signalStatus.emit('Loading thumbnail for %s'%(filepath))
				self.loadIcon.emit(thumbpath,filepath,fname)
		self.signalStatus.emit('Current path : %s'%self.directory)


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = AppWindow()
	myapp.show()
	sys.exit(app.exec_())



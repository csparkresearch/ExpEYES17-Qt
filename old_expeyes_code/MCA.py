import layout,os,string,time,glob
import ejmca

import numpy as np
from PyQt4 import QtGui,QtCore
import pyqtgraph as pg
import pyqtgraph.exporters

import sys,time

class AppWindow(QtGui.QMainWindow, layout.Ui_MainWindow):
	total_bins = 512
	def __init__(self, parent=None,**kwargs):
		super(AppWindow, self).__init__(parent)
		self.setupUi(self)
		self.statusBar = self.statusBar()

		self.p = ejmca.open()
		if self.p.dummy:
			self.showStatus("System Status | Device not found. Dummy mode.",True)
		else:
			self.showStatus("System Status | Connected to device. Version : %s"%self.p.version)


		self.exitBtn = QtGui.QPushButton("EXIT")
		self.exitBtn.clicked.connect(self.askBeforeQuit)
		self.exitBtn.setStyleSheet("height: 10px;padding:3px;color: #FF2222;")
		self.statusBar.addPermanentWidget(self.exitBtn)
		self.saveSignal = QtGui.QShortcut(QtGui.QKeySequence(QtCore.QCoreApplication.translate("MainWindow", "Ctrl+S", None)), self)
		self.saveSignal.activated.connect(self.save)

		self.plot=pg.PlotWidget()
		self.plot.setMinimumHeight(250)
		self.plot_area.addWidget(self.plot)
		self.plot.getAxis('left').setGrid(170)
		self.plot.getAxis('bottom').setGrid(170); 		self.plot.getAxis('bottom').setLabel('bins')
		self.plot.setLimits(xMin=0,xMax=self.total_bins,yMin=0,yMax=65535);self.plot.setXRange(0,self.total_bins)

		self.region = pg.LinearRegionItem()
		self.region.setZValue(10)
		self.plot.addItem(self.region, ignoreBounds=False)

		self.curve = pg.PlotCurveItem(name = 'Data')
		self.fitcurve = pg.PlotCurveItem(name = 'Fit',pen = [255,0,0])
		self.plot.addItem(self.curve);self.plot.addItem(self.fitcurve);
		self.plot.scene().sigMouseClicked.connect(self.onClick)

		self.thres = pg.InfiniteLine(angle=0, movable=True)
		self.thres.setPos(1000)
		self.peakGap = 20
		
		self.plot.addItem(self.thres, ignoreBounds=True)
		self.peakMarks={}
		self.currentPeak = None
		
		self.x=[];self.y=[];self.xscale = 1.
		self.saved={}
		self.generateThumbnails()
		
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.load)

	def closeEvent(self, evnt):
		evnt.ignore()
		self.askBeforeQuit()

	def askBeforeQuit(self):
		reply = QtGui.QMessageBox.question(self, 'Warning', 'Really quit?', QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
		if reply == QtGui.QMessageBox.Yes:
			global app
			app.quit()

	def start(self):
		self.showStatus("System Status | Acquisition Started")
		self.p.start_hist()
	def pause(self):
		self.showStatus("System Status | Acquisition Stopped")
		self.p.stop_hist()

	def clear(self):
		self.showStatus("System Status | Data cleared")
		self.p.clear_hist()
		self.clearPlot()

	def clearPeaks(self):
		for a in self.peakMarks:
			self.plot.removeItem(a)
		self.peakMarks={}
		self.currentPeak = None
		
	def clearPlot(self):
		self.clearPeaks();self.region.setRegion([0,0]);
		self.x = [];self.y=[];
		self.curve.clear();self.fitcurve.clear()

	def setAutoUpdate(self,state):
		if state:
			for a in [self.updateButton,self.locateButton,self.fitButton]:a.setEnabled(False)
			self.timer.start(500) #every 500mS
		else:
			for a in [self.updateButton,self.locateButton,self.fitButton]:a.setEnabled(True)
			self.timer.stop()

	def showStatus(self,msg,error=None):
		if error: self.statusBar.setStyleSheet("color:#FF0000")
		else: self.statusBar.setStyleSheet("color:#000000")
		self.statusBar.showMessage(msg)

	def load(self):
		self.clearPeaks()
		try:
			self.x,self.y = self.p.read_hist()	
		except:
			self.showStatus("System Status | Read Error",True)
		self.thres.setBounds([50,max(self.y)+100])
		self.fitcurve.clear()
		self.curve.setData(self.x,self.y[:-1], stepMode=True, fillLevel=0, brush=(26, 197, 220,100))

	def fit(self):
		start,end=self.region.getRegion()
		if(start>0):start = int(round(start*self.xscale))
		else: start=0
		if(end>0):end = int(round(end*self.xscale))
		else:end=0
		self.fitcurve.clear()
		try:
			import eyemath
			X = np.array(self.x[start:end])*self.xscale
			nf, par = eyemath.fit_gauss(X,self.y[start:end])
			self.fitcurve.setData(X,nf[:-1], stepMode=True, fillLevel=0, brush=(126, 197, 220,100))
			msg = 'Amplitude= %5.1f  E= %5.2f  sigma = %5.2f'%(par[0], par[1], par[2])
			QtGui.QMessageBox.critical(self, 'Fit Results', msg)
			self.showStatus("Fit result : "+msg,True)
		except Exception as e:
			QtGui.QMessageBox.critical(self, 'Fit Failed', e.message)

	def calibrate(self):
		print self.region.getBounds()
		if not self.currentPeak:
			QtGui.QMessageBox.critical(self, 'Peak not selected', 'Please locate peaks first.<br>Then click on the relevant peak to select it')
			return

		en = float(self.knownPeak.value())
		self.xscale = en/self.currentPeak
		print self.xscale
		self.plot.getAxis('bottom').setLabel('Energy (MeV)')
		self.clearPeaks()
		self.plot.setLimits(xMax=max(self.x)*self.xscale);self.plot.setXRange(0,max(self.x)*self.xscale)
		self.curve.setData(np.array(self.x)*self.xscale,self.y[:-1], stepMode=True, fillLevel=0, brush=(0,0,255,150))

	def peakGapChanged(self,val):
		self.peakGap = val
		self.peakDetectSpacingLabel.setText(str(val))

	def locate(self):
		if len(self.y)<10:
			self.showStatus("Peak Detection | please click on upload / load data from file",True)
			return
		import peak
		self.clearPeaks()
		indices = peak.indexes(self.y, thres=self.thres.value()/max(self.y), min_dist=self.peakGap)
		for a in indices:
			arr = pg.ArrowItem(angle=-160,tipAngle = 90, headLen=7, tailLen=9, tailWidth=5, pen={'color': 'r', 'width': 1}) 
			self.plot.addItem(arr)
			arr.setPos(a*self.xscale,self.y[a])
			self.peakMarks[arr] = a
		self.showStatus("Peak Detection | %d Peak(s) Found"%len(indices))

	def onClick(self,event):
		items = self.plot.scene().items(event.scenePos())
		for x in self.peakMarks:
			x.setStyle(pen={'color': 'r', 'width': 2})
		for x in items:
			if isinstance(x, pg.ArrowItem):
				x.setStyle(pen={'color': 'g', 'width': 1})
				val = self.peakMarks[x]
				self.showStatus("Peak Clicked | bin #%d , value %d"%(val,self.y[val]))
				self.currentPeak = val
				self.region.setRegion([(val-20)*self.xscale,(val+20)*self.xscale])

	def save(self):
		if not len(self.x):
			QtGui.QMessageBox.critical(self, 'Acquire Data', 'Please acquire some data first!')
			return
		import plotSaveWindow
		info = plotSaveWindow.AppWindow(self,[self.curve,self.fitcurve],self.plot)
		info.show()

	def loadPlot(self,sel):
		self.clearPlot()
		fname = self.saved[str(sel.text())]
		self.showStatus("Loaded data from file | %s"%fname)
		self.loadFromFile( fname )
		self.tabWidget.setCurrentIndex(0)

	def loadFromFile(self,filename):
			try:
				ar = np.loadtxt(filename)
				self.x =ar[:,0]
				self.y =ar[:,1]
				self.thres.setBounds([50,max(self.y)])
			except Exception as e:
				print (e)
			self.fitcurve.clear()
			self.curve.setData(self.x,self.y[:-1], stepMode=True, fillLevel=0, brush=(26, 197, 220,100))
			self.plot.getAxis('bottom').setLabel('')

	def generateThumbnails(self):
		self.textfiles = []
		thumbfiles = [a for a in os.listdir('./.thumbs') if a.split('.')[-1] == 'svg']
		thumbfiles.sort()

		for a in os.listdir('.'):
			pcs = a.split('.')
			if pcs[-1] == 'dat':
				self.saved[pcs[0]] = a
				timestamp = int(os.path.getctime(a))
				if string.join(pcs[:-1]+[str(timestamp),'svg'],'.') in thumbfiles:
					continue
				map(os.remove, glob.glob('./.thumbs/'+pcs[0]+'*.svg')) #remove old thumbnails
				self.textfiles.append((a,timestamp))
		self.textfiles.sort()

		self.exporter = pg.exporters.SVGExporter(self.plot.plotItem)
		for f,tm in self.textfiles:
			self.loadFromFile(f)
			self.exporter.export('.thumbs/'+f[:-4]+'.'+str(tm)+'.svg')

		thumbfiles = [a for a in os.listdir('./.thumbs') if a.split('.')[-1] == 'svg']
		thumbfiles.sort()
		for f in thumbfiles:
			x = QtGui.QIcon('./.thumbs/'+f)
			a = QtGui.QListWidgetItem(x,f.split('.')[0])
			self.thumbs.addItem(a)

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = AppWindow()
	myapp.show()
	sys.exit(app.exec_())



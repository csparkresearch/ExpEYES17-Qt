# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
import os,glob
try:
	from PyQt5 import QtGui,QtCore
except:
	from PyQt4 import QtGui,QtCore
import numpy as np

from .templates import ui_fileBrowser as fileBrowser
import pyqtgraph as pg

class dummyApp:
	def processEvents(self):
		pass


class fileBrowser(QtGui.QFrame,fileBrowser.Ui_Form):
	trace_names = ['#%d'%a for a in range(10)]
	trace_colors = [(0,255,0),(255,0,0),(255,255,100),(10,255,255)]
	textfiles=[]
	_browserPath = '.'
	def __init__(self,*args,**kwargs):
		super(fileBrowser, self).__init__()
		self.setupUi(self)
		self.thumbList = {}

		self.thumbnailSubdir = kwargs.get('thumbnail_directory','thumbnails')
		self.clickCallback = kwargs.get('clickCallback',self.showNewPlot)
		self.app = kwargs.get('app',dummyApp())

	def refresh(self):
		self.generateThumbnails(self._browserPath)
		
	def itemClicked(self,sel):
		fname = self.thumbList[str(sel)][1]
		print(fname)
		self.clickCallback( fname )


	def changeDirectory(self):
		dirname = QtGui.QFileDialog.getExistingDirectory(self,"Load a folder containing Experiments", os.path.expanduser("./"),  QtGui.QFileDialog.ShowDirsOnly)
		if not dirname:return
		self._browserPath=str(dirname)
		self.pathLabel.setText(self._browserPath)
		self.generateThumbnails(self._browserPath)


	def clearThumbnails(self):
		for a in self.thumbList:
			self.listWidget.takeItem(self.listWidget.row(self.thumbList[a][0]))
		self.thumbList={}
		
	def generateThumbnails(self,directory='.',**kwargs):
		self.clearThumbnails()
		
		if directory=='.':directory = os.path.expanduser('~')
		self.app.processEvents()
		P2=pg.PlotWidget(enableMenu = False)
		curves = []
		for name,col in zip(self.trace_names,self.trace_colors):
			C=pg.PlotCurveItem(name = name);C.setPen(color=col, width=3)
			P2.addItem(C)
			curves.append(C)

		self.textfiles = []
		homedir = os.path.expanduser('~')
		thumbdir = os.path.join(homedir,self.thumbnailSubdir)
		if not os.path.isdir(thumbdir):
			print ('Directory missing. Will create')
			os.makedirs(thumbdir)
		thumbFormat = 'png'

		self.exporter = pg.exporters.ImageExporter(P2.plotItem)


		for a in os.listdir(directory):
			pcs = a.split('.')
			if pcs[-1] in ['dat','csv','txt']:  #check if extension is acceptable 
				fname = str.join('.',pcs[:-1])
				filepath = os.path.join(directory,a)
				timestamp = int(os.path.getctime(filepath))
				thumbpath = os.path.join(thumbdir,fname+str(timestamp)+'.'+thumbFormat)

				if not os.path.exists(thumbpath):  #need to create fresh thumbnail
					try:
						self.pathLabel.setText('Generating thumbnail for %s'%(filepath));self.app.processEvents()
						map(os.remove, glob.glob(os.path.join(thumbdir,fname)+'*.'+thumbFormat)) #remove old thumbnails (different timestamp) if any
						self.loadFromFile(P2,curves,filepath) 
						self.exporter.export(thumbpath)
					except Exception as e:
						print ('problem',e.message)
						continue
				try:
					self.pathLabel.setText('Loading thumbnail for %s'%(filepath));self.app.processEvents()
					print ('hm : Loading thumbnail for %s'%(filepath))
					x = QtGui.QIcon(thumbpath)
					a = QtGui.QListWidgetItem(x,fname)
					self.listWidget.addItem(a)
					self.thumbList[fname] = [a,filepath]
				except Exception as e:
					print( 'failed to load thumbnail for ',fname,e.message)
		self.pathLabel.setText('Current path : %s'%directory)
		

	def loadFromFile(self,plot,curves,filename,histMode=False):
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
						plot.getAxis('bottom').setLabel('time')
						plot.getAxis('left').setLabel('Voltage')
				ar = np.loadtxt(filename,skiprows=1)                    #skip the header row and start loading

			XR = [0,0];YR=[0,0]
			for A in range(len(ar[0])//2): #integer division
				self.x =ar[:,A*2]
				self.y =ar[:,A*2+1]
				if histMode:curves[A].setData(self.x,self.y[:-1], stepMode=True, fillLevel=0, brush=(126, 197, 220,100))
				else:curves[A].setData(self.x,self.y)
				if( min(self.x) < XR[0] ):XR[0] = min(self.x)-abs(min(self.x))*.1
				if( max(self.x) > XR[1] ):XR[1] = max(self.x)+abs(max(self.x))*.1
				if( min(self.y) < YR[0] ):YR[0] = min(self.y)-abs(min(self.y))*.1
				if( max(self.y) > YR[1] ):YR[1] = max(self.y)+abs(max(self.y))*.1
			self.autoScale(plot,XR[0],XR[1],YR[0],YR[1]);

	def autoScale(self,plot,xMin,xMax,yMin,yMax):
			plot.setLimits(xMin=xMin,xMax=xMax,yMin=yMin,yMax=yMax);plot.setXRange(xMin,xMax);plot.setYRange(yMin,yMax)

	def showNewPlot(self,fname):
		self.newwin = pg.GraphicsWindow(title="Data from file | %s"%fname)
		self.newwin.resize(800,600)
		#self.newwin.setWindowTitle('pyqtgraph example: Plotting')
		self.p1 = self.newwin.addPlot()
		self.newcurves=[]
		for name,col in zip(self.trace_names,self.trace_colors):
			C=pg.PlotCurveItem(name = name,pen = col)
			self.p1.addItem(C)
			self.newcurves.append(C)

		self.loadFromFile( self.p1,self.newcurves,fname ) 


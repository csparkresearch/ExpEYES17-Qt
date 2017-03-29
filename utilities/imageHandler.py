import os,string
from PyQt4 import QtGui,QtCore
from templates import ui_fileBrowser as fileBrowser
import pyqtgraph as pg

class dummyApp:
	def processEvents(self):
		pass


class imageHandler(QtGui.QFrame,fileBrowser.Ui_Form):
	trace_names = ['#%d'%a for a in range(10)]
	trace_colors = [(0,255,0),(255,0,0),(255,255,100),(10,255,255)]
	textfiles=[]
	_browserPath = '.'
	def __init__(self,*args,**kwargs):
		super(imageHandler, self).__init__()
		self.setupUi(self)
		self.thumbList = {}

		self.thumbnailSubdir = kwargs.get('thumbnail_directory','thumbnails')
		self.clickCallback = kwargs.get('clickCallback',None)
		self.app = kwargs.get('app',dummyApp())
		self.generateThumbnails()

	def itemClicked(self,sel):
		fname = self.thumbList[str(sel.text())][1]
		print fname
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
		
		if directory=='.':directory = os.path.expanduser(os.path.join('~','Documents'))
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
				fname = string.join(pcs[:-1],'.')
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
						print (e.message)
						continue
				try:
					self.pathLabel.setText('Loading thumbnail for %s'%(filepath));self.app.processEvents()
					x = QtGui.QIcon(thumbpath)
					a = QtGui.QListWidgetItem(x,fname)
					self.listWidget.addItem(a)
					self.thumbList[fname] = [a,filepath]
				except Exception as e:
					print 'failed to load thumbnail for ',fname,e.message
		self.pathLabel.setText('Current path : %s'%directory)
		

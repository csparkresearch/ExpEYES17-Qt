# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
import os,glob
from ..Qt import QtGui, QtCore,QtWidgets

import numpy as np

from .templates import ui_onlineBrowser as onlineBrowser
import pyqtgraph as pg

class dummyApp:
	def processEvents(self):
		pass

try:
	import requests
except:
	print ('requests library missing. online browser will not work.')

class onlineBrowser(QtWidgets.QFrame,onlineBrowser.Ui_Form):
	trace_names = ['#%d'%a for a in range(10)]
	trace_colors = [(0,255,0),(255,0,0),(255,255,100),(10,255,255)]
	textfiles=[]
	def __init__(self,*args,**kwargs):
		super(onlineBrowser, self).__init__()
		self.setupUi(self)
		self.thumbList = {}

		self.downloadedSubdir = kwargs.get('save_directory','ExpEYES_Online')
		self.clickCallback = kwargs.get('clickCallback',self.showClickedFile)
		self.app = kwargs.get('app',dummyApp())

	def refresh(self):
		self.generateItemList()
		
	def itemClicked(self,sel):
		fname = self.thumbList[str(sel)][1]
		print(fname)
		self.clickCallback( fname )

	def clearItems(self):
		for a in self.thumbList:
			self.listWidget.takeItem(self.listWidget.row(self.thumbList[a][0]))
		self.thumbList={}
		
	def generateItemList(self,**kwargs):
		self.clearItems()
		
		url = self.urlEdit.text()
		dlPath = url+'getStaticScripts'
		print ('downloading from ',dlPath)
		self.app.processEvents()
	

		self.textfiles = []
		homedir = os.path.expanduser('~')
		thumbdir = os.path.join(homedir,self.downloadedSubdir)
		if not os.path.isdir(thumbdir):
			print ('Directory missing. Will create')
			os.makedirs(thumbdir)


		requests.get(dlPath,hooks=dict(response=self.processData))

	def processData(self,expts,*args,**kwargs):
		if expts.status_code == 200:
			dirList = expts.json()['staticdata']
			for a in dirList:
				print ('directory :',a)
				scriptList = dirList[a]['data']
				for b in scriptList:
					try:
						#x = QtGui.QIcon(thumbpath)
						fname = b['Filename']
						filepath = dirList[a]['path']
						item = QtGui.QListWidgetItem(fname)#x,fname)
						self.listWidget.addItem(item)
						self.thumbList[fname] = [item,filepath]
					except Exception as e:
						print( 'failed to load ',b,e)


		else:
		  print ('got nothing. error:',expts.status_code)

	def loadFromFile(self,plot,curves,filename,histMode=False):
		print('what just happened?')
	def showClickedFile(self):
		print('what just happened?click.')
		

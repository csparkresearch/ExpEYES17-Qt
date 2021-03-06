# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
import os,string,glob

from ..Qt import QtGui,QtCore,QtWidgets,QWebView


import sys,pkg_resources

class helpBrowser(QWebView):
	def __init__(self,*args,**kwargs):
		super(helpBrowser, self).__init__()
		self.help_path = '.'
		sys.path.append(self.help_path)
		self.showMaximized()
				
	def setFile(self,url=None):
		if url is None:
			os.path.join(os.path.dirname(sys.argv[0]),'help','MD_HTML','index.html')
			url = './help/MD_HTML/index.html'
		newUrl = QtCore.QUrl.fromLocalFile(QtCore.QFileInfo(url).absoluteFilePath())
		print ('SETTING URL',url,newUrl)
		self.setUrl(newUrl)#pkg_resources.resource_filename('eyes_html',url)))
		

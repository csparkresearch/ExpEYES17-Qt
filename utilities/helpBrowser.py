# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
import os,string,glob
try:
	from PyQt5 import QtWebKit,QtCore
	from PyQt5.QtWebKitWidgets import QWebView , QWebPage
except:
	print ('trying yo use qt4 fallback')
	from PyQt4 import QtCore
	from pyqt4.QtWebKit import QWebView

import sys,pkg_resources

class helpBrowser(QWebView):
	def __init__(self,*args,**kwargs):
		super(helpBrowser, self).__init__()
		self.help_path = '.'
		sys.path.append(self.help_path)
		self.showMaximized()
		self.setUrl(QtCore.QUrl("https://www.google.com"))
				
	def setFile(self,url='./help/MD_HTML/index.html'):
		print ('SETTING URL',url)
		self.setUrl(QtCore.QUrl(url))#pkg_resources.resource_filename('eyes_html',url)))
		

# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
import os,string,glob
try:
	from PyQt4 import QtWebKit,QtCore
except:
	from PyQt5 import QtWebKit,QtCore
import sys,pkg_resources

class helpBrowser(QtWebKit.QWebView):
	def __init__(self,*args,**kwargs):
		super(helpBrowser, self).__init__()
		self.help_path = '.'
		sys.path.append(self.help_path)

	def setFile(self,url='./help/MD_HTML/index.html'):
		self.setUrl(QtCore.QUrl(url))#pkg_resources.resource_filename('eyes_html',url)))
		

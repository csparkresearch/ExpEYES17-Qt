import os
print ('using %s'%os.environ['SPARK17_QT_LIB'])
if os.environ['SPARK17_QT_LIB'] == 'PyQt5':
	from PyQt5 import QtGui,QtCore,QtWidgets
	from PyQt5.QtWebKitWidgets import QWebView# , QWebPage
if os.environ['SPARK17_QT_LIB'] == 'PyQt4':
	from PyQt4 import QtGui,QtCore
	from PyQt4 import QtGui as QtWidgets
	from PyQt4.QtWebKit import QWebView
if os.environ['SPARK17_QT_LIB'] == 'PySide':
	from PySide import QtGui,QtCore
	from PySide import QtGui as QtWidgets
	from PySide.QtWebKit import QWebView
	QtCore.pyqtSignal = QtCore.Signal
	QtCore.pyqtSlot = QtCore.Slot

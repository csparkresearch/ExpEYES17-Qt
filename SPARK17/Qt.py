import os
if os.environ['SPARK17_QT_LIB'] == 'PyQt5':
	from PyQt5 import QtGui,QtCore,QtWidgets
else:
	print ('using PyQt4')
	from PyQt4 import QtGui,QtCore
	from PyQt4 import QtGui as QtWidgets


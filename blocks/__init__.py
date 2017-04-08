# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from __future__ import print_function
import os,string,time
from collections import OrderedDict
import time, os
from CommunicationHandlerQt import communicationHandler
import numpy as np
from PyQt4 import QtGui,QtCore
import pyqtgraph as pg
import pyqtgraph.exporters

#from templates import ui_layout as layout
from utilities.fileBrowser import fileBrowser
from utilities.expeyesWidgets import expeyesWidgets
from expeyes import eyemath17 as eyemath


import gettext, sys,time
gettext.bindtextdomain("expeyes")
gettext.textdomain('expeyes')
_ = gettext.gettext

#class AppWindow(QtGui.QMainWindow, layout.Ui_MainWindow,expeyesWidgets):

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = AppWindow()
	myapp.show()
	sys.exit(app.exec_())

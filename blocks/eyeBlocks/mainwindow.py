#!/usr/bin/python
# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-

from __future__ import print_function

license="""\
  Copyright (C) 2017 Georges Khaznadar <georgesk@debian.org>

  Application Expeyes-Blocks

  This application may be used under the terms of the
  GNU General Public License version 3.0 as published by
  the Free Software Foundation, or, at your preference,
   any later verion of the same.

  Expeyes-Blocks is built upon Qt4 GUI libraries, see "About Qt".

  This application is provided AS IS with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND
  FITNESS FOR A PARTICULAR PURPOSE.
"""

from version import version

import copy, re
from os.path import basename

from PyQt4.QtCore import QPoint, QRect, Qt, QSize, QString, \
	QTimer, QFileInfo, SIGNAL, QByteArray, QStringList

from PyQt4.QtGui import QMainWindow, QApplication, \
	QMessageBox, QFileDialog, QTextCursor

def _translate(context, text, disambig):
	return QApplication.translate(context, unicode(text), disambig)
        

from templates.ui_blocks import Ui_MainWindow
from component import Component, InputComponent
from timecomponent import TimeComponent
from modifcomponent import ModifComponent
from channelcomponent import ChannelComponent
import wizard



class BlockMainWindow(QMainWindow, Ui_MainWindow):
	"""
	This class implements the main window of the Expeyes-Blocks
	application.
	"""
	def __init__(self, parent=None):
		QMainWindow.__init__(self, parent)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.splitter.setSizes([4,1])
		self.loadComponents()
		self.connectSignals()
		self.fileName=None
		self.dirty="" # may become "*"
		self.widget.boxModel="expeyes-junior"
		self.warn(_translate("eyeBlocks.mainwindow","<span style='color:blue'>[Current targetted box]</span> %1",None).arg(self.widget.boxModel))
		return

	def loadComponents(self, path=None):
		self.widget.clear()
		cList=Component.listFromRC()
		for c in cList:
			self.componentsList.newComponent(c)
		return

	def connectSignals(self):
		"""
		connecting signals to methods
		"""
		self.action_Quit.triggered.connect(self.close)
		self.actionSave.triggered.connect(self.save)
		self.actionSave_as.triggered.connect(self.saveAs)
		self.action_Open.triggered.connect(self.load)
		self.action_About.triggered.connect(self.about)
		self.actionAbout_Qt.triggered.connect(self.aboutQt)
		self.widget.blocksChanged.connect(self.makeDirty)
		self.action_Compile.triggered.connect(self.compile_)
		self.action_Run.triggered.connect(self.run)
		self.actionExpeyes_17.triggered.connect(self.chooseBox("expeyes-17"))
		self.actionExpeyes_Junior.triggered.connect(self.chooseBox("expeyes-junior"))
		
	def compile_(self):
		"""
		Compile the current scheme to a working application.

		:returns: the path to the main python program.
		"""
		import os, os.path
		# save the file if necessary
		if self.dirty=="*": self.save()
		fileNameShorted=os.path.basename(str(self.fileName)).replace(".eyeblk","")
		directory=os.path.join("build", fileNameShorted)
		try:
			os.makedirs(directory, mode=0o755)
		except:
			pass
		l=os.listdir(directory)
		l=QStringList(l)
		ok=True
		if l:
			ok=QMessageBox.question(self,
				_translate("eyeBlocks.mainwindow","OK to erase a previous build?",None),
				_translate("eyeBlocks.mainwindow","Here are some previous built files:\n %1\nDo you really want to overwrite them?",None).arg(
					l.join(", ")),
				QMessageBox.No|QMessageBox.Yes
			) == QMessageBox.Yes
		if not ok: return
		return wizard.compile_(self, directory)
		
	def run(self):
		"""
		Compile the current scheme to a working application,
		and run it in a detached thread
		"""
		program=self.compile_()
		wizard.run(program)
		return
		
	def chooseBox(self, model):
		"""
		choose the targetted box

		:param model: the target model
		:type model:
		"""
		def callBack():
			self.boxModel=model
			self.warn(_translate("eyeBlocks.mainwindow","<span style='color:blue'>[New targetted box]</span> %1",None).arg(model))
			return
		return callBack
				
	def about(self):
		"""
		brings up the About dialog
		"""
		QMessageBox.about(self,_translate("eyeBlocks.mainwindow","About",None), license)
		return
		
	def aboutQt(self):
		"""
		brings up the About dialog
		"""
		QMessageBox.aboutQt(self,_translate("eyeBlocks.mainwindow","About Qt",None))
		return
		
	versionPattern=re.compile(r"^Expeyes-Blocks version ([\.\d]+)$")
	classPattern  =re.compile(r"^Class Name \((\d+) bytes\)$")
	blobPattern   =re.compile(r"^Blob \((\d+) bytes\)$")
		
	def load(self):
		"""
		Loads a component composition
		"""
		fileName=QFileDialog.getOpenFileName(self,
			_translate("eyeBlocks.mainwindow","Open a file",None),
			filter=_translate("eyeBlocks.mainwindow","Expeyes-Blocks:  *.eyeblk (*.eyeblk);;All files: * (*)",None)
		)
		self.loadFile(fileName)
		return
		
	def loadFile(self, fileName):
		"""
		Loads a component composition

		:param fileName: a file of saved data
		:type fileName:
		"""
		ok=False
		cur=0
		with open(fileName,"rb") as instream:
			s=instream.readline()
			thisVersion=self.versionPattern.match(s).group(1)
			# take a decision about thisVersion
			components=[]
			nameSize = instream.readline()
			while nameSize:
				size=int(self.classPattern.match(nameSize).group(1))
				className=instream.readline().strip()
				if len(className) != size:
					raise Exception(_translate("eyeBlocks.mainwindow","Error size: %s does not match %s",None) %(size, className))
				s=instream.readline()
				blobSize=int(self.blobPattern.match(s).group(1))
				blob=QByteArray(instream.read(blobSize))
				obj, dataStream, className = eval("%s.unserialize(blob)" %className)
				components.append(obj)
				# prepare next iteration
				nameSize = instream.readline()
			if components:
				ok=True
				# restore components in the right pannel
				self.widget.components=components
				self.widget.connectSnaps()
				self.widget.update()
				# restore list items in the left pannel
				for c in components:
					self.componentsList.hideItem(c)
		if ok: 
			self.fileName=fileName
			self.dirty=""
			self.setWindowTitle(self.currentTitle())
			self.warn(_translate("eyeBlocks.mainwindow","<span style='color:blue'>[Loaded file]</span> %1",None).arg(fileName))
		return
		
	def save(self):
		"""
		Saves the current component composition
		"""
		if self.fileName:
			with open(self.fileName,"wb") as outstream:
				outstream.write("Expeyes-Blocks version %s\n" %version)
				for c in self.widget.components:
					c.save(outstream)
			self.dirty=""
			self.setWindowTitle(self.currentTitle())
			self.warn(_translate("eyeBlocks.mainwindow","<span style='color:blue'>[Saved file]</span> %1",None).arg(self.fileName))
		else:
			self.saveAs()
		return
		
	def saveAs(self, fileName=None):
		"""
		Saves the current component composition in a new file

		:param fileName: name of the file, defaults to None
		:type fileName:
		"""
		if fileName: self.fileName=fileName
		if not self.fileName:
			self.fileName = _translate("eyeBlocks.mainwindow","untitled.eyeblk",None)
		self.fileName=QFileDialog.getSaveFileName(
			self, _translate("eyeBlocks.mainwindow","Save to file",None), self.fileName,
			filter = _translate("eyeBlocks.mainwindow","Expeyes-Blocks:  *.eyeblk (*.eyeblk);;All files: * (*)",None)
		)
		if self.fileName:
			self.save()
		return
		
	def makeDirty(self):
		self.dirty="*"
		self.setWindowTitle(self.currentTitle())
		return
		
	def closeEvent(self, event):
		ok = True
		if self.dirty:
			ok=QMessageBox.question(
				self, _translate("eyeBlocks.mainwindow","Please confirm",None),
					_translate("eyeBlocks.mainwindow","""\
The current work is not yet saved,
do you really want to quit the application?
""",None),
				QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes
		if ok:
			QMainWindow.closeEvent(self,event)
			event.accept() # let the window close
		else:
			event.ignore()
		return

	def currentTitle(self):
		"""
		:returns: the current title of the main window, taking in account the file name and a dirty flag.
		:rtype: str
		"""
		return "Blocks (%s)%s" %(basename(str(self.fileName)), self.dirty)
		
	def warn(self, text):
		"""
		appends a warning to the messages, and adds a line break.
		
		:param text: the warning to display, with HTML syntax.
		:type text: QString or str
		"""
		self.messages.insertHtml(text)
		self.messages.insertHtml("<br>")
		self.messages.ensureCursorVisible ()
		return

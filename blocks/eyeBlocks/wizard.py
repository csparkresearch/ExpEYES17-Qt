# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
############################################################################
#
#  Copyright (C) 2017 Georges Khaznadar <georgesk@debian.org>
#
#
#  This file may be used under the terms of the GNU General Public
#  License version 3.0 as published by the Free Software Foundation,
#  or, at your preference, any later verion of the same.
#
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import print_function

import os, re
from PyQt4 import QtCore, QtGui
from xml.dom.minidom import parse, parseString
from subprocess import call, Popen, PIPE
from datetime import datetime
import threading, copy

def _translate(context, text, disambig):
	return QtGui.QApplication.translate(context, unicode(text), disambig)
        

class BlockSource(object):
	"""
	this class is used to work with the structure of blocks given by the
	working area
	
	:param bw: the working area
	:type bw: BlockWidget
	"""
	
	def __init__(self, bw):
		object.__init__(self)
		self.bw=bw
		self.count=len(bw.components)
		self.chains, self.dangling = self.makeChains()
		

	def makeChains(self):
		"""
		finds chained components in the working area
		
		:returns: a list of chaines components and a list of dangling components, as indexes
		:rtype: tuple(list(list(int)), list(int))
		"""
		placed=[]
		chains=[]
		for d in range(self.count):
			for l in chains:
				for c in l:
					if d in l: continue
					elif self.bw.areSnappedComponents(d,c):
						l.insert(l.index(c),d); placed.append(d)
					elif self.bw.areSnappedComponents(c,d):
						l.insert(l.index(c)+1,d); placed.append(d)
			if d in placed: continue
			for e in range(self.count):
				if e in placed: continue
				if self.bw.areSnappedComponents(d,e):
					chains.append([d,e]); placed.append(d); placed.append(e)
				elif self.bw.areSnappedComponents(e,d):
					chains.append([e,d]); placed.append(d); placed.append(e)
		return chains, [d for d in range(self.count) if d not in placed]

	def structureWarnings(self):
		"""
		emits a list of warnings about the working's area connections
		
		:returns: a list of warnings
		:rtype: list(str)
		"""
		warnings=[]
		ns = self.bw.notSnapped()
		if ns: 
			for c,s in ns:
				if self.bw.components.index(c) not in self.dangling:
					# warn only for non-dangling components
					warnings.append("Missing snap Point: %s / %s" %(c.summary(), s.text))
		if self.dangling:
			warnings.append("Dangling components: %s" \
				%(", ".join([self.bw.components[i].summary() for i in self.dangling])))
		return warnings
		
def compile_(mw, directory):
	"""
	compile expeyes-blocks for a given target

	:param bw: main window
	:type bw: BlockMainWindow
	:param directory: place to make the build
	:type directory:
	:returns: the path to the main python program
	"""
	bw=mw.widget
	bs=BlockSource(bw)
	sw=bs.structureWarnings()
	for w in sw:
		w="<span style='color:red'>[struct warn]</span> "+w
		mw.warn(w)
	target=bw.boxModel
	components=bw.components
	templatePath=os.path.join(os.path.dirname(__file__),"templates")
	if target=="expeyes-17" or target=="expeyes-junior":
		call("cp {blocktemplate} {d}/block1.ui".format(
			blocktemplate=os.path.join(templatePath,"block1.ui.template"),
			d=directory
		),
		shell=True)
		call("pyuic4 {d}/block1.ui -o {d}/ui_block1.py".format(d=directory), shell=True)
		now=datetime.now().isoformat()
		cmd="cat {runtemplate} | sed 's/^\\(# generation date:\\).*/\\1 {t}/' > {d}/run.py".format(
			runtemplate=os.path.join(templatePath,"run.py.template"),
			d=directory,t=now
		)
		call(cmd, shell=True)
		mw.warn(_translate("eyeBlocks.wizard","<span style='color:blue'>[Compilation: done]</span> output in <b>%1</b> for %2.",None).arg(directory).arg(target))
	return "{d}/run.py".format(d=directory)
	
def run(program):
	"""
	runs program in a non-blocking thread

	:param program: the path to a main python program
	:type program:
	"""
	cmd="(python %s &)" %program
	def my_run():
		call(cmd, shell=True)
	thread = threading.Thread(target=my_run)
	thread.start()
	return
	
		
		
	
	
		

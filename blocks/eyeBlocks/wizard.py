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

import os, re, io
from PyQt4 import QtCore, QtGui
from xml.dom.minidom import parse, parseString
from subprocess import call, Popen, PIPE
from datetime import datetime
import threading, copy

from voltagecomponent import VoltageComponent

def _translate(context, text, disambig):
	return QtGui.QApplication.translate(context, unicode(text), disambig)
        

class BlockSource(object):
	"""
	this class is used to work with the structure of blocks given by the
	working area
	
	:param BlockWidget bw: the working area
	:property timeComponent: a TimeComponent if there is some, or None
	:property scope: a ChannelComponent with "scope" in its ident, if there is some, else None
	"""
	
	def __init__(self, bw):
		object.__init__(self)
		self.bw=bw
		self.count=len(bw.components)
		self.graph, self.dangling = self.makeGraph()
		self.debugGraph()
		
		l=[c for c in self.bw.components if "time" in c.ident]
		self.timeComponent = l[0] if l else None
		
		l=[c for c in self.bw.components if "scope" in c.ident]
		self.scope=l[0] if l else None
		self.xscope=None
		self.yscope=4*[0]
		######### TAKE IN ACCOUNT SCOPE'S INPUTS ##########################
		if self.scope:
			sci=bw.components.index(self.scope)
			cc=len(self.bw.components)
			scopeInputs=[(l, [str(sp.text) for sp in self.graph[l][sci]]) for l in range(cc) if self.graph[l][sci]]
			for i in (1,2,3,4):
				l = [self.bw.components[n].code for n, texts in scopeInputs if texts[1]=="block-in-signal-%s" %i]
				self.yscope[i-1] = l[0] if l else 0
			l=[self.bw.components[n] for n, texts in scopeInputs if texts[1]=="block-in-signal-x"]
			self.xscope = l[0] if l else None
			if isinstance(self.xscope, VoltageComponent):
				print("HELLO, something should be done in the case of Lissajous setup!")
		

	def debugGraph(self):
		"""
		Shows debug information about the graph
		"""
		result=""
		result+="%5ls" %""
		for i in range(self.count):
			result+="%3s" %i
		result+="\n"
		i=0
		for l in self.graph:
			result+="%5ls" %i
			for c in l:
				if c:
					result+="%3s" %"*"
				else:
					result+="%3s" %"."
			result+="\n"
			i+=1
		result+="\n"
		for i in range(self.count):
			result+="%s => %s\n" %(i, self.bw.components[i].summary())
		QtGui.QMessageBox.warning(self.bw, "line -> column", result)

	def makeGraph(self):
		"""
		computes the graph of connected snap points
		
		:returns: a directed graph and a list of dangling components, as indexes
		:rtype: (list(list((SnapPoint,SnapPoint))), list(int))
		"""
		graph=[]
		placed=[]
		for d in range(self.count):
			l=[]
			for e in range(self.count):
				snaps=self.bw.areSnappedComponents(d,e)
				l.append((snaps))
				if snaps: 
					placed.append(d); placed.append(e)
			graph.append(l)
		return graph, [d for d in range(self.count) if d not in placed]

	def structureWarnings(self):
		"""
		emits a list of warnings about the working's area connections
		
		:returns: a list of warnings
		:rtype: list(str)
		"""
		warnings=[]
		ns = self.bw.notSnapped()
		if ns: 
			for s in ns:
				if self.bw.components.index(s.parent) not in self.dangling:
					# warn only for non-dangling components
					warnings.append(_translate("eyeBlocks.wizard","Unconnected snap Point: %1: %2",None).arg(
						s.text).arg(
						s.parent.summary())
					)
		if self.dangling:
			warnings.append(_translate("eyeBlocks.wizard","Dangling components: %1",None).arg(
				", ".join([self.bw.components[i].summary() for i in self.dangling])))
		return warnings
		
def compile_(mw, directory):
	"""
	compile expeyes-blocks for a given target

	:param BlockMainWindow bw: main window
	:param str directory: place to make the build
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
		call("cp {commontemplate} {d}/common.py".format(
			commontemplate=os.path.join(templatePath,"common.py.template"),
			d=directory
		),
		shell=True)
		call("pyuic4 {d}/block1.ui -o {d}/ui_block1.py".format(d=directory), shell=True)
		now=datetime.now().isoformat()
		######### compiling the connections found in the graph ########
		infileName=os.path.join(templatePath,"run.py.{}.template".format(target))
		outfileName=os.path.join(directory,"run.py")
		with io.open(infileName, encoding="utf-8") as infile:
			with io.open(outfileName,"w", encoding="utf-8") as outfile:
				lines=infile.readlines()
				for l in lines:
					l=re.sub(r"^TITLE=.*","TITLE='Experiment generated by ExpEyes-Blocks'",l)
					######### TIME RELATED DATA #######################
					if bs.timeComponent:
						l=re.sub(r"^NP=.*","NP=%d" %bs.timeComponent.npoints,l)
						l=re.sub(r"^TG=.*","TG=%d" %bs.timeComponent.delay,l)
					######### SCOPE RELATED DATA #######################
					if bs.scope:
						l=re.sub(r"^CHANINPUTS=.*","CHANINPUTS=%s" %bs.yscope,l)
					outfile.write(l)
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
	
		
		
	
	
		

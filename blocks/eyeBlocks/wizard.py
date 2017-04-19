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
import threading

def compile_(bw, directory):
	"""
	compile expeyes-blocks for a given target

	:param bw: working area
	:type bw: BlockWidget
	:param directory: place to make the build
	:type directory:
	:returns: the path to the main python program
	"""
	target=bw.boxModel
	components=bw.components
	templatePath=os.path.join(os.path.dirname(__file__),"templates")
	if target=="expeyes-17":
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
	
		
		
	
	
		

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

def compile_(components, directory, target):
	"""
	compile expeyes-blocks for a given target
	@param directory place to make the build
	@param target model of an expeyes box
	"""
	if target=="expeyes-17":
		call("cp templates/block1.ui.template %s/block1.ui" %directory, shell=True)
		call("pyuic4 {d}/block1.ui -o {d}/ui_block1.py".format(d=directory), shell=True)
	return
		

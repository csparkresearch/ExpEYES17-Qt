# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
# cspark_expeyes - Qt based Application stack to support ExpEYES-17.
#
# Source Link : https://github.com/csparkresearch/ExpEYES17-Qt
#
# Copyright (C) 2016 by Jithin B.P. <jithinbp@gmail.com>
# Contributors:
# - Jithin B.P
# - Georges Khaznadar
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	# Create and display the splash screen
	splash_pix = QtGui.QPixmap(os.path.join(os.path.dirname(sys.argv[0]),os.path.join('templates','splash.png')))
	splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
	splash.setMask(splash_pix.mask())
	splash.show()
	for a in range(10):
		app.processEvents()
		time.sleep(0.01)

	from SPARK17.spark17 import *
	import time, os,functools,importlib
	import numpy as np
	import pyqtgraph as pg
	import pyqtgraph.exporters


	myapp = AppWindow(app=app)
	myapp.show()
	splash.finish(myapp)
	sys.exit(app.exec_())



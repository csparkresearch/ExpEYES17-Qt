# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
from ..Qt import QtGui,QtCore,QtWidgets

import pyqtgraph as pg
from collections import OrderedDict
import numpy as np

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class pg3dWidgets(object):
	"""
	This class contains methods for 3d plots
	
	feature list : 
	
	"""

	plotDict = {}
	plots3d = []
	widgetArray = []
	def __init__(self,*args,**kwargs):
		import pyqtgraph.opengl as gl
		self.gl = gl
		pass


	def popup3dPlot(self,col='#FFF'):
		plot3d = self.gl.GLViewWidget()
		plot3d.setWindowTitle('3D Plot')
		plot3d.setCameraPosition(distance=50)
		plot3d.show()
		#gx = gl.GLGridItem();gx.rotate(90, 0, 1, 0);gx.translate(-10, 0, 0);self.plot.addItem(gx)
		#gy = gl.GLGridItem();gy.rotate(90, 1, 0, 0);gy.translate(0, -10, 0);self.plot.addItem(gy)
		gz = self.gl.GLGridItem();#gz.translate(0, 0, -10);
		plot3d.addItem(gz);
		plot3d.opts['distance'] = 40
		plot3d.opts['elevation'] = 10
		plot3d.opts['azimuth'] = 20

		import numpy as np
		p4 = self.gl.GLSurfacePlotItem(z=np.array([[0.1,0.1],[0.1,0.1]]), shader='heightColor', computeNormals=False, smooth=False)
		p4.shader()['colorMap'] = np.array([0.2, 2, 0.5, 0.2, 1, 1, 0.2, 0, 2])
		plot3d.addItem(p4)

		self.plots3d.append(plot3d)
		return plot3d,p4






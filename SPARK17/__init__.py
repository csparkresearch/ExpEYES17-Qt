
## 'Qt' is a local module; it is intended mainly to cover up the differences
## between PyQt4 and PySide.
import os
os.environ['PYQTGRAPH_QT_LIB'] = 'PyQt5'
os.environ['SPARK17_QT_LIB'] = 'PyQt5'

from .Qt import QtGui,QtCore

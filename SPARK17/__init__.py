
## 'Qt' is a local module; it is intended mainly to cover up the differences
## between PyQt4 and PyQt5.
import os
ENVIRON = 'PyQt4'

os.environ['PYQTGRAPH_QT_LIB'] = ENVIRON
os.environ['SPARK17_QT_LIB'] = ENVIRON

from .Qt import QtGui,QtCore

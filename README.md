[![Build Status](https://api.travis-ci.org/csparkresearch/ExpEYES17-Qt.svg?branch=master)](https://api.travis-ci.org/csparkresearch/ExpEYES17-Qt)
# ExpEYES17-Qt
Qt based toolkit for accessing [ExpEYES-17](http://expeyes.in)
![](SPARK17/help/_apps/images/photographs/sensor-logger.jpg =600x)
![](SPARK17/help/_apps/images/screencasts/oscilloscope.gif =600x)
## Building from source for python2.7 with PyQt4

### Dependencies

+ On Debian/Ubuntu
  + sudo apt-get install python-pyqt4 , python-pyqtgraph, python-scipy, python-pyqt4.qtsvg, pyqt4-dev-tools, python-pyqt4.qtwebkit, python-serial
  + make

`python -m SPARK17.spark17`


## Building from source for python3 with PyQt5

### Installing Dependencies

+ On Debian/Ubuntu
  + sudo apt-get install python3-pyqt5 , python3-pyqtgraph, python3-scipy, python3-pyqt5.qtsvg, pyqt5-dev-tools, python3-pyqt5.qtwebkit, python3-serial
  + make QT_VERSION=PyQt5

`python3 -m SPARK17.spark17`

## Housekeeping

`make clean` wipes out all generated files and leves only sources.



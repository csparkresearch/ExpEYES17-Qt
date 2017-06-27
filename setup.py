#!/usr/bin/env python


#!/usr/bin/env python

from distutils.core import setup

setup(name='ExpEYES',
	version='0.1',
	description='Experiment GUIs for ExpEYES-17',
	author='Jithin B.P.',
	author_email='csparkresearch@gmail.com',
	url='https://expeyes.in',
	install_requires = ['pyqtgraph>=0.9.10','pyqt5'],
	packages=['expeyes','expeyes.SENSORS'],
)



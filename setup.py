#!/usr/bin/env python


#!/usr/bin/env python

from distutils.core import setup

setup(name='ExpEYES17',
	version='0.1',
	description='Experiment GUIs for ExpEYES-17. Uses PyQt4',
	author='Jithin B.P.',
	author_email='csparkresearch@gmail.com',
	include_package_data=True,
	url='https://expeyes.in',
	install_requires = ['pyqtgraph>=0.9.10','pyqt4'],
	packages=['SPARK17','SPARK17.expeyes','SPARK17.expeyes.SENSORS'],
)



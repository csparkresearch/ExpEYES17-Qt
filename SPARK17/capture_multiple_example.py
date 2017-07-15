# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-

import expeyes.eyes17 as eyes
from pylab import *

import time
p=eyes.open()
p.set_sine(1000)
p.set_sqr1(1000)

t,v, tt,vv = p.capture_hr_multiple(300, 100, 'A1','A2')

plot(t,v)
plot(tt,vv)

show()


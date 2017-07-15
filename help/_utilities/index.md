---
layout: e17page
title: "index"
description: "introduction to general purpose utilities goes on this page"
active: utilities
---


## General Purpose utilities for ExpEYES-17

### Code example to acquire a trace from A1, and plot it

```python
#code snippet example
from expeyes import eyes17
p=eyes17.open()
x,y = p.capture1('CH1',1000,1)

from pylab import *
plot(x,y)
show()
```

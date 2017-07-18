---
layout: e17page
title: "index"
description: "L'introduction aux utilitaires généraux vient ici"
active: utilities
---


## Utilitaires généraux pour ExpEYES-17

### Exemple de code pour capturer des échantillons de A1, et en tracer un graphique

```python
#########################
# petit exemple de code #
#########################
from expeyes import eyes17
p=eyes17.open()
x,y = p.capture1('CH1',1000,1)

from pylab import *
plot(x,y)
show()
```

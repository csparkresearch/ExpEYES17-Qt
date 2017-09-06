---
layout: e17page
title: "index"
description: "introduction to experiment related apps goes on this page"
active: apps
---

```python
#Example code to capture a trace and plot it
from expeyes import eyes17
p = eyes17.open()

#Fetch 1000 points from A1 with 1uS between each consecutive point
x,y = p.capture1('A1',1000,1)
from pylab import *
plot(x,y)
show()
```


{% include experiment_gallery.html %}

<script type="text/javascript">
{% include gallery.js %}
</script>

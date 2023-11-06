# bokeh_smith
For drawing Smith Charts with Bokeh

# Example
Here's a usage within a Jupyter notebook:

```
from bokeh.io import show, output_notebook
output_notebook()

import numpy as np
from bokeh_smith import smith_chart

p=smith_chart(width=200,height=200)
s11=np.linspace(1,.8,10)*np.exp(2*np.pi*1j*np.linspace(0,.1,10))
p.circle(s11.real,s11.imag)
show(p)
```

which should produce a basic Smith chart with 10 points plotted.
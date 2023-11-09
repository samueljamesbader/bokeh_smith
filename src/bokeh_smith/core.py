import numpy as np
from bokeh.plotting import figure
from bokeh.models import Range1d


def smith_chart(
             a_values=np.r_[0, .25, .5, 1, 2, 4],
             b_values=np.r_[-3, -2, -1, -.5, -.25, -.125, .125, .25, .5, 1, 2, 3],
             *args, **kwargs):
    """A bokeh figure but with a Smith chart pre-drawn on it.

    Args:
        a_values (sequence): which curves of constant normalized real
            impedance to draw
        b_values (sequence): which curves of constant normalized imaginary
            impedance to draw [zero is always drawn]
        *args,**kwargs: passed directly to bokeh figure()
    """
    p = figure(x_range=Range1d(start=-1, end=1, bounds=(-1, 1)),
               y_range=Range1d(start=-1, end=1, bounds=(-1, 1)),
               *args, **kwargs)

    # Curves of constant a=Re{Γ} are circles with center x0,y0 = a/(a+1),0 with radius 1/(a+1)
    a = np.asarray(a_values)
    p.ellipse(x=a / (a + 1), y=0, width=2 / (a + 1), height=2 / (a + 1), fill_color=None, line_color='grey',
                 line_width=.5)

    # Curves of constant b=Im{Γ} are circles with center x0,y0 = 1,1/b with radius 1/b
    # And for b=0, that's just a horizontal line at y=0
    b = np.asarray(b_values)
    p.ellipse(x=1, y=1 / b, width=2 / b, height=2 / b, fill_color=None, line_color='grey', line_width=.5)
    p.line([-1, 1], [0, 0], line_color='grey', line_width=.5)

    # Cover up the area above and below the unit circle
    x = np.linspace(-1, 1, 30)
    p.varea(x=(x - .5) * 1.01 + .5, y1=-np.sqrt(1 - x ** 2) - .01, y2=-2, fill_color='white')
    p.varea(x=(x - .5) * 1.01 + .5, y1=np.sqrt(1 - x ** 2) + .01, y2=2, fill_color='white')

    # Put an x in the center
    p.x(0, 0, line_color='grey')

    # Turn off axis and cartesian grid
    p.xaxis.visible = False
    p.yaxis.visible = False
    p.grid.visible = False

    return p

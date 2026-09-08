from functools import partial, wraps

import numpy as np
from bokeh.plotting import figure
from bokeh.models import Range1d


def smith_chart(
             a_values=np.r_[0, .25, .5, 1, 2, 4],
             b_values=np.r_[-3, -2, -1, -.5, -.25, -.125, .125, .25, .5, 1, 2, 3],
             impedance_or_admittance='impedance',
             *args, **kwargs):
    """A bokeh figure but with a Smith chart pre-drawn on it.

    Args:
        a_values (sequence): which curves of constant normalized real
            impedance to draw
        b_values (sequence): which curves of constant normalized imaginary
            impedance to draw [zero is always drawn]
        *args,**kwargs: passed directly to bokeh figure()
    """
    p = figure(x_range=Range1d(start=-1.02, end=1.02, bounds=(-1.02, 1.02)),
               y_range=Range1d(start=-1.02, end=1.02, bounds=(-1.02, 1.02)),
               *args, **kwargs)

    sgn=1 if impedance_or_admittance == 'impedance' else -1

    # Curves of constant a=Re{Γ} are circles with center x0,y0 = sgn*a/(a+1),0 with radius 1/(a+1)
    a = np.asarray(a_values)
    line_widths = np.where((a == 0)|(a == 1), 1, .5)
    p.ellipse(x=sgn*a / (a + 1), y=0, width=2 / (a + 1), height=2 / (a + 1), fill_color=None, line_color='grey',
                 line_width=line_widths)

    # Curves of constant b=Im{Γ} are circles with center x0,y0 = sgn*1,sgn*1/b with radius 1/b
    # And for b=0, that's just a horizontal line at y=0
    b = np.asarray(b_values)
    line_widths = np.where((b == 0)|(np.abs(b) == 1), 1, .5)
    p.ellipse(x=sgn, y=sgn / b, width=2 / b, height=2 / b, fill_color=None, line_color='grey', line_width=line_widths)
    p.line([-1, 1], [0, 0], line_color='grey', line_width=1)

    # Cover up the area above and below the unit circle
    x = np.linspace(-1, 1, 100)
    p.varea(x=(x - .5) * 1.01 + .5, y1=-np.sqrt(1 - x ** 2) - .01, y2=-2, fill_color='white')
    p.varea(x=(x - .5) * 1.01 + .5, y1=np.sqrt(1 - x ** 2) + .01, y2=2, fill_color='white')

    # Put an x in the center
    p.scatter(0, 0, line_color='grey', marker='x')

    # Label each constant-a circle at its left crossing of the real axis, x = (a-1)/(a+1)
    p.text(x=sgn*(a - 1) / (a + 1), y=0, text=[f'{v:g}' for v in a],
           text_color='black', text_font_size='8pt',
           text_align='center', text_baseline='bottom')

    # Label each constant-b arc where it meets the unit circle, Γ = ((b²-1)+2bi)/(b²+1)
    p.text(x=sgn*(b ** 2 - 1) / (b ** 2 + 1), y=sgn*2 * b / (b ** 2 + 1), text=[f'{v:g}' for v in b],
           text_color='black', text_font_size='8pt',
           text_align='center', text_baseline='middle')

    # Turn off axis and cartesian grid
    p.xaxis.visible = False
    p.yaxis.visible = False
    p.grid.visible = False

    return p

smith_chart_z = wraps(smith_chart)(partial(smith_chart, impedance_or_admittance='impedance'))
smith_chart_y = wraps(smith_chart)(partial(smith_chart, impedance_or_admittance='admittance'))

if __name__ == '__main__':
    from bokeh.plotting import show
    show(smith_chart_z())
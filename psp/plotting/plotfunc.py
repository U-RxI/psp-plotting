from cmath import cos, sin
from math import atan2, radians
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from typing import Iterable
import numpy as np

# Styling
ALPHA_BASE = 0.5 # For quiver
TEXT_FONTSIZE = 10

def nplot(ax : plt.Axes, x : Iterable, y : Iterable, **kvargs):
    #Normal plot
    p = ax.plot(x, y, **kvargs)
    return p

def plot_textbox(ax : plt.Axes, x : float, y : float, s : str, box : dict = {}, **kwargs):
    textbox = ax.text(x, y, s, fontsize = TEXT_FONTSIZE, alpha = 1, **kwargs)
    if box:
        textbox.set_bbox(box)
    return textbox
    
def plot_quiver(ax : plt.Axes, phasor : complex, ref : tuple, color : str, text : str, dx : float = 0, dy : float = 0, polar : bool = True, **kwargs):
    if polar:
        u = atan2(phasor.imag,phasor.real)
        v = abs(phasor)
        coor = [ref[0], ref[1], u, v]
    else:
        coor = [ref[0], ref[1], phasor.real, phasor.imag]
    
    quiver = ax.quiver(*coor,
                         color = color,
                         angles='xy',
                         scale_units = 'xy',
                         scale = 1,
                         **kwargs)
    if text:
        plot_textbox(ax = ax,
                     x = quiver.U + dx,
                     y = quiver.V + dy,
                     s = text)
    return quiver 

# def plot_quiver(ax : plt.Axes, phasor : complex, color : str, text : str, dx : float = 0, dy : float = 0, polar : bool = True, **kwargs):
#     if polar:
#         u = atan2(phasor.imag,phasor.real)
#         v = abs(phasor)
#         coor = [0, 0, u, v]
#     else:
#         coor = [0, 0, phasor.real, phasor.imag]
    
#     quiver = axes.quiver(*coor,
#                          color = color,
#                          angles='xy',
#                          scale_units = 'xy',
#                          scale = 1,
#                          **kwargs)
    
#     plot_textbox(axes = axes,
#                  x = quiver.U + dx,
#                  y = quiver.V + dy,
#                  s = text)
#     return quiver 

def plot_aux_line(ax : plt.Axes, x0 : float = 0, y0 : float = 0, magnitude : float = 1, angle : float = 0, text : str = '', deg : bool = False, dx : float = 0, dy : float = 0, polar : bool = False, **kwargs):
    if deg:
        _angle =  radians(angle)
    
    x1 = ( magnitude*cos(_angle) ).real
    y1 = ( magnitude*sin(_angle) ).real
    
    if polar:
        coor_line = ( [x0, _angle], [y0, magnitude] )
        coor_text_x = _angle
        coor_text_y = magnitude/2
    else:
        coor_line = ([x0, x1], [y0, y1] )
        coor_text_x = (x1+x0)/2+dx
        coor_text_y = (y1+y0)/2+dy
        
    line = ax.plot( *coor_line,'--k')
    # plot textbox in middel of line
    plot_textbox(ax = ax, x = coor_text_x, y = coor_text_y, s = text, **kwargs)
    return line

def add_point(ax : plt.Axes, value:complex|tuple, **kwargs):
    if isinstance(value, complex):
        x = value.real
        y = value.imag
    if isinstance(value, tuple):
        x = value[0]
        y = value[1]
    point = ax.plot(x, y, 'o', **kwargs)
    return point

def get_centroid(A : complex, B : complex, C : complex):
    x = (A.real + B.real + C.real)/3
    y = (A.imag + B.imag + C.imag)/3
    return complex(x,y)

def phase_to_line(xA : complex, xB : complex, xC : complex):
    xAL = xA - xB
    xBL = xB - xC
    xCL = xC - xA
    return xAL, xBL, xCL

def line_to_phase(xAL : complex, xBL : complex, xCL : complex):
    xA = - (1/3) * xBL - (2/3) * xCL
    xB = (2/3) * xBL + (1/3) * xCL
    xC = - (1/3) * xBL + (1/3) * xCL
    return xA, xB, xC

def arrow(ax : plt.Axes, x : Iterable , y : Iterable, n : int = None):
    """
       Add evenly spaced arrows along a curve on a matplotlib Axes.

       Parameters
       ----------
       ax : matplotlib.axes.Axes
           The axes object on which to draw the arrows.
       x : iterable of float
           Sequence of x-coordinates of the curve.
       y : iterable of float
           Sequence of y-coordinates of the curve.
       n : int, optional
           Number of arrows to draw. If None, an arrow is drawn for every x point.

       Notes
       -----
       - Arrows are placed at approximately equal index intervals,
         not necessarily equal arc-length.
       - The arrows use a fixed arrow style ('->') and a mutation scale of 15.

       Examples
       --------
       >>> fig, ax = plt.subplots()
       >>> t = np.linspace(0, 2*np.pi, 100)
       >>> x = np.cos(t)
       >>> y = np.sin(t)
       >>> line = ax.plot(x, y)
       >>> arrow(ax, x, y, n=5)
       >>> plt.show() #doctest: +SKIP
       """
    if n:
        d = len(x)//(n+1)
    else:
        d = 1
    ind = np.arange(d,len(x),d)
    for i in ind:
        ar = FancyArrowPatch ((x[i-1],y[i-1]),(x[i],y[i]),
                              arrowstyle='->', mutation_scale=15)
        ax.add_patch(ar)


import matplotlib.pyplot as plt
from psp.plotting.plotfunc import (
    plot_quiver,
    plot_textbox,
    plot_aux_line,
    add_point,
    nplot,
)
import psp.plotting.plotfunc as plotfunc
from psp.plotting.angle import plot_angle
from abc import ABC, abstractmethod
from math import cos, sin, pi
from typing import Iterable, Callable
import numpy as np
from shapely.geometry import Polygon
from psp.plotting.fakeax import FakeAx

plt.ioff()  # to prevent figure window from showing until plt.show() is called.

# Concept
# Specielle plots from RXplot, PhasorPlot og PolarPlot arver fra ComplexPlot
# De deler en masse metoder til at plotte med.
# Alle special plot definere deres standard layout
# Ønsker man at overwrite eller added ved at bruge axis, så er der lavet en
# axis til at opsamle alle metode cal til plt.Axes.
# E.g. myplot.ax.set_xlim([-1, 5]) bliver gemt i FakeAx og bliver derefter
# først kaldt når ComplexPlot.Show() kaldes.


class ComplexPlot(ABC):
    """
    A class to represent a plot using complex numbers.
    This class utilize the matplotlib.pyplot module for plotting.

    ...

    Attributes
    ----------
    title : str
        Title of the plot.
    projection : str | None
        Parameter for the matplotlib.pyplot.figure.add_subplot function
    coordinates : list
        List of coordinates to be considered for setting the x and y limits of
        the plot.
    ax : plt.Axes
        List of coordinates to be considered for setting the x and y limits of
        the plot.


    Methods
    -------
    info(additional=""):
        Prints the person's name and age.
    """

    def __init__(
        self,
        title: str,
        ax: plt.Axes = None,
        figsize: tuple = (8, 8),
        projection: str = None,
    ):
        """
        Constructs all the necessary attributes for the abstract class
        ComplexPlot object.

        Parameters
        ----------
        title : str
            Title of the plot.
        ax : plt.Axes
            Axes object to be used for the plotting in case the figure is
            created elsewhere. If no axes is given the class creates it own
            figures and axes. The default is None.
        figsize : tuple
            Tuple with the figure size in inches.
            The default is (8, 8).
        projection : str, optional
            Parameter for the matplotlib.pyplot.figure.add_subplot function.
            Options: {None, 'aitoff', 'hammer', 'lambert', 'mollweide',
             'polar', 'rectilinear', str}
            The default is None resulting in a rectilinear projection.

        Returns
        -------
        None.

        """
        self.title = title
        self.projection = projection
        self.coordinates = []

        if ax:
            self._ax = ax
            self.ax = FakeAx(self._ax)
        else:
            self.fig = plt.figure(figsize=figsize)
            self._ax = self.fig.add_subplot(111, projection=self.projection)
            self._ax.set_title(self.title)
            self.ax = FakeAx(self._ax)

    ##########################################################################
    # plot functionalities
    ##########################################################################

    def add_phasor(
        self,
        value: complex,
        ref: tuple = (0, 0),
        name: str = "",
        color: str = None,
        polar: bool = False,
        **kwargs,
    ):
        """
        This functions adds a phasor to the plot (axes object).

        Parameters
        ----------
        value : complex
            Value of the phasor with respect to (0,0). If you wish to simple
            move with respect to ref = (1,1), you need to add 1+1j to value.
        ref : tuple, optional
            Tuple with coordinates for the beginning of the phasor.
            The default is (0,0).
        name : str, optional
            Name of the phasor. This will be plotted on as a textbox close to
            the phasor. The default is "".
        color : str, optional
            Select the color of the phasor. The default is None.
        polar : bool, optional
            Option for plotting on a axes with polar projection.
            The default is False, which is equal to a cartesian axes.
        **kwargs : N/A
            Additional arguments can be added for the underlying ax.quiver
            object.

        Returns
        -------
        None.

        """
        plot_quiver(
            ax=self.ax,
            phasor=value,
            ref=ref,
            color=color,
            text=name,
            polar=polar,
            alpha=0.7,
            **kwargs,
        )

        self.coordinates.append((value.real, value.imag))

    def add_textbox(self, x: float, y: float, s: str, box: dict = {}, **kwargs):
        """
        Method for plotting a textbox.

        Parameters
        ----------
        x : float
            x-coordinate for the position.
        y : float
            y-coordinate for the position.
        s : str
            Text for the textbox.
        box : dict, optional
            Added a box around the text box. The default is {}.
            Specific any argument to add the box e.g. {'color' : 'red'}.
        **kwargs : TYPE
            Additional arguments can be added for the underlying ax.text
            object.

        Returns
        -------
        None.

        """
        plot_textbox(self.ax, x=x, y=y, s=s, box=box, **kwargs)

        self.coordinates.append((x, y))

    def add_point(self, value: complex | tuple, **kwargs):
        """
        Method to add a point to the plot.

        Parameters
        ----------
        value : complex|tuple
            x and y coordinate for the point specified either a coordinate
            (x,y) or a complex number x+jy.
        **kwargs : TYPE
            Additional arguments can be added for the underlying ax.plot
            object.

        Returns
        -------
        None.

        """
        add_point(self.ax, value=value, **kwargs)

        self.coordinates.append((value.real, value.imag))

    def add_line(self, arange: Iterable, afunc: Callable, **kwargs):
        """
        Method to add a line to the plot based on a range and function.

        Parameters
        ----------
        arange : Iterable
            A range of values for the x-axis.
        afunc : Callable
            A function to be called afunc(x).
        **kwargs : N/A
            Additional arguments can be added for the underlying ax.plot
            object.

        Returns
        -------
        None.

        """
        x = arange
        y = list(map(afunc, arange))
        nplot(self.ax, x=x, y=y, **kwargs)

        for p in zip(x, y):
            self.coordinates.append(p)

    def add_limit(self, magnitude, angle, x0=0, y0=0, text="", deg=True, polar=False):
        plot_aux_line(
            self.ax,
            x0=x0,
            y0=y0,
            magnitude=magnitude,
            angle=angle,
            text=text,
            deg=deg,
            polar=polar,
        )

        self.coordinates.append((x0, y0))
        x1 = x0 + magnitude * cos(angle / 180 * pi)
        y1 = x0 + magnitude * sin(angle / 180 * pi)
        self.coordinates.append((x1, y1))

    def add_plot(self, x: Iterable, y: Iterable, **kwargs):
        nplot(self.ax, x=x, y=y, **kwargs)

        for p in zip(x, y):
            self.coordinates.append(p)

    def add_angle(
        self,
        r: float,
        phi_start: float,
        phi_end: float,
        text: dict = {},
        scale: float = 1,
        arrow_start: bool = False,
        arrow_end: bool = True,
    ):
        plot_angle(self.ax, r, phi_start, phi_end, text, scale, arrow_start, arrow_end)

    def add_impedance_trace(
        self, imp: Iterable[complex], start: complex = 0 + 0j, **kwargs
    ):
        """
        Method for adding an trace of impedance to the plot. The method is
        intended for plotting the combined positive sequence of multiple
        cable/line sections in a radial topology.

        Parameters
        ----------
        imp : Iterable[complex]
            A Iterable (e.g. list or tuple) of complex numbers to be plotted.
        start : complex, optional
            Start of the trace. The default is 0+0j.
        **kwargs : N/A
            Additional arguments can be added for the underlying ax.plot
            object.

        Raises
        ------
        ValueError
            The variable imp has to be either iterable[complex] or a complex number.

        Returns
        -------
        None.

        """

        if isinstance(imp, complex):
            impedances = np.cumsum([start, imp])
        elif all(isinstance(d, complex) for d in imp):
            impedances = np.cumsum([start, *imp])
        else:
            raise ValueError(
                "The variable imp has to be either iterable[complex] or a complex number"
            )

        real = [x.real for x in impedances]
        imag = [x.imag for x in impedances]

        kwargs.setdefault("color", "black")
        kwargs.setdefault("linestyle", "dashed")
        kwargs.setdefault("label", "impedance trace 1")

        self.add_plot(real, imag, **kwargs)

    def add_trajectory(
        self, Z: Iterable[complex], n: int = None, arrow: bool = True, **kwargs
    ):
        nplot(self.ax, Z.real, Z.imag, **kwargs)
        if arrow:
            plotfunc.arrow(self._ax, Z.real, Z.imag, n)

        for p in zip(Z.real, Z.imag):
            self.coordinates.append(p)

    def add_zone(self, zone: Polygon, **kwargs):
        nplot(self.ax, *zone.exterior.xy, **kwargs)

        for p in zip(*zone.exterior.xy):
            self.coordinates.append(p)

    def _get_rmax(self, scale: float = 1.1):
        """
        Method to return 110% of the maximum x and y values use for the plot.
        This value can be used to set the x and y plot limit for the plot
        automatically.

        Returns
        -------
        float
            Maximum x/y value used in the plot times 110% (default).
        scale
            Set the scale that x/y value is multiplied with. The default is 1.1.

        """
        xmax = max(map(abs, [x for x, y in self.coordinates]))
        ymax = max(map(abs, [y for x, y in self.coordinates]))

        return max(xmax, ymax) * scale

    def _get_xmax(self, scale: float = 1.1):
        """
        Method to return 110% of the maximum x values use for the plot.
        This value can be used to set the x plot limit for the plot
        automatically.

        Returns
        -------
        float
            Maximum x value used in the plot times 110% (default).
        scale
            Set the scale that x value is multiplied with. The default is 1.1.

        """
        xmax = max(map(abs, [x for x, y in self.coordinates]))

        return xmax * scale

    def _get_ymax(self, scale: float = 1.1):
        """
        Method to return 110% of the maximum y values use for the plot.
        This value can be used to set the y plot limit for the plot
        automatically.

        Returns
        -------
        float
            Maximum y value used in the plot times 110% (default).
        scale
            Set the scale that x value is multiplied with. The default is 1.1.

        """
        ymax = max(map(abs, [y for x, y in self.coordinates]))

        return ymax * scale

    def show(self):
        """
        Method to show the plot.

        Returns
        -------
        None.

        """
        self.layout(self.ax)
        self.ax.overwrite()
        plt.show()

    ##########################################################################
    @abstractmethod
    def layout(self):
        pass


# testing


# def P2R(magnitude: float, angle_deg: float) -> complex:
#    angle_rad = angle_deg / 180 * pi
#    return magnitude * (cos(angle_rad) + 1j * sin(angle_rad))

# myplot1 = RXplot(title = 'Polar plot')
# myplot1.add_phasor(value=P2R(1, 180), color='Blue', name='V1')
# myplot1.add_phasor(value=P2R(1, 30), color='Red', name='I1')
# myplot1.add_limit(1, 85, text='test', polar = True)

# myplot1.add_textbox(0.5, 0.5, 'Test')
# myplot1.show()


# myplot2 = PlotPhasor(title = 'Phasor plot')
# myplot2.add_phasor(value=P2R(4, 45), color='Blue', name='V1', polar=False)
# myplot2.add_phasor(value=P2R(6, 30), color='Red', name='I1',  polar=False)

# myplot2.ax.set_xlabel('hejdff')

# myplot2.ax.set_xlim([-1, 6])
# myplot2.set_limits([-1, 10, -1, 10])
# myplot2.add_phasor(value=P2R(6, 180), color='Red', name='I1',  polar=False)
# myplot2.add_point(value=P2R(10, 30), color='Red', label='I1')
# myplot2.add_line(range(4), lambda x : x*2)
# myplot2.add_angle(radius=1, centX=0, centY=0, startangle=10, angle=230, text = '$\\Theta$')
# myplot2.add_limit(8, 85, text='test', polar = False)
# myplot2.show()


# myplot3 = RXplot('test')
# myplot3.add_impedance_trace([0+0j, 1+1j, 2+3j])
# myplot3.add_textbox(1, 1, 'array', box={'color':'red'})
# myplot3.add_angle(1, 0, np.pi/4)
# myplot3.ax.set_aspect('equal', 'box')
# myplot3.show()


# Good source for fft
# https://pysdr.org/content/frequency_domain.html

from psp.plotting.complex_plot import ComplexPlot
from psp.plotting.plotfunc import plot_quiver, center_axis
import matplotlib.pyplot as plt


class RXplot(ComplexPlot):
    """A class for creating a complex plot."""

    def __init__(self, title: str, ax: plt.Axes = None,  figsize: tuple = (8, 8)):
        super().__init__(title, ax=ax, figsize=figsize)

    def autoscale(self):
        self.ax.set_xlim([- self._get_rmax(), self._get_rmax()])
        self.ax.set_ylim([- self._get_rmax(), self._get_rmax()])

    def _post_actions(self):
        self.ax.legend()
        self.autoscale()

    def _layout(self):
        self.ax.set_xlabel(r"$R\;[\Omega]$")
        self.ax.set_ylabel(r"$X\;[\Omega]$")
        self.ax.grid(True)


class PolarPlot(ComplexPlot):
    """A class for creating a phasor plot using a polar projection."""

    def __init__(self, title: str, ax: plt.Axes = None, figsize: tuple = (8, 8)):
        super().__init__(title=title, ax=ax, figsize=figsize, projection="polar")

    def add_phasor(
        self,
        value: complex,
        ref: tuple = (0, 0),
        name: str = "",
        color: str = None,
        **kwargs,
    ):
        plot_quiver(
            ax=self._ax,
            phasor=value,
            ref=ref,
            color=color,
            text=name,
            polar=True,
            alpha=0.7,
            **kwargs,
        )
        self.coordinates.append((value.real, value.imag))

    def autoscale(self):
        self.ax.set_rlim(0, self._get_rmax())

    def _post_actions(self):
        self.ax.legend()
        self.autoscale()

    def _layout(self):
        self.ax.set_rlabel_position(90)


class PhasorPlot(ComplexPlot):
    """
    A class for creating a phasor plot using a cartesian projection.
    The plot will have a centered x and y axis.
    """

    def __init__(self, title: str, ax: plt.Axes = None, figsize: tuple = (8, 8)):
        super().__init__(title=title, ax=ax, figsize=figsize)
        self.opt_center_axis = True

    def autoscale(self):
        self.ax.set_xlim([-self._get_rmax(), self._get_rmax()])
        self.ax.set_ylim([-self._get_rmax(), self._get_rmax()])

    def _post_actions(self):
        self.ax.legend()
        self.autoscale()

    def _layout(self):

        self.ax.set_aspect("equal", "box")
        self.grid(color="lightgrey", linestyle="-")

        self.set_xlabel("Re", fontweight="bold")
        self.set_ylabel("Im", fontweight="bold", rotation=0)

        if self.opt_center_axis:
            center_axis(ax)

class TimeSeriesPlot(ComplexPlot):
    """A class for creating a time series plot."""

    def __init__(self, title: str, ax: plt.Axes = None, figsize: tuple = (8, 8)):
        super().__init__(title, ax=ax, figsize=figsize)

    def autoscale(self):
        self.ax.autoscale()

    def _post_actions(self):
        self.ax.legend()
        self.autoscale()

    def _layout(self, ax: plt.Axes):
        ax.set_xlabel(r"Time [s]")
        ax.grid(True)
from psp.plotting.complex_plot import ComplexPlot
from psp.plotting.fakeax import FakeAx
from abc import ABC
import matplotlib.pyplot as plt


class DiffBiasPlot(ABC):
    def __init__(self, title: str, figsize: tuple = (8, 8)):
        self.title = title
        self.coordinates = []

        self.fig = plt.figure(figsize=figsize)
        self._ax = self.fig.add_subplot(111)
        self._ax.set_title(self.title)
        self.ax = FakeAx(self._ax)

    add_point = ComplexPlot.add_point
    add_textbox = ComplexPlot.add_textbox
    add_plot = ComplexPlot.add_plot
    _get_rmax = ComplexPlot._get_rmax
    show = ComplexPlot.show
    layout = ComplexPlot.layout

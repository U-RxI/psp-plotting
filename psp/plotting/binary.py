import numpy as np
from psp.plotting.fakeax import FakeAx
import matplotlib.pyplot as plt

from functools import partial

default_kwargs = {'color' : 'Blue'}

class BinaryPlot():
    """A class for creating a binary plot from a comtrade file."""

    def __init__(self, title: str, figsize : tuple = (8, 8)):
        self.title = title
        self.figsize = figsize
 
        self.fig = plt.figure(figsize=self.figsize)
        self._ax = self.fig.add_subplot(111)
        self._ax.set_title(self.title)
        self.ax = FakeAx(self._ax)

    def add_binary(self, record : object, changed_signal_only : bool = True, trigger_time_zero : bool = True, **kwargs):
        binary_plot(self._ax, record, changed_signal_only, trigger_time_zero,  **kwargs)
   
    def show(self):
        """
        Method to show the plot.

        Returns
        -------
        None.

        """
        self.layout()
        self.ax.overwrite()
        plt.show()

    def layout(self):
        self._ax.set_xlabel(r'Time [s]')
        #self.fig.set_size_inches(15, 10)
        #self.fig.subplots_adjust(left=0.2, top=0.95, bottom=0.05)

def _find_chunks(stream):
    # Identify non-zero elements
    non_zero = np.array(stream) != 0

    # Identify positions where neighbors are zero
    # Shifted arrays
    left_zero = np.roll(np.array(stream) == 0, 1)
    right_zero = np.roll(np.array(stream) == 0, -1)

    # Set boundary conditions
    left_zero[0] = True
    right_zero[-1] = True

    # Find non-zero elements with at least one zero neighbor
    condition1 = non_zero & (left_zero | right_zero)

    # (Special case) Find non-zero elements where both neighbors being zero
    condition2 = non_zero & (left_zero & right_zero)

    # Get the indices
    indices1 = np.where(condition1)[0]

    # Get the indices
    indices2 = np.where(condition2)[0]

    indices = np.sort(np.concatenate((indices1, indices2)))

    if indices.size > 0:
        indices = np.split(indices, len(indices) / 2)
    return indices


def _binary_hbar(ax, name, stream, time, changed_signal_only=True, **kwargs):
    kwargs = {**default_kwargs, **kwargs}
    # Constant signal zero
    if not any(stream):  # ones only
        if changed_signal_only:
            return
        else:
            ax.barh(name, time[-1], left=0, alpha=0, **kwargs)  # invisible bar
            return

    # Constant signal one
    if all(stream):  # ones only
        if changed_signal_only:
            return
        else:
            ax.barh(name, time[-1], left=0, **kwargs)
            return

    idx = _find_chunks(stream)
    for i, j in idx:
        start = time[i]
        end = time[j - 1]
        ax.barh(name, end - start, left=start, **kwargs)


def binary_plot(ax, record, changed_signal_only=True, trigger_time_zero=True, **kwargs):
    idx = reversed(range(len(record.status)))

    if trigger_time_zero:
        time = record.time - record.trigger_time
    else:
        time = record.time

    for i in idx:
        _binary_hbar(ax=ax,
                     name=record.status_channel_ids[i],
                     stream=record.status[i],
                     time=time,
                     changed_signal_only=changed_signal_only,
                     **kwargs)

def count_binary(record):
    total = len(record.status)
    changed = 0
    contant_zero = 0
    contant_one = 0
    for s in record.status:
        if not any(s):
            contant_zero += 1
        elif all(s):
            contant_one += 1
        else:
            changed += 1
    return total, changed, contant_zero, contant_one

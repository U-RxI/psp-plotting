#!/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
from math import atan2

from dataclasses import dataclass

ARROW_LENGTH = 0.025

# Default properties
text_prop = {
    "horizontalalignment": "center",
    "verticalalignment": "center",
    "bbox": {"color": "white"},
    "fontsize": 10,
}

line_prop = {"color": "black", "linestyle": "solid", "linewidth": 1}


@dataclass
class Point:
    x: float
    y: float


def _create_arrow(p1: Point, p2: Point, scale: float) -> tuple:
    """Function to calculate the coordinates for an arrow"""
    d = ARROW_LENGTH * scale

    ang = atan2(p2.y - p1.y, p2.x - p1.x)

    leg1 = Point(
        x=p1.x + d * np.cos(ang + np.pi / 4), y=p1.y + d * np.sin(ang + np.pi / 4)
    )

    leg2 = Point(
        x=p1.x + d * np.cos(ang - np.pi / 4), y=p1.y + d * np.sin(ang - np.pi / 4)
    )

    x = [leg1.x, p1.x, leg2.x]
    y = [leg1.y, p1.y, leg2.y]

    return x, y


def _plot_arrow(ax: plt.Axes, arrow: tuple) -> list[plt.Line2D]:
    """Function to plot a tuple with list of points to assemble an arrow"""
    obj = ax.plot(*arrow, **line_prop)
    return obj


def _plot_text(axes: plt.Axes, r: float, phi: float, s: str) -> plt.Text:
    """Function to plot a text (s) on an axis using a radius (r) and an angle (phi)"""
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    obj = axes.text(x, y, s, **text_prop)
    return obj


def plot_angle(
    ax: plt.Axes,
    r: float,
    phi_start: float,
    phi_end: float,
    text: dict = {},
    scale: float = 1,
    arrow_start: bool = False,
    arrow_end: bool = True,
) -> tuple:
    """Function to plot an angle on a complex or phasor plot"""
    length = 1000
    xrange = np.linspace(phi_start, phi_end, length)
    x = r * np.cos(xrange)
    y = r * np.sin(xrange)

    obj = []

    # plot line
    line = ax.plot(x, y, **line_prop)
    obj.append(*line)

    if text:
        # plot text
        textbox = _plot_text(ax, **text)
        obj.append(textbox)

    # plot arrows
    if arrow_start:
        p1 = Point(x[0], y[0])  # First
        p2 = Point(x[1], y[1])  # Second

        arrow = _create_arrow(p1, p2, scale)
        obj_start = _plot_arrow(ax, arrow)
        obj.append(*obj_start)

    if arrow_end:
        p1 = Point(x[-1], y[-1])  # Last
        p2 = Point(x[-2], y[-2])  # Second last

        arrow = _create_arrow(p1, p2, scale)
        obj_end = _plot_arrow(ax, arrow)
        obj.append(*obj_end)

    return tuple(obj)

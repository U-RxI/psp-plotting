from numpy import linspace
from shapely.geometry import LineString


def transfer_PQ(polygon, Un):
    t = linspace(0, 1.0, 1000)
    linestring = LineString(polygon.exterior.coords)
    out = list(map(lambda x: linestring.interpolate(x, normalized=True).coords, t))

    x2 = []
    y2 = []
    for p in out:
        if 0 in list(*p):
            continue
        xp = P(Un, *p) / 1e6
        xq = Q(Un, *p) / 1e6
        x2.append(xp)
        y2.append(xq)

    return x2, y2


def P(U, Z):
    return abs(U) ** 2 / abs(complex(*Z)) ** 2 * Z[0]


def Q(U, Z):
    return abs(U) ** 2 / abs(complex(*Z)) ** 2 * Z[1]
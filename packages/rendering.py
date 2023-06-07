from enum import Enum

import plotly.graph_objects as go

# from packages.collections import Points, Surfaces
from packages.objects import Point, Surface, Vector
from packages.utils import flatten


DEF_WINDOW_SIZE = 5


class Axis(Enum):
    X = "X"
    Y = "Y"
    Z = "Z"

    def get(self, window_size=DEF_WINDOW_SIZE):
        x = y = z = [0, 0]
        if self == Axis.X:
            x = [-window_size, window_size]
        elif self == Axis.Y:
            y = [-window_size, window_size]
        elif self == Axis.Z:
            z = [-window_size, window_size]
        return go.Scatter3d(x=x, y=y, z=z, mode="lines", name=self.value)

    @staticmethod
    def all(window_size=DEF_WINDOW_SIZE):
        return Axis.X.get(window_size), Axis.Y.get(window_size), Axis.Z.get(window_size)


def easy_plot(
    *args,
    surface_size: float = 2,
    surface_opacity: float = 0.5,
    window_size=DEF_WINDOW_SIZE
):
    fig = go.Figure()
    _range = [-window_size, window_size]
    # args = [i.values if (isinstance(i, Points) or isinstance(i, Surfaces)) else i for i in args]
    args = flatten(args)
    points = [point for point in args if isinstance(point, Point)]
    vectors = [vector.end for vector in args if isinstance(vector, Vector)]
    points += vectors
    surfaces = [surface for surface in args if isinstance(surface, Surface)]

    if not points and not surfaces:
        raise ValueError("No points or surfaces were passed")

    for point in points:
        x, y, z = point.array

        fig.add_trace(
            go.Scatter3d(x=[x], y=[y], z=[z], mode="markers", marker=dict(size=5))
        )

    for surface in surfaces:
        mg_x, mg_y, mg_z = surface.to_mesh(surface_size)
        fig.add_trace(go.Surface(x=mg_x, y=mg_y, z=mg_z, opacity=surface_opacity))

    axis_x, axis_y, axis_z = Axis.all(window_size)
    fig.add_trace(axis_x)
    fig.add_trace(axis_y)
    fig.add_trace(axis_z)
    fig.update_layout(
        scene=dict(
            xaxis=dict(title="X", color="red", range=_range),
            yaxis=dict(title="Y", color="green", range=_range),
            zaxis=dict(title="Z", color="blue", range=_range),
            aspectratio=dict(x=1, y=1, z=1),
        )
    )
    fig.show()

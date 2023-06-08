import random
import plotly.graph_objects as go
from enum import Enum
from typing import List
from packages.objects import Point, Plane, Vector, Square, Line
from packages.utils import flatten

DEF_WINDOW_SIZE = 5


def rand_colour():
    return f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})"


class Axis(Enum):
    """
    Enum class to represent axes in 3D space (X, Y, Z).
    """

    X = "X"
    Y = "Y"
    Z = "Z"

    def get(self, window_size=DEF_WINDOW_SIZE):
        """
        Returns a 3D Scatter trace along this axis.

        Parameters:
        window_size (float): The range of values to plot along this axis. Defaults to DEF_WINDOW_SIZE.

        Returns:
        plotly.graph_objects.Scattered: A 3D scatter trace along this axis.
        """

        x = y = z = [0, 0]
        if self == Axis.X:
            x = [-window_size, window_size]
        elif self == Axis.Y:
            y = [-window_size, window_size]
        elif self == Axis.Z:
            z = [-window_size, window_size]
        return go.Scatter3d(x=x, y=y, z=z, mode="lines", name=self.value)

    @staticmethod
    def add_to_fig(fig, window_size=DEF_WINDOW_SIZE):
        """
        Adds the 3 axes to a fig object

        Parameters:
        fig: figure object to add to
        window_size (float): The range of values to plot along each axis. Defaults to DEF_WINDOW_SIZE.
        """

        fig.add_trace(Axis.X.get(window_size))
        fig.add_trace(Axis.Y.get(window_size))
        fig.add_trace(Axis.Z.get(window_size))


def handle_lines(
    fig, lines: List[Line], line_thickness: float, line_opacity: float = 0.5
):
    for line in lines:
        sx, sy, sz = line.start.array
        ex, ey, ez = line.end.array
        fig.add_trace(
            go.Scatter3d(
                x=[sx, ex],
                y=[sy, ey],
                z=[sz, ez],
                mode="lines",
                line=dict(color=rand_colour(), width=line_thickness),
                opacity=line_opacity,
            )
        )


def handle_points(fig, points: List[Point], marker_size: float):
    for point in points:
        x, y, z = point.array
        fig.add_trace(
            go.Scatter3d(
                x=[x],
                y=[y],
                z=[z],
                mode="markers",
                marker=dict(size=marker_size, color=rand_colour()),
            )
        )


def handle_squares(fig, squares: List[Square], plane_opacity: float):
    for square in squares:
        x, y, z = square.to_mesh()
        fig.add_trace(
            go.Mesh3d(x=x, y=y, z=z, opacity=plane_opacity, color=rand_colour())
        )


def handle_planes(fig, planes: List[Plane], plane_size: float, plane_opacity: float):
    for plane in planes:
        x, y, z = plane.to_mesh(plane_size)
        fig.add_trace(
            go.Plane(x=x, y=y, z=z, opacity=plane_opacity, color=rand_colour())
        )


def easy_plot(
    *args,
    marker_size: float = 4,
    line_thickness: float = 4,
    plane_size: float = 2,
    plane_opacity: float = 0.5,
    window_size=DEF_WINDOW_SIZE,
):
    """
    Plots 3D points, vectors, planes and squares using Plotly.

    Parameters:
    *args (any): Variable length argument list containing objects to plot.
    marker_size (float): Size of the markers for points. Defaults to 3.
    plane_size (float): Size of the mesh for planes. Defaults to 2.
    plane_opacity (float): Opacity of planes and squares. Defaults to 0.5.
    window_size (float): The range of values to plot along each axis. Defaults to DEF_WINDOW_SIZE.

    Returns:
    None
    """

    fig = go.Figure()
    args = flatten(args)

    lines = [line for line in args if isinstance(line, Line)]
    points = [point for point in args if isinstance(point, Point)]
    squares = [square for square in args if isinstance(square, Square)]
    planes = [plane for plane in args if isinstance(plane, Plane)]
    vectors = [vector.end for vector in args if isinstance(vector, Vector)]

    if not (points or squares or planes or vectors):
        raise ValueError("No points or planes were passed")

    handle_lines(fig, lines, line_thickness)
    handle_points(fig, points, marker_size=marker_size)
    handle_squares(fig, squares, plane_opacity=plane_opacity)
    handle_planes(fig, planes, plane_size=plane_size, plane_opacity=plane_opacity)
    handle_points(fig, vectors, marker_size=marker_size)

    Axis.add_to_fig(fig, window_size)
    _range = [-window_size, window_size]
    fig.update_layout(
        scene=dict(
            xaxis=dict(title="X", color="red", range=_range),
            yaxis=dict(title="Y", color="green", range=_range),
            zaxis=dict(title="Z", color="blue", range=_range),
            aspectratio=dict(x=1, y=1, z=1),
        ),
        showlegend=False,
    )
    fig.show()

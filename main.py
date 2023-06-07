from packages.rendering import easy_plot
from packages.objects import Point, Vector, Surface, Line

if __name__ == "__main__":
    FOCAL_LENGTH = 0.5
    WIDTH = 36
    HEIGHT = 24

    camera = Point(1, 1, 1)
    center = camera.vector.shrink_by(FOCAL_LENGTH).direction
    camera_plane = Surface.is_perpendicular_to_at(camera.vector, center)
    center_to_up = Line.from_(center).to(camera_plane.intersects(Vector.up())).vector.shrink_to(0.01)
    up = center_to_up.end
    down = (-center_to_up).end

    easy_plot(
        Point.origin(),
        camera,
        center,
        up,
        down,
        # down_to_up,
        # Vector.intersects(camera.vector, down_to_up)
        # rl,
    )

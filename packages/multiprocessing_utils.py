from packages.objects import Square, Line


def picture_to_rays(picture: Square, pixel_width, pixel_height, camera_radius, offset):
    return picture.to_rays(pixel_width, pixel_height, camera_radius + offset)


def ray_to_mesh_points(ray: Line, points_density_for_line, subject_radius):
    return ray.to_mesh(points_density_for_line, subject_radius)

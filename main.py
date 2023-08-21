from multiprocessing import Pool, cpu_count
import time

import numpy as np
from tqdm import tqdm
from scipy.spatial import KDTree
from packages.collections import Points, Squares
from packages.multiprocessing_utils import picture_to_rays, ray_to_mesh_points
from packages.objects import SubSpace, Point
from functools import partial
from packages.rendering import easy_plot


def assign_center(tree, point_cloud, centre, subspace_radius):
    distances, indices = tree.query(
        centre,
        distance_upper_bound=subspace_radius * np.sqrt(2),
        k=len(coords),
    )
    points = [
        point_cloud[i]
        for indices_index, i in enumerate(indices)
        if distances[indices_index] != float("inf")
    ]
    return centre, points


if __name__ == "__main__":
    subject_radius = 1
    camera_radius = 3
    cams_along_inclination = 1
    inclinations_range = [20, 60, 80]

    focal_length = 50
    sensor_width = 36
    sensor_height = 24
    pixel_width = 6
    pixel_height = 4
    unit = 1000  # mm

    points_density_for_line = 20
    window_size = 5
    subspace_count = 2
    # CPU_COUNT = 1
    CPU_COUNT = cpu_count()

    cameras = Points.get_points_at_inclinations(
        camera_radius, cams_along_inclination, inclinations_range
    )
    pictures = Squares.generate_pictures(
        cameras, focal_length, sensor_width, sensor_height, unit
    )

    # get rays
    print("getting rays ...")
    with Pool(CPU_COUNT) as pool:
        func = partial(
            picture_to_rays,
            pixel_width=pixel_width,
            pixel_height=pixel_height,
            camera_radius=camera_radius,
            offset=0.5,
        )
        rays_temp = list(tqdm(pool.imap(func, pictures), total=len(pictures)))
    rays = [ray for sublist in rays_temp for ray in sublist]
    time.sleep(0.5)
    print("got rays")

    # point cloud
    print("getting point cloud ...")
    with Pool(CPU_COUNT) as pool:
        func = partial(
            ray_to_mesh_points,
            points_density_for_line=points_density_for_line,
            camera_radius=camera_radius,
            subject_radius=subject_radius,
        )
        point_cloud_temp = list(tqdm(pool.imap(func, rays), total=len(rays)))
    point_cloud = [point for sublist in point_cloud_temp for point in sublist]
    time.sleep(0.5)
    print("got point cloud")

    subspace = SubSpace(subspace_count)
    coords = [point.array.tolist() for point in point_cloud]
    subspace_tree = KDTree(coords)

    # subspace assignment
    print("assigning point cloud ...")
    # all_close_points = []
    for subspace_centre in tqdm(subspace.points, desc="Assigning points"):
        subspace_centre, close_points = assign_center(
            subspace_tree, point_cloud, subspace_centre, subject_radius / subspace_count
        )
        for point in close_points:
            subspace.subspace_assignments[str(subspace_centre)].add(point)
        # all_close_points.extend(close_points)
    time.sleep(0.5)
    print("assigned point cloud")

    # for k, v in subspace.subspace_assignments.items():
    #     print(k)
    #     print(v)
    #     print("\n")

    print("rendering...")
    easy_plot(
        Point.origin(),
        cameras.elements,
        subspace,
        window_size=window_size,
        subject_radius=subject_radius,
        show_surface=False,
    )
    print("render completed")

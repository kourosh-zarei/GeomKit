from multiprocessing import Pool, cpu_count
import time
from tqdm import tqdm
from scipy.spatial import KDTree
from packages.collections import Points, Squares
from packages.multiprocessing_utils import picture_to_rays, ray_to_mesh_points
from packages.objects import SubSpace, Point
from functools import partial
from packages.rendering import easy_plot


def assign_center(centre):
    distances, indices = tree.query(
        centre,
        distance_upper_bound=0.5,
        k=len(coords),
    )
    points = [
        point_cloud[i]
        for indices_index, i in enumerate(indices)
        if distances[indices_index] != float("inf")
    ]
    return centre, points


if __name__ == "__main__":
    subject_radius = 0.5
    camera_radius = 3
    cams_along_inclination = 5
    inclinations_range = [45]

    focal_length = 50
    sensor_width = 36
    sensor_height = 24
    pixel_width = 108
    pixel_height = 72
    unit = 1000  # mm

    points_density_for_line = 10
    window_size = 5
    # CPU_COUNT = 1  # 
    CPU_COUNT = cpu_count()  # 100%|██████████| 6/6 [00:59<00:00,  9.84s/it]

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
            offset=0.5
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
            subject_radius=subject_radius
        )
        point_cloud_temp = list(tqdm(pool.imap(func, rays), total=len(rays)))
    point_cloud = [point for sublist in point_cloud_temp for point in sublist]
    time.sleep(0.5)
    print("got point cloud")

    subspace = SubSpace(5)
    coords = [point.array.tolist() for point in point_cloud]
    tree = KDTree(coords)

    # subspace assignment
    print("assigning point cloud ...")
    all_close_points = []
    for point in tqdm(subspace.points, desc="Assigning points"):
        center, close_points = assign_center(point)
        for point in close_points:
            subspace.subspace_assignments[str(center)].add(point.name)
        all_close_points.extend(close_points)
    time.sleep(0.5)
    print("assigned point cloud")

    # for k, v in subspace.subspace_assignments.items():
    #     print(k)
    #     print(v)
    #     print("\n")

    # print("rendering...")
    # easy_plot(
    #     Point.origin(),
    #     cameras.elements,
    #     all_close_points,
    #     window_size=window_size,
    #     subject_radius=subject_radius,
    # )
    # print("render completed")

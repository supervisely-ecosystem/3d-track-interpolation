import functools

import sly_globals as g
import supervisely_lib as sly
from interpolation import get_coords, interpolate_all, plot
from supervisely_lib.geometry.cuboid_3d import Cuboid3d, Vector3d


def send_error_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        value = None
        try:
            value = func(*args, **kwargs)
        except Exception as e:
            request_id = kwargs["context"]["request_id"]
            g.my_app.send_response(request_id, data={"error": repr(e)})
        return value

    return wrapper


def get_interpolation_figures(request_figures_id, dataset_id):
    pointclouds = sorted(g.api.pointcloud.get_list(dataset_id), key=lambda x: x.name)
    pointcloud_ids = [x.id for x in pointclouds]

    requested_figures = g.api.pointcloud.figure.get_by_ids(dataset_id, request_figures_id)
    request_pointcloud_ids = [fig.entity_id for fig in requested_figures]

    first_cloud = pointcloud_ids.index(request_pointcloud_ids[0])  # firtst cloud
    last_cloud = pointcloud_ids.index(request_pointcloud_ids[-1])  # last cloud
    if last_cloud > first_cloud:
        pointclouds_to_interp = pointcloud_ids[first_cloud:last_cloud + 1]
    elif last_cloud < first_cloud:
        raise ValueError("Reversed sequence or wrong geometries order!")

    # all figures the same object
    assert (all(rf.object_id == requested_figures[0].object_id for rf in requested_figures))

    sly.logger.debug(f"Dataset ID:{dataset_id}")
    sly.logger.debug(f"Pointcloud IDS:{pointcloud_ids}")
    sly.logger.debug(f"Requsted Pointcloud IDS:{request_pointcloud_ids}")
    sly.logger.debug(f"Pointclouds to interp:{pointclouds_to_interp}")
    return requested_figures, request_pointcloud_ids, pointclouds_to_interp


def upload_new_figures(res_coords, request_pointcloud_ids, pointclouds_to_interp, source_figure):
    for figure_idx, pc_id in enumerate(pointclouds_to_interp):
        if pc_id in request_pointcloud_ids:
            sly.logger.info("Skip keypoint figure in upload")
            continue  # skip existing keypoints

        pos = Vector3d(float(res_coords[figure_idx][0]),
                       float(res_coords[figure_idx][1]),
                       float(res_coords[figure_idx][2]))
        rot = Vector3d(0, 0, float(res_coords[figure_idx][3]))
        dim = Cuboid3d.from_json(source_figure.geometry).dimensions
        geometry = Cuboid3d(pos, rot, dim)

        g.api.pointcloud.figure.create(pc_id,
                                       source_figure.object_id,
                                       geometry.to_json(),
                                       source_figure.geometry_type,
                                       track_id=g.track_id)

        sly.logger.info("Upload new figure")


def create_interpolated_figures(figures_ids, dataset_id):
    """
    :param figures_ids: list of figures IDs
    """
    assert len(figures_ids) > 1, "len figures < 2"

    requested_figures, request_pointcloud_ids, pointclouds_to_interp = \
        get_interpolation_figures(figures_ids, dataset_id)
    true_coords = get_coords(requested_figures)

    res_coords = interpolate_all(true_coords, pointclouds_to_interp, request_pointcloud_ids)
    upload_new_figures(res_coords, request_pointcloud_ids, pointclouds_to_interp, source_figure=requested_figures[0])


@g.my_app.callback("interpolate_figures_ids")
@sly.timeit
@send_error_data
def interpolate_figures_ids(api: sly.Api, task_id, context, state, app_logger):
    app_logger.debug("Input data", extra={"state": state})
    ds_id = state["dataset_id"]
    figures_ids = state["figures_ids"]
    g.track_id = state["track_id"]
    create_interpolated_figures(figures_ids, ds_id)
    g.my_app.send_response(context["request_id"], data={"results": 1})


def test_run():
    request_figures_id = [56655589, 56655590, 56655621, 56655596]
    dataset = g.api.dataset.get_list(g.project_id)[0]
    create_interpolated_figures(request_figures_id, dataset_id=dataset.id)


if __name__ == "__main__":
    g.my_app.run()

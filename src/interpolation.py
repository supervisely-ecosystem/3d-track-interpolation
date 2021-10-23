import numpy as np
from scipy import interpolate
from scipy.spatial.transform import Rotation, Slerp


# TODO: Bézier Splines
# TODO: Kalman filter interpolation !!!!
# TODO: Curve Fitting


def _interpolate_rotation(x, yaw):
    rot_mat = np.zeros((yaw.size, 3))
    rot_mat[:, 2] = yaw

    rots = Rotation.from_rotvec(rot_mat)
    slerp = Slerp(x, rots)

    def get_z(q):
        return slerp(q).as_rotvec()[2]

    return get_z


def _interpolation_univariate_spline(x, y):
    """
        linear if 2 points. quadratic spline if 3 points, else cubic spline
    :return:
    """
    k = len(x) - 1
    return interpolate.InterpolatedUnivariateSpline(x, y, k=k if k < 4 else 3)


def _const_interp(x, y):
    def const_return(q):
        return y[0]

    return const_return


def get_coords(figures):
    """
    :returns ndarray ([[x,y,z,yaw],[x,y,z,yaw],...]])
    """
    coords = []
    for fig in figures:
        pos = fig.geometry['position']
        coords.append([pos['x'], pos['y'], pos['z'], fig.geometry['rotation']['z']])
    return np.asarray(coords)


def create_space(x, pointclouds_to_interp, request_pointcloud_ids):
    time = np.arange(len(pointclouds_to_interp))
    x_in_time = []
    for i, pc_id in enumerate(request_pointcloud_ids):
        x_in_time.append([pointclouds_to_interp.index(pc_id), x[i]])
    x_time, x_in_time = np.asarray(x_in_time).T
    iterp_f = _interpolation_univariate_spline(x_time, x_in_time)
    space = np.asarray([iterp_f(x) for x in time])
    return space


def interpolate_all(coords, pointclouds_to_interp, request_pointcloud_ids,
                    xy_interp_method=_interpolation_univariate_spline,
                    xz_interp_method=_interpolation_univariate_spline,
                    rot_interp_method=_interpolate_rotation):
    """
    Interpolate all values.
    If x is decreasing - order will be inverted
    If std(y) >= std(x):
    Uniformly accelerated motion is implied.
    :return: ndarray: [[x,y,z,yaw][x,y,z,yaw][x,y,z,yaw]]
    """
    x, y, z, yaw = coords.T

    swap = False
    if np.std(np.abs(y)) >= np.std(np.abs(x)):
        x, y = y, x
        swap = True

    reverse = False
    if not np.all(np.diff(x) > 0):  # not monotonically increasing
        x, y, z, yaw = x[::-1], y[::-1], z[::-1], yaw[::-1]  # reverse
        assert np.all(np.diff(x) > 0), "Both axis not monotonic"
        reverse = True

    if np.std(x) == 0:
        xy_interp_method = _const_interp
        xz_interp_method = _const_interp

    x_space = create_space(x, pointclouds_to_interp, request_pointcloud_ids)

    xy_interp_f = xy_interp_method(x, y)
    xy_coords = np.asarray([(k, xy_interp_f(k)) for k in x_space])
    if swap:
        xy_coords = np.flip(xy_coords, axis=1)

    z_interp_f = xz_interp_method(x, z)
    z_coords = np.asarray([z_interp_f(k) for k in x_space])

    yaw_interp_f = rot_interp_method(x, yaw)
    yaw_coords = np.asarray([yaw_interp_f(k) for k in x_space])

    res = np.column_stack((xy_coords, z_coords, yaw_coords))
    res = res if not reverse else np.flip(res, axis=0)
    return res


def plot(true_coords, res_coords):
    x0, y0, z0, yaw0 = true_coords.T
    x, y, z, yaw = res_coords.T
    import matplotlib.pyplot as plt
    plt.plot(x, y)
    plt.plot(x0, y0, '*')
    plt.savefig('plots/xy_InterpolatedUnivariateSplinek_LINEAR.png')

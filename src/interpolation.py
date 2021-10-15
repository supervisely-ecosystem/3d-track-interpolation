import numpy as np
from scipy import interpolate


# TODO: acceleration
# TODO: rotation according track
# TODO: Bézier Splines
# TODO: Kalman filter interpolation !!!!
# TODO: Curve Fitting

def _interpolation_default(x, y):
    """
    Available:
        ‘linear’, ‘nearest’, ‘nearest-up’, ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’, ‘previous’, ‘next’
    """
    return interpolate.interp1d(x, y, 'linear')


def _interpolation_cubic(x, y):
    return interpolate.interp1d(x, y, 'cubic')


def _interpolation_univariate_spline(x, y):
    """
        linear if 2 points. quadratic spline if 3 points, else cubic spline
    :return:
    """
    k = len(x) - 1
    return interpolate.InterpolatedUnivariateSpline(x, y, k=k if k < 4 else 3)


def get_coords(figures):
    """
    :returns ndarray ([[x,y,z,yaw],[x,y,z,yaw],...]])
    """
    coords = []
    for fig in figures:
        pos = fig.geometry['position']
        coords.append([pos['x'], pos['y'], pos['z'], fig.geometry['rotation']['z']])
    return np.asarray(coords)


def interpolate_all(coords, track_len,
                    xy_interp_method=_interpolation_univariate_spline,
                    xz_interp_method=_interpolation_univariate_spline,
                    rot_interp_method=_interpolation_univariate_spline):
    """
    Simple straight forward interpolation.
    Uniformly accelerated motion is implied.
    :return: ndarray: [[x,y,z,yaw][x,y,z,yaw][x,y,z,yaw]]
    """
    x, y, z, yaw = coords.T

    x_space = np.linspace(x[0], x[-1], track_len)
    xy_interp_f = xy_interp_method(x, y)
    xy_coords = np.asarray([(x, xy_interp_f(x)) for x in x_space])

    z_interp_f = xz_interp_method(x, z)
    z_coords = np.asarray([z_interp_f(x) for x in x_space])

    yaw_interp_f = rot_interp_method(x, yaw)
    yaw_coords = np.asarray([yaw_interp_f(x) for x in x_space])

    return np.column_stack((xy_coords, z_coords, yaw_coords))


def plot(true_coords, res_coords):
    x0, y0, z0, yaw0 = true_coords.T
    x, y, z, yaw = res_coords.T
    import matplotlib.pyplot as plt
    plt.plot(x, y)
    plt.plot(x0, y0, '*')
    plt.savefig('plots/xy_InterpolatedUnivariateSplinek_LINEAR.png')

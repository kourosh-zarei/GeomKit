import numpy as np


def distance(*args):
    return np.sqrt(sum(arg**2 for arg in args))


def pol_to_cart(r, incl, azim):
    x = r * np.sin(np.radians(incl)) * np.cos(np.radians(azim))
    y = r * np.sin(np.radians(incl)) * np.sin(np.radians(azim))
    z = r * np.cos(np.radians(incl))
    return x, y, z


def cart_to_pol(x, y, z):
    r = np.sqrt(x**2 + y**2 + z**2)
    incl = np.degrees(np.arccos(z / r))
    azim = np.degrees(np.arctan2(y, x))
    return [r, incl, azim]


def flatten(*args):
    result = []
    for arg in args:
        if isinstance(arg, list) or isinstance(arg, tuple):
            result.extend(flatten(*arg))
        else:
            result.append(arg)
    return result


def printer(*args):
    return args

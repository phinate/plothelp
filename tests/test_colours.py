from __future__ import annotations

from jax import config
from matplotlib.colors import to_rgb

from plothelp import linear_fade, linear_fade_2D

# precision
config.update("jax_enable_x64", True)


def test_linear_fade():
    c1 = "red"
    c2 = "blue"
    num_points = 10
    res = linear_fade(c1, c2, num_points)
    assert res.shape == (num_points, 3)
    red = list(to_rgb(c1))
    blue = list(to_rgb(c2))
    assert res[0].tolist() == red
    assert res[-1].tolist() == blue

    c1 = (1, 0, 0)
    c2 = (0, 0, 1)
    res = linear_fade(c1, c2, num_points)
    assert res.shape == (num_points, 3)
    assert res[0].tolist() == red
    assert res[-1].tolist() == blue

    c1 = (1, 0, 0, 1)
    c2 = (0, 0, 1, 1)
    res = linear_fade(c1, c2, num_points)
    assert res.shape == (num_points, 3)
    assert res[0].tolist() == red
    assert res[-1].tolist() == blue


def test_linear_fade_2D():
    c1 = "red"
    c2 = "blue"
    c3 = "green"
    c4 = "yellow"
    grid_size = (10, 10)
    res = linear_fade_2D(c1, c2, c3, c4, grid_size)
    red = list(to_rgb(c1))
    blue = list(to_rgb(c2))
    green = list(to_rgb(c3))
    yellow = list(to_rgb(c4))
    assert res.shape == (grid_size[0], grid_size[1], 3)
    assert res[0, 0].tolist() == red
    assert res[-1, -1].tolist() == yellow
    assert res[0, -1].tolist() == blue
    assert res[-1, 0].tolist() == green

    c1 = (1, 0, 0)
    c2 = (0, 0, 1)
    c3 = (0, 1, 0)
    c4 = (1, 1, 0)
    res = linear_fade_2D(c1, c2, c3, c4, grid_size)
    assert res.shape == (grid_size[0], grid_size[1], 3)
    assert res[0, 0].tolist() == list(c1)
    assert res[-1, -1].tolist() == list(c4)
    assert res[0, -1].tolist() == list(c2)
    assert res[-1, 0].tolist() == list(c3)

    c1 = (1, 0, 0, 1)
    c2 = (0, 0, 1, 1)
    c3 = (0, 1, 0, 1)
    c4 = (1, 1, 0, 1)
    res = linear_fade_2D(c1, c2, c3, c4, grid_size)
    assert res.shape == (grid_size[0], grid_size[1], 3)
    assert res[0, 0].tolist() == list(c1[:-1])
    assert res[-1, -1].tolist() == list(c4[:-1])
    assert res[0, -1].tolist() == list(c2[:-1])
    assert res[-1, 0].tolist() == list(c3[:-1])

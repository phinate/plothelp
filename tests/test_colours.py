from __future__ import annotations

from plothelp import linear_fade, linear_fade_2D


def test_linear_fade():
    c1 = "red"
    c2 = "blue"
    num_points = 10
    res = linear_fade(c1, c2, num_points)
    assert res.shape == (num_points, 3)

    c1 = (1, 0, 0)
    c2 = (0, 0, 1)
    num_points = 10
    res = linear_fade(c1, c2, num_points)
    assert res.shape == (num_points, 3)

    c1 = (1, 0, 0, 1)
    c2 = (0, 0, 1, 1)
    num_points = 10
    res = linear_fade(c1, c2, num_points)
    assert res.shape == (num_points, 3)


def test_linear_fade_2D():
    c1 = "red"
    c2 = "blue"
    c3 = "green"
    c4 = "yellow"
    grid_size = (10, 10)
    res = linear_fade_2D(c1, c2, c3, c4, grid_size)
    assert res.shape == (grid_size[0], grid_size[1], 3)

    c1 = (1, 0, 0)
    c2 = (0, 0, 1)
    c3 = (0, 1, 0)
    c4 = (1, 1, 0)
    grid_size = (10, 10)
    res = linear_fade_2D(c1, c2, c3, c4, grid_size)
    assert res.shape == (grid_size[0], grid_size[1], 3)

    c1 = (1, 0, 0, 1)
    c2 = (0, 0, 1, 1)
    c3 = (0, 1, 0, 1)
    c4 = (1, 1, 0, 1)
    grid_size = (10, 10)
    res = linear_fade_2D(c1, c2, c3, c4, grid_size)
    assert res.shape == (grid_size[0], grid_size[1], 3)

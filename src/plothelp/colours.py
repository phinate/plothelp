from __future__ import annotations

__all__ = ("linear_fade", "linear_fade_2D")

from functools import partial
from typing import Tuple, Union

import jax.numpy as jnp
from jax import vmap
from matplotlib.colors import to_rgb

color = Union[str, Tuple[float, float, float], Tuple[float, float, float, float]]


def linear_fade(c1: color, c2: color, num_points: int) -> jnp.ndarray:
    start = jnp.array(to_rgb(c1))
    end = jnp.array(to_rgb(c2))
    interp = vmap(partial(jnp.linspace, num=num_points))
    return interp(start, end).T


def linear_fade_2D(
    c1: color, c2: color, c3: color, c4: color, grid_size: tuple[int, int]
) -> jnp.ndarray:
    start = jnp.array(to_rgb(c1))
    end = jnp.array(to_rgb(c3))
    across = grid_size[0]
    interp = vmap(partial(jnp.linspace, num=across))
    res1 = interp(start, end)
    start = jnp.array(to_rgb(c2))
    end = jnp.array(to_rgb(c4))
    res2 = interp(start, end)
    down = grid_size[1]
    # interpolate between res1 and res2 along the down axis
    interp = vmap(partial(jnp.linspace, num=down))
    return interp(res1, res2).T

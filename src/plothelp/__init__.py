"""
Copyright (c) 2022 Nathan . All rights reserved.

plothelp: Simple auto-grid pyplot util.
"""


from __future__ import annotations

from plothelp.colours import linear_fade, linear_fade_2D
from plothelp.plot import autogrid

from ._version import version as __version__

__all__ = ("__version__", "autogrid", "linear_fade", "linear_fade_2D")

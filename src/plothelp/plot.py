from __future__ import annotations

__all__ = ("autogrid",)

import sys
from typing import Any, Sequence

if sys.version_info < (3, 8):
    from typing_extensions import Protocol
else:
    from typing import Protocol

import matplotlib.pyplot as plt


class PlotCallable(Protocol):
    def __call__(self, current_plot: dict[str, Any], *args: Any, **kwargs: Any) -> None:
        ...


def autogrid(
    data: Sequence[Any],
    plot_func: PlotCallable,
    plot_func_kwargs: dict[str, Any] | None = None,
    subplot_kwargs: dict[str, Any] | None = None,
    title: str | None = None,
    plots_per_row: int | None = None,
    figsize_scale: float = 2.0,
    outfile_name: str | None = None,
    tight_layout: bool = True,
    flip_size: bool = False,
) -> plt.Figure:
    """Utility function to visualize `plot_func` over an iterable set of `data`.

    Args:
        data: An iterable set of data to visualize.
        plot_func: A function that takes a `dict` as the first arg, which contains the
            current data element `"data"`, the current axis `"ax"`, and the current
            index `"i"`, then modifies the axis in place. The function should not
            return anything (it won't be used even if so).
            Also optionally takes extra keyword arguments that are unpacked from the
            `plot_func_kwargs` dict.
        plot_func_kwargs: A dictionary of keyword arguments to pass to `plot_func`.
        subplot_kwargs: Keyword arguments to pass to `plt.subplots`.
        title: Title to use for the figure.
        plots_per_row: Number of plots to show per row (if None, will attempt to
            guess based on the number of data elements).
        figsize_scale: Factor to scale the figure size by.
        outfile_name: If not None, save the figure to this file.

    Returns:
        The figure object.
    """
    # automatically select the number of plots per row to minimise blank plots
    length = len(data)
    if plots_per_row is None:
        if length == 1:
            plots_per_row = 1
        else:
            if length < 3:
                i = 2
            else:
                i = 3
            rem_dict = {}
            while (length % i != 0) and i < 10:
                rem_dict[i] = length % i
                i += 1
            if i < 10:
                plots_per_row = i
            else:
                plots_per_row = max(rem_dict, key=rem_dict.get)  # type: ignore[arg-type]
                # (https://github.com/python/mypy/issues/6692) ?

    rem = length % plots_per_row
    if rem == 0:
        rows = int(length / plots_per_row)
    else:
        rows = int(length / plots_per_row) + 1
    if subplot_kwargs is None:
        subplot_kwargs = {}
    if plot_func_kwargs is None:
        plot_func_kwargs = {}

    if "figsize" not in subplot_kwargs:
        if flip_size:
            subplot_kwargs["figsize"] = [
                rows * figsize_scale,
                plots_per_row * figsize_scale,
            ]
        else:
            subplot_kwargs["figsize"] = [
                plots_per_row * figsize_scale,
                rows * figsize_scale,
            ]
    if "dpi" not in subplot_kwargs:
        subplot_kwargs["dpi"] = 120

    if flip_size:
        fig, axes = plt.subplots(nrows=plots_per_row, ncols=rows, **subplot_kwargs)
    else:
        fig, axes = plt.subplots(nrows=rows, ncols=plots_per_row, **subplot_kwargs)

    row = 0
    column = 0
    axes_ravel = axes.ravel()
    for i, datum in enumerate(data):
        if i % plots_per_row == 0 and i != 0:
            row += 1
            column -= plots_per_row

        # plotting callback
        ax = axes_ravel[i]
        plot_func(dict(ax=ax, data=datum, i=i), **plot_func_kwargs)

        column += 1

    if rows > 1:
        while column % plots_per_row != 0:
            fig.delaxes(axes[row, column])
            column += 1
    if title is not None:
        plt.suptitle(title)
    if tight_layout:
        plt.tight_layout()
        if outfile_name is not None:
            plt.savefig(outfile_name, bbox_inches="tight")
    else:
        if outfile_name is not None:
            plt.savefig(outfile_name)
    return fig

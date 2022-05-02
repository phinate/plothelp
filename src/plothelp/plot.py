from __future__ import annotations

__all__ = ("autoplot",)

from typing import Any, Callable, Iterable, Sequence

import matplotlib.pyplot as plt


def autoplot(
    data: Sequence[Any],
    plot_func: Callable[[Any, Iterable[Any], int], None],
    subplot_kwargs: dict[str, Any] | None = None,
    title: str | None = None,
    plots_per_row: int | None = None,
    figsize_scale: float = 2.0,
    outfile_name: str | None = None,
) -> plt.Figure:
    """Utility function to visualize `plot_func` over an iterable set of `data`.

    Args:
        data: An iterable set of data to visualize.
        plot_func: A function that takes a single data element, the current index, and
            the current axis, then modifies the axis in place.
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
    plt.rc(
        "figure",
        figsize=[plots_per_row * figsize_scale, rows * figsize_scale],
        facecolor="w",
    )
    if subplot_kwargs is None:
        subplot_kwargs = {}
    fig, axes = plt.subplots(nrows=rows, ncols=plots_per_row, dpi=120, **subplot_kwargs)

    row = 0
    column = 0

    for i, datum in enumerate(data):
        if i % plots_per_row == 0 and i != 0:
            row += 1
            column -= plots_per_row

        # plotting callback
        ax = axes[row, column]
        plot_func(ax, datum, i)

        column += 1

    while column % plots_per_row != 0:
        fig.delaxes(axes[row, column])
        column += 1
    if title is not None:
        plt.suptitle(title)
    plt.tight_layout()
    if outfile_name is not None:
        plt.savefig(outfile_name, bbox_inches="tight")
    return fig

from __future__ import annotations

import plothelp


def test_autoplot():
    data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]

    def plot_func(ax, data, i):
        ax.plot(data, i)

    plothelp.autoplot(
        data,
        plot_func=plot_func,
        title="Test",
    )

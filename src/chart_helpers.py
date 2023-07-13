import matplotlib.pyplot as plt
import numpy as np
from scipy.stats.kde import gaussian_kde


def make_histogram(
    data, title, bin_count=1000, cumulative=False, fig_num=None, alpha=1, label=None
):
    if fig_num is None:
        plt.figure()
    else:
        plt.figure(fig_num)
    n, bins, patches = plt.hist(
        data,
        histtype="stepfilled",
        bins=bin_count,
        cumulative=cumulative,
        density=True if cumulative else False,
        alpha=alpha,
        label=label,
    )

    if not isinstance(data[0], np.ndarray):
        data = [data]

    for idx, datum in enumerate(data):
        try:
            kde = gaussian_kde(datum)
            dist_space = np.linspace(min(datum), max(datum), len(bins))
            if cumulative is False:
                line = plt.plot(dist_space, kde(bins) * n.sum(), label="Gaussian graph")
            else:
                y = kde(bins)
                y = np.cumsum(y)
                y = np.interp(y, (y.min(), y.max()), (0, 1))
                line = plt.plot(dist_space, y, label="Gaussian graph" if label is None
                                else f"{label[idx]} (Gaussian)")
            line = line[0].get_xydata()
        except Exception as e:
            print(f"Failed to make gaussian KDE: {e}")
        # print(line)

    plt.title(title)
    plt.xlabel("Pulls")
    plt.ylabel("Probablity" if cumulative else "Frequency")
    # if label:
    ax = plt.gcf().axes[0]
    ax.legend(prop={"size": 10})

    return n, bins, label


def make_bar(bins, values, title, labels=[]):
    if not isinstance(values[0], np.ndarray):
        values = [values]

    if not labels:
        labels = [None]

    plt.figure()
    # creating the bar plot
    for value, label in zip(values, labels):
        pulls = bins[: len(value)]
        plt.bar(pulls, (value * 100) / pulls, label=label)
    plt.xlabel("Pulls")
    plt.ylabel("Probability per pull")
    plt.title(title)
    if labels[0] is not None:
        ax = plt.gcf().axes[0]
        ax.legend(prop={"size": 10})

"""Visualisation helpers for the available-workers example."""
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

col_available = "#00b050"
col_unavailable = "#a6a6a6"
col_task = "#0060a8"


def draw_assignment(worked_on_by, available, ax=None, title=None):
    """Draw workers (top) and tasks (bottom) with a line for every assignment.

    worked_on_by: dict task -> set of workers, e.g. {1: {2, 4}, 2: {5}, 3: {6}}
    available:    dict worker -> bool
    """
    workers = sorted(available)
    tasks = sorted(worked_on_by)
    if ax is None:
        _, ax = plt.subplots(figsize=(1.5 * len(workers) + 1.5, 4.5))

    width = max(len(workers), len(tasks)) - 1
    wx = {w: i * width / max(len(workers) - 1, 1) for i, w in enumerate(workers)}
    tx = {t: (i + 0.5) * width / len(tasks) for i, t in enumerate(tasks)}
    y_workers, y_tasks = 2.0, 0.0

    # assignments
    for t in tasks:
        for w in worked_on_by[t]:
            color = col_available if available[w] else "#d00000"
            style = "-" if available[w] else "--"
            ax.plot([wx[w], tx[t]], [y_workers - 0.12, y_tasks + 0.12],
                    color=color, linewidth=2, linestyle=style, zorder=1)

    # workers
    for w in workers:
        ax.add_patch(Circle((wx[w], y_workers), 0.13, zorder=2,
                            facecolor=col_available if available[w] else col_unavailable,
                            edgecolor="black"))
        ax.text(wx[w], y_workers, str(w), color="white", fontweight="bold",
                ha="center", va="center", zorder=3)
        ax.text(wx[w], y_workers + 0.22, "available" if available[w] else "not available",
                ha="center", fontsize=7, color="black" if available[w] else "#7f7f7f")

    # tasks
    for t in tasks:
        ax.add_patch(FancyBboxPatch((tx[t] - 0.3, y_tasks - 0.11), 0.6, 0.22, zorder=2,
                                    boxstyle="round,pad=0.02",
                                    facecolor=col_task, edgecolor="black"))
        ax.text(tx[t], y_tasks, f"Task {t}", color="white", fontweight="bold",
                ha="center", va="center", fontsize=9, zorder=3)

    ax.text(-0.6, y_workers, "Workers", ha="right", va="center", fontsize=10)
    ax.text(-0.6, y_tasks, "Tasks", ha="right", va="center", fontsize=10)
    ax.set_xlim(-1.6, width + 0.4)
    ax.set_ylim(-0.35, y_workers + 0.45)
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title)
    return ax

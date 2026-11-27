"""Visualisation helpers for the harbour (ship assignment) example."""
import math

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

# x-range of each dock (berth) in the pier
dock_x = {1: (0.8, 3.6), 2: (4.4, 7.6), 3: (8.4, 11.2)}
pier_bottom, berth_top, pier_top = 0.0, 3.0, 4.6
water = "#d6ecfa"

# one colour per boat, so boats can be told apart across plots
boat_colors = {1: "#1f3b57", 2: "#6b3e26", 3: "#2f5d50", 4: "#4a4a8a", 5: "#7a7a7a"}


def _draw_boat(ax, x, y, number, width=1.1):
    """Draw a small ship centred at (x, y) with its number on the hull."""
    h = width * 0.32
    hull = [(x - width / 2, y + h / 2), (x + width / 2, y + h / 2),
            (x + width * 0.38, y - h / 2), (x - width * 0.38, y - h / 2)]
    ax.add_patch(Polygon(hull, closed=True, facecolor=boat_colors.get(number, "black"),
                         edgecolor="black", linewidth=1))
    ax.add_patch(Rectangle((x - width * 0.18, y + h / 2), width * 0.36, h * 0.8,
                           facecolor="#d9d9d9", edgecolor="black", linewidth=1))
    ax.text(x, y, str(number), color="white", fontweight="bold",
            ha="center", va="center", fontsize=10)


def draw_harbour(solution, ax=None, title=None):
    """Draw the pier with all boats in their docks.

    `solution` maps boat number -> dock number, e.g. {1: 2, 2: 3, 3: 1, 4: 1, 5: 2}.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(7, 3.2))

    # water in front of the pier
    ax.add_patch(Rectangle((-0.2, pier_bottom - 0.6), 12.4, 0.6, facecolor=water, edgecolor="none"))
    # pier: grey block, docks are berths (water) cut out from below
    ax.add_patch(Rectangle((0, pier_bottom), 12, pier_top - pier_bottom,
                           facecolor="#bfbfbf", edgecolor="black", linewidth=1.5))
    for d, (x0, x1) in dock_x.items():
        ax.add_patch(Rectangle((x0, pier_bottom - 0.02), x1 - x0, berth_top - pier_bottom + 0.02,
                               facecolor=water, edgecolor="none"))
        ax.plot([x0, x0, x1, x1], [pier_bottom, berth_top, berth_top, pier_bottom],
                color="black", linewidth=1.5)
        ax.text((x0 + x1) / 2, berth_top + 0.3, f"Dock {d}", ha="center", fontsize=10)
    ax.text(6, pier_top - 0.45, "Docks", ha="center", fontsize=12, fontweight="bold")

    # boats: up to 2 per row inside a berth, filled from the top
    for d, (x0, x1) in dock_x.items():
        boats = sorted(b for b, dock in solution.items() if dock == d)
        for i, b in enumerate(boats):
            row, col = divmod(i, 2)
            x = x0 + (x1 - x0) * (0.26 + 0.48 * col)
            y = berth_top - 0.6 - 0.95 * row
            _draw_boat(ax, x, y, b, width=1.3)

    ax.set_xlim(-0.2, 12.2)
    ax.set_ylim(pier_bottom - 0.6, pier_top + 0.2)
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title)
    return ax


def draw_all(solutions, cols=3):
    """Draw a list of solutions as a grid of small harbour plots."""
    n = len(solutions)
    rows = math.ceil(n / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 2.4 * rows), squeeze=False)
    for i, ax in enumerate(axes.flat):
        if i < n:
            draw_harbour(solutions[i], ax=ax, title=f"Solution {i + 1}")
        else:
            ax.axis("off")
    fig.tight_layout()
    return fig

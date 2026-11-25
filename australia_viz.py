"""Visualisation helpers for the Australia map colouring example."""
import math

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# colours as in the lecture slides
fill = {"blue": "#0060a8", "green": "#00b050", "red": "#c00000"}

# simplified region outlines (x to the right, y downwards);
# neighbouring regions share edges exactly as in the border constraints
shapes = {
    "WA":  [(40, 110), (150, 40), (150, 250), (130, 270), (40, 285), (20, 200)],
    "NT":  [(150, 40), (240, 40), (240, 150), (150, 150)],
    "SA":  [(150, 150), (260, 150), (260, 320), (230, 300), (150, 250)],
    "QL":  [(240, 40), (290, 10), (330, 60), (370, 140), (380, 200),
            (260, 200), (260, 150), (240, 150)],
    "NSW": [(260, 200), (380, 200), (370, 270), (330, 290), (260, 280)],
    "VT":  [(260, 280), (330, 290), (310, 330), (260, 320)],
}
label_pos = {"WA": (85, 180), "NT": (195, 100), "SA": (205, 215),
             "QL": (315, 140), "NSW": (315, 245), "VT": (290, 308)}


def draw_map(solution, ax=None, title=None):
    """Draw the map with every region filled in its colour from `solution`
    (a dict like {"WA": "green", "NT": "blue", ...})."""
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 5))
    for r, points in shapes.items():
        ax.add_patch(Polygon(points, closed=True, facecolor=fill[solution[r]],
                             edgecolor="black", linewidth=2, joinstyle="round"))
        lx, ly = label_pos[r]
        ax.text(lx, ly, r, color="white", fontweight="bold", ha="center", va="center",
                fontsize=9 if r == "VT" else 14)
    ax.set_xlim(10, 390)
    ax.set_ylim(340, 0)   # flip y so the north is at the top
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title)
    return ax


def draw_all(solutions, cols=3):
    """Draw a list of solutions as a grid of small maps."""
    n = len(solutions)
    rows = math.ceil(n / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 3.4 * rows), squeeze=False)
    for i, ax in enumerate(axes.flat):
        if i < n:
            draw_map(solutions[i], ax=ax, title=f"Solution {i + 1}")
        else:
            ax.axis("off")
    fig.tight_layout()
    return fig

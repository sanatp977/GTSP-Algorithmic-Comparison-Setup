# displayingCases.py

import json
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.widgets import Button
import os

# Path to tsp_cases.json (outside the 'codes' folder)
JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "tsp_cases.json")

# Load data
with open(JSON_PATH, "r") as f:
    cases = json.load(f)

NUM_COLORS = max(len(case[2]) for case in cases)
colors = cm.get_cmap('tab20', NUM_COLORS)

# Prepare labels
case_labels = [
    f"Goods: {len(city_class)}, Cities: {len(city_position)}"
    for city_position, goods_class, city_class in cases
]

current_index = [0]  # Use list so we can mutate inside button callbacks

# --- Plotting logic ---
def plot_case(index):
    ax.clear()  # clear the axes properly

    city_position, goods_class, city_class = cases[index]
    x = [pos[0] for pos in city_position]
    y = [pos[1] for pos in city_position]

    # Collect points by goods class
    class_points = {}
    for i, (xi, yi) in enumerate(zip(x, y)):
        g = goods_class[i]
        if g not in class_points:
            class_points[g] = []
        class_points[g].append((xi, yi, i))

    # Plot points ordered by goods class
    for g in sorted(class_points.keys()):
        x_vals = [p[0] for p in class_points[g]]
        y_vals = [p[1] for p in class_points[g]]
        ax.scatter(x_vals, y_vals, color=colors(g), label=f"Good {g + 1}", s=80)
        for xi, yi, idx in class_points[g]:
            ax.text(xi + 0.5, yi + 0.5, str(idx), fontsize=9)

    ax.set_title(f"Test Case #{index + 1}: {case_labels[index]}")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.legend(title="Goods Classes", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Dynamically adjust limits with a margin
    margin = 2
    ax.set_xlim(min(x) - margin, max(x) + margin)
    ax.set_ylim(min(y) - margin, max(y) + margin)

    plt.tight_layout()
    plt.draw()


# --- Buttons ---
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.12, right=0.75)
plot_case(current_index[0])

# Button axes
# Make these larger if required to clearly show previous and next button
axprev = plt.axes([0.35, 0.0002, 0.06, 0.005])  # [left, bottom, width, height]
axnext = plt.axes([0.55, 0.0002, 0.06, 0.005])

bprev = Button(axprev, 'Previous')
bnext = Button(axnext, 'Next')

# Button handlers
def next_case(event):
    if current_index[0] < len(cases) - 1:
        current_index[0] += 1
        plot_case(current_index[0])

def prev_case(event):
    if current_index[0] > 0:
        current_index[0] -= 1
        plot_case(current_index[0])

bnext.on_clicked(next_case)
bprev.on_clicked(prev_case)

plt.show()

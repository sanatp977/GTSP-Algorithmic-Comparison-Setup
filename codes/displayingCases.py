# displayingCases.py

import json
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.widgets import Slider
import os

# Path to tsp_cases.json (go up one folder)
JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "tsp_cases.json")

# Load the data
with open(JSON_PATH, "r") as f:
    cases = json.load(f)

# Set up color map
NUM_COLORS = max(len(case[2]) for case in cases)
colors = cm.get_cmap('tab20', NUM_COLORS)

# Precompute label for each case
case_labels = [
    f"Goods: {len(city_class)}, Cities: {len(city_position)}"
    for city_position, goods_class, city_class in cases
]

# Plot a single test case
def plot_case(index):
    plt.clf()
    city_position, goods_class, city_class = cases[index]
    x = [pos[0] for pos in city_position]
    y = [pos[1] for pos in city_position]
    
    for i, (xi, yi) in enumerate(zip(x, y)):
        g = goods_class[i]
        plt.scatter(xi, yi, color=colors(g), s=80, label=f"Good {g}" if f"Good {g}" not in plt.gca().get_legend_handles_labels()[1] else "")
        plt.text(xi + 0.5, yi + 0.5, str(i), fontsize=9)
    
    plt.title(f"Test Case #{index + 1}: {case_labels[index]}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.legend(title="Goods Classes", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.draw()

# Initial plot
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2, right=0.75)
plot_case(0)

# Slider
ax_slider = plt.axes([0.15, 0.05, 0.7, 0.03])
slider = Slider(ax_slider, 'Case Index', 0, len(cases) - 1, valinit=0, valstep=1)

def update(val):
    plot_case(int(slider.val))

slider.on_changed(update)

plt.show()

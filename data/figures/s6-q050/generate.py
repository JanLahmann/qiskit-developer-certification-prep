# Stem figure for s6-q050: raw ZNE estimates at noise factors 1, 3, 5. The
# proof-free (conceptual) question keys on the linear fit through exactly
# these POINTS; the assert checks they are collinear (slope -0.08,
# intercept 0.70) so the drawn data and the explanation cannot drift apart.
# Runs under pipeline/render_figures.py's deterministic prelude.
import matplotlib.pyplot as plt
import numpy as np

POINTS = ((1, 0.62), (3, 0.46), (5, 0.30))
x = np.array([p[0] for p in POINTS], dtype=float)
y = np.array([p[1] for p in POINTS])
slope, intercept = np.polyfit(x, y, 1)
assert abs(slope + 0.08) < 1e-9 and abs(intercept - 0.70) < 1e-9, (slope, intercept)

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(x, y, "ko", markersize=8)
for xi, yi in POINTS:
    ax.annotate(f"{yi:.2f}", (xi, yi), textcoords="offset points", xytext=(8, 6))
ax.set_xlim(-0.5, 6)
ax.set_ylim(0.0, 1.0)
ax.set_xticks([0, 1, 2, 3, 4, 5, 6])
ax.set_xlabel("noise factor")
ax.set_ylabel("raw expectation value")
ax.grid(True, linewidth=0.4, color="0.8")
fig.savefig("s6-q050-stem.svg")

# Figure for s4-q047: the STEM diagram. Hand-drawn with matplotlib primitives
# (no Qiskit rendering involved) so that the picture shows the PAIRING and not
# an implementation detail: a column of observables, a row of parameter-value
# sets, and the grid of expectation values they produce. The proof script runs
# an Estimator on exactly these shapes ((4, 1) observables x (1, 6) parameter
# values) and reports the resulting evs shape — keep the two in sync
# (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: everything is drawn from fixed coordinates.
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

CELL_W, CELL_H = 1.2, 0.8
COL_STEP, ROW_STEP = 1.3, 1.0
N_OBS, N_PAR = 4, 6


def box(ax, x, y, label, fill):
    ax.add_patch(Rectangle((x, y), CELL_W, CELL_H, facecolor=fill,
                           edgecolor="black", linewidth=1.0))
    ax.text(x + CELL_W / 2, y + CELL_H / 2, label,
            ha="center", va="center", fontsize=9)


fig, ax = plt.subplots(figsize=(7.6, 4.6))
ax.set_xlim(0, 3.0 + COL_STEP * N_PAR + 0.4)
ax.set_ylim(0, 2.2 + ROW_STEP * N_OBS + 1.6)
ax.set_aspect("equal")
ax.axis("off")

grid_x0 = 3.0
top = 1.6 + ROW_STEP * N_OBS
mid_x = grid_x0 + (COL_STEP * N_PAR - 0.1) / 2

for j in range(N_PAR):
    box(ax, grid_x0 + j * COL_STEP, top, f"$\\theta_{{{j + 1}}}$", "#e8e8e8")
ax.text(mid_x, top + CELL_H + 0.35, "parameter values (1, 6)",
        ha="center", va="bottom", fontsize=10)

for i in range(N_OBS):
    box(ax, 1.4, top - (i + 1) * ROW_STEP, f"$O_{{{i + 1}}}$", "#e8e8e8")
ax.text(1.1, top - ROW_STEP * N_OBS / 2 - 0.1, "observables (4, 1)",
        ha="center", va="center", rotation=90, fontsize=10)

for i in range(N_OBS):
    for j in range(N_PAR):
        box(ax, grid_x0 + j * COL_STEP, top - (i + 1) * ROW_STEP, "ev", "white")
ax.text(mid_x, 0.55, "expectation values (4, 6)",
        ha="center", va="center", fontsize=10)

fig.savefig("s4-q047-stem.svg")

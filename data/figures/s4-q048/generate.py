# Figure for s4-q048: the STEM diagram. Hand-drawn with matplotlib primitives
# (no Qiskit rendering involved) so the picture shows the PAIRING and not an
# implementation detail: five observables and five parameter-value sets meeting
# row by row, one expectation value per row. The proof script runs an Estimator
# on exactly these shapes ((5,) observables x (5,) parameter sets) and reports
# the resulting evs shape — keep the two in sync
# (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: everything is drawn from fixed coordinates.
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow, Rectangle

CELL_W, CELL_H = 1.2, 0.8
ROW_STEP = 1.1
N = 5
OBS_X, PAR_X, EV_X = 0.5, 3.9, 7.7


def box(ax, x, y, label, fill):
    ax.add_patch(Rectangle((x, y), CELL_W, CELL_H, facecolor=fill,
                           edgecolor="black", linewidth=1.0))
    ax.text(x + CELL_W / 2, y + CELL_H / 2, label,
            ha="center", va="center", fontsize=9)


fig, ax = plt.subplots(figsize=(8.8, 5.4))
ax.set_xlim(0, EV_X + CELL_W + 0.6)
ax.set_ylim(0, 1.0 + ROW_STEP * N + 0.9)
ax.set_aspect("equal")
ax.axis("off")

top = 1.0 + ROW_STEP * N

for i in range(N):
    y = top - (i + 1) * ROW_STEP
    box(ax, OBS_X, y, f"$O_{{{i + 1}}}$", "#e8e8e8")
    ax.text(OBS_X + CELL_W + 0.35, y + CELL_H / 2, "x", ha="center",
            va="center", fontsize=10)
    box(ax, PAR_X, y, f"$\\theta_{{{i + 1}}}$", "#e8e8e8")
    ax.add_patch(FancyArrow(PAR_X + CELL_W + 0.25, y + CELL_H / 2,
                            EV_X - PAR_X - CELL_W - 0.6, 0.0, width=0.03,
                            head_width=0.18, head_length=0.25,
                            length_includes_head=True, color="black"))
    box(ax, EV_X, y, "ev", "white")

ax.text(OBS_X + CELL_W / 2, top + 0.25, "observables (5,)", ha="center",
        va="bottom", fontsize=10)
ax.text(PAR_X + CELL_W / 2, top + 0.25, "parameter values (5,)", ha="center",
        va="bottom", fontsize=10)
ax.text(EV_X + CELL_W / 2, top + 0.25, "expectation values (5,)", ha="center",
        va="bottom", fontsize=10)

fig.savefig("s4-q048-stem.svg")

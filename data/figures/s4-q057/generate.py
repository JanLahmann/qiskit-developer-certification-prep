# Figure for s4-q057: the STEM diagram. Hand-drawn with matplotlib
# primitives — a schematic timeline of ONE session: job 1 and job 2 run with a
# short gap, then no job arrives for longer than the interactive TTL, and job 3
# is submitted while the maximum TTL window (started by job 1) is still open.
# The question is conceptual (scheduling cannot be executed locally; local
# testing mode ignores execution modes). Every feature drawn is stated in prose
# on guides/execution-modes ("Basic workflow": the max TTL timer starts with
# the first job and never pauses; the interactive TTL timer starts after each
# job; with no job inside it the workload is deactivated; a job can reactivate
# it before max TTL, but must go through the normal queue). Fetched 2026-10-01.
# Runs under pipeline/render_figures.py's deterministic prelude.
# Determinism: everything is drawn from fixed coordinates.
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

fig, ax = plt.subplots(figsize=(9.2, 3.4))
ax.set_xlim(0, 14.0)
ax.set_ylim(0, 5.2)
ax.axis("off")

Y_JOB = 1.6
H = 0.8


def job(x, w, label):
    ax.add_patch(Rectangle((x, Y_JOB), w, H, facecolor="#c6dbef",
                           edgecolor="black", linewidth=1.0))
    ax.text(x + w / 2, Y_JOB + H / 2, label, ha="center", va="center", fontsize=10)


def span(x1, x2, y, label, style="-"):
    ax.add_patch(FancyArrowPatch((x1, y), (x2, y), arrowstyle="<->",
                                 mutation_scale=10, linewidth=1.0,
                                 linestyle=style, color="black"))
    ax.text((x1 + x2) / 2, y + 0.15, label, ha="center", va="bottom", fontsize=9)


# Time axis.
ax.add_patch(FancyArrowPatch((0.3, 0.9), (13.8, 0.9), arrowstyle="->",
                             mutation_scale=12, linewidth=1.0, color="black"))
ax.text(13.8, 0.55, "time", ha="right", va="center", fontsize=9)

# Jobs.
job(1.0, 2.0, "job 1")
job(3.6, 2.0, "job 2")

# Short gap between job 1 and job 2 (inside the interactive TTL).
span(3.0, 3.6, Y_JOB + H + 0.25, "")

# Interactive TTL after job 2, then the idle stretch beyond it.
span(5.6, 7.4, Y_JOB + H + 0.25, "interactive TTL")
ax.plot([7.4, 7.4], [1.0, Y_JOB + H + 0.25], color="black", linewidth=0.8,
        linestyle=":")
ax.text(8.6, Y_JOB + H / 2, "no job", ha="center", va="center", fontsize=9,
        style="italic")

# Job 3 submitted later.
ax.add_patch(FancyArrowPatch((10.0, 0.25), (10.0, Y_JOB - 0.05), arrowstyle="->",
                             mutation_scale=12, linewidth=1.2, color="black"))
ax.text(10.0, 0.1, "job 3 submitted", ha="center", va="top", fontsize=9)

# Maximum TTL window started by job 1, still open at job 3.
span(1.0, 12.8, 4.35, "maximum TTL (starts when job 1 starts)", style="--")
ax.plot([1.0, 1.0], [Y_JOB + H, 4.35], color="black", linewidth=0.8, linestyle=":")
ax.plot([12.8, 12.8], [1.0, 4.35], color="black", linewidth=0.8, linestyle=":")

fig.savefig("s4-q057-stem.svg")

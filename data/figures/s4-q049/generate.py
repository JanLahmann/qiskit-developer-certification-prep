# Figure for s4-q049: the STEM diagram. Hand-drawn with matplotlib primitives —
# a schematic QPU timeline for a three-job workload. Every feature drawn is one
# the execution-modes guide states in prose (single queue entry for the whole
# workload; an active window in which the QPU is dedicated and exclusive; the
# interactive TTL gaps between consecutive jobs, during which the window is
# held; no other user's job and no calibration job inside the window). The
# question is conceptual — queueing semantics cannot be executed locally — so
# the drawing carries no Qiskit artifact and no invented numbers.
# Sources relied on: https://quantum.cloud.ibm.com/docs/guides/execution-modes
# and https://quantum.cloud.ibm.com/docs/guides/choose-execution-mode
# (fetched 2026-07-27).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: everything is drawn from fixed coordinates.
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow, Rectangle

BAR_H = 0.7
Y_WORK = 2.5   # the workload's lane
Y_OTHER = 1.2  # everybody else's lane

fig, ax = plt.subplots(figsize=(9.0, 3.9))
ax.set_xlim(0, 13.6)
ax.set_ylim(0, 5.0)
ax.axis("off")


def bar(x, w, y, label, fill, hatch=None, fontsize=9):
    ax.add_patch(Rectangle((x, y), w, BAR_H, facecolor=fill,
                           edgecolor="black", linewidth=1.0, hatch=hatch))
    ax.text(x + w / 2, y + BAR_H / 2, label, ha="center", va="center",
            fontsize=fontsize)


# Lane labels.
ax.text(0.0, Y_WORK + BAR_H / 2, "this workload", ha="left", va="center",
        fontsize=9)
ax.text(0.0, Y_OTHER + BAR_H / 2, "everyone else", ha="left", va="center",
        fontsize=9)

# One queue entry for the whole workload, then three jobs with idle gaps.
bar(2.2, 2.0, Y_WORK, "queue wait", "#d9d9d9")
bar(4.5, 1.7, Y_WORK, "job 1", "#9ec5e8")
bar(7.1, 1.7, Y_WORK, "job 2", "#9ec5e8")
bar(9.7, 1.7, Y_WORK, "job 3", "#9ec5e8")
for x in (6.65, 9.25):
    ax.text(x, Y_WORK + BAR_H / 2, "gap", ha="center", va="center", fontsize=8,
            style="italic")
ax.text(7.95, Y_WORK - 0.25, "gaps: QPU idle but still held for this workload",
        ha="center", va="top", fontsize=8, style="italic")

# The other lane stays empty for the whole active window.
ax.add_patch(Rectangle((4.5, Y_OTHER), 6.9, BAR_H, facecolor="white",
                       edgecolor="black", linewidth=1.0, linestyle="--"))
ax.text(7.95, Y_OTHER + BAR_H / 2,
        "no other job, no calibration job", ha="center", va="center",
        fontsize=8, style="italic")
bar(11.9, 1.2, Y_OTHER, "job", "#e8e8e8")

# Bracket over the active window.
ax.plot([4.5, 4.5, 11.4, 11.4], [3.6, 3.85, 3.85, 3.6], color="black",
        linewidth=1.0)
ax.text(7.95, 3.95, "active window: QPU dedicated to this workload",
        ha="center", va="bottom", fontsize=9)

# Time axis.
ax.add_patch(FancyArrow(2.2, 0.5, 11.2, 0.0, width=0.02, head_width=0.16,
                        head_length=0.28, length_includes_head=True,
                        color="black"))
ax.text(13.5, 0.3, "time", ha="right", va="top", fontsize=9)

fig.savefig("s4-q049-stem.svg")

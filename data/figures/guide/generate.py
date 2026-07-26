# Figures for the visual-literacy guide page (site/docs/visual-guide.mdx).
#
# This directory is NOT a question figure directory: pipeline/render_figures.py
# only walks questions, so this generator is run by hand from inside a scratch
# directory:
#
#     cd <scratch dir> && .venv/bin/python data/figures/guide/generate.py
#
# and the resulting guide-*.svg files are copied here. Determinism is the same
# contract as for question figures — no sampling, no timestamps — and is
# checked by rendering twice and diffing the bytes.
# build_site_data.py mirrors data/figures/** into site/static/img/bank/**, so
# these files are referenced from MDX as /img/bank/guide/guide-*.svg.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow, Rectangle

plt.rcParams["svg.hashsalt"] = "certiq"

_real_savefig = plt.Figure.savefig


def _savefig(self, fname, **kw):
    kw.setdefault("metadata", {"Date": None})
    kw.setdefault("bbox_inches", "tight")
    return _real_savefig(self, fname, **kw)


plt.Figure.savefig = _savefig

import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector
from qiskit.visualization import (plot_bloch_multivector, plot_histogram,
                                  plot_state_qsphere)

# ---------------------------------------------------------------------------
# 1. Circuit anatomy: registers, a barrier, a measurement arrow into the
#    classical wire, and an If/Else region driven by that classical bit.
# ---------------------------------------------------------------------------
qr = QuantumRegister(2, "q")
cr = ClassicalRegister(2, "c")
anatomy = QuantumCircuit(qr, cr)
anatomy.h(0)
anatomy.cx(0, 1)
anatomy.barrier()
anatomy.measure(0, 0)
with anatomy.if_test((cr[0], 1)) as else_:
    anatomy.z(1)
with else_:
    anatomy.x(1)
anatomy.measure(1, 1)
anatomy.draw(output="mpl").savefig("guide-circuit.svg")

# ---------------------------------------------------------------------------
# 2. Histogram: little-endian outcome labels, unequal bars.
# ---------------------------------------------------------------------------
hist_qc = QuantumCircuit(3)
hist_qc.ry(2 * np.pi / 3, 0)
hist_qc.cx(0, 1)
hist_qc.x(2)
counts = {str(k): round(v * 1000)
          for k, v in Statevector(hist_qc).probabilities_dict().items()}
plot_histogram(counts).savefig("guide-histogram.svg")

# ---------------------------------------------------------------------------
# 3. Bloch multivector: one sphere per qubit, direction carries the meaning.
# ---------------------------------------------------------------------------
bloch_qc = QuantumCircuit(2)
bloch_qc.h(0)
bloch_qc.x(1)
plot_bloch_multivector(Statevector(bloch_qc)).savefig("guide-bloch.svg")

# ---------------------------------------------------------------------------
# 4. Q-sphere: latitude = Hamming weight, marker size = magnitude,
#    marker colour = phase.
# ---------------------------------------------------------------------------
qs_qc = QuantumCircuit(3)
qs_qc.h(0)
qs_qc.h(1)
qs_qc.t(0)
plot_state_qsphere(Statevector(qs_qc)).savefig("guide-qsphere.svg")

# ---------------------------------------------------------------------------
# 5-8. The four broadcasting patterns, drawn from fixed coordinates.
# ---------------------------------------------------------------------------
CELL_W, CELL_H = 1.2, 0.8
COL_STEP, ROW_STEP = 1.3, 1.0
SHADE, PLAIN = "#e8e8e8", "white"


def box(ax, x, y, label, fill=PLAIN, fs=9, dashed=False):
    ax.add_patch(Rectangle((x, y), CELL_W, CELL_H, facecolor=fill,
                           edgecolor="black", linewidth=1.0,
                           linestyle="--" if dashed else "-"))
    ax.text(x + CELL_W / 2, y + CELL_H / 2, label, ha="center", va="center",
            fontsize=fs)


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def down_arrow(ax, x, y_from, length=0.35):
    ax.add_patch(FancyArrow(x, y_from, 0, -length, width=0.03,
                            head_width=0.16, head_length=0.14, color="black",
                            length_includes_head=True))


def outer_diagram(n_obs, n_par, obs_shape, par_shape, out_shape, title):
    fig, ax = canvas(7.2, 4.4)
    ax.set_xlim(0, 3.0 + COL_STEP * n_par + 0.4)
    ax.set_ylim(0, 2.2 + ROW_STEP * n_obs + 1.6)
    x0 = 3.0
    top = 1.6 + ROW_STEP * n_obs
    mid = x0 + (COL_STEP * n_par - 0.1) / 2
    for j in range(n_par):
        box(ax, x0 + j * COL_STEP, top, f"$\\theta_{{{j + 1}}}$", SHADE)
    ax.text(mid, top + CELL_H + 0.3, f"parameter values {par_shape}",
            ha="center", va="bottom", fontsize=10)
    for i in range(n_obs):
        box(ax, 1.4, top - (i + 1) * ROW_STEP, f"$O_{{{i + 1}}}$", SHADE)
    ax.text(1.05, top - ROW_STEP * n_obs / 2 - 0.1, f"observables {obs_shape}",
            ha="center", va="center", rotation=90, fontsize=10)
    for i in range(n_obs):
        for j in range(n_par):
            box(ax, x0 + j * COL_STEP, top - (i + 1) * ROW_STEP, "ev")
    ax.text(mid, 0.5, f"expectation values {out_shape}", ha="center",
            va="center", fontsize=10)
    ax.text(0.1, top + CELL_H + 0.3, title, ha="left", va="bottom",
            fontsize=11, fontweight="bold")
    return fig


def row_diagram(n, title, single):
    """Zip (one observable per parameter set) and broadcast-single-observable
    (one observable stretched over every parameter set)."""
    fig, ax = canvas(7.4, 3.6)
    ax.set_xlim(0, 3.4 + COL_STEP * n + 0.4)
    ax.set_ylim(0, 4.8)
    x0 = 3.4
    row_w = COL_STEP * n - (COL_STEP - CELL_W)
    for j in range(n):
        box(ax, x0 + j * COL_STEP, 3.5, f"$\\theta_{{{j + 1}}}$", SHADE)
    ax.text(x0 - 0.2, 3.9, f"parameter values ({n},)", ha="right",
            va="center", fontsize=10)
    if single:
        ax.add_patch(Rectangle((x0, 2.1), row_w, CELL_H, facecolor="none",
                               edgecolor="black", linewidth=0.8,
                               linestyle="--"))
        box(ax, x0, 2.1, "$O$", SHADE)
        ax.text(x0 + row_w - 0.1, 2.5, "the same observable, stretched",
                ha="right", va="center", fontsize=8, style="italic")
        ax.text(x0 - 0.2, 2.5, "observables ()", ha="right", va="center",
                fontsize=10)
    else:
        for j in range(n):
            box(ax, x0 + j * COL_STEP, 2.1, f"$O_{{{j + 1}}}$", SHADE)
        ax.text(x0 - 0.2, 2.5, f"observables ({n},)", ha="right", va="center",
                fontsize=10)
    for j in range(n):
        box(ax, x0 + j * COL_STEP, 0.8, "ev")
        down_arrow(ax, x0 + j * COL_STEP + CELL_W / 2, 2.05)
    ax.text(x0 - 0.2, 1.2, f"expectation values ({n},)", ha="right",
            va="center", fontsize=10)
    ax.text(0.1, 4.5, title, ha="left", va="bottom", fontsize=11,
            fontweight="bold")
    return fig


def nd_diagram(title):
    """Shape algebra: ranks are right-aligned, missing leading axes are padded
    with 1, and every length-1 axis is stretched."""
    fig, ax = canvas(7.4, 3.4)
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 5.6)
    label_x, x0 = 5.6, 5.8
    rows = [
        ("parameter values (3, 6)", ["1", "3", "6"], 4.2, {0: "padded"}),
        ("observables (2, 3, 1)", ["2", "3", "1"], 2.9, {2: "stretched"}),
        ("expectation values (2, 3, 6)", ["2", "3", "6"], 1.0, {}),
    ]
    for name, dims, y, notes in rows:
        ax.text(label_x, y + CELL_H / 2, name, ha="right", va="center",
                fontsize=10)
        for c, d in enumerate(dims):
            box(ax, x0 + c * COL_STEP, y, d, PLAIN if y == 1.0 else SHADE,
                dashed=(c in notes))
            if c in notes:
                ax.text(x0 + c * COL_STEP + CELL_W / 2, y - 0.15, notes[c],
                        ha="center", va="top", fontsize=8, style="italic")
    ax.plot([x0 - 0.2, x0 + COL_STEP * 2 + CELL_W + 0.2], [2.35, 2.35],
            color="black", linewidth=1.0)
    ax.text(0.1, 5.2, title, ha="left", va="bottom", fontsize=11,
            fontweight="bold")
    return fig


row_diagram(4, "Broadcast single observable", single=True).savefig(
    "guide-bc-single.svg")
row_diagram(4, "Zip", single=False).savefig("guide-bc-zip.svg")
outer_diagram(2, 3, "(2, 1)", "(1, 3)", "(2, 3)", "Outer / product").savefig(
    "guide-bc-outer.svg")
nd_diagram("Standard nd generalization").savefig("guide-bc-nd.svg")

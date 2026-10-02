# Figure for s4-q062: the STEM figure — the gate map (qubits + two-qubit
# couplings) of FakeNairobiV2, a 7-qubit H-shaped device. Hand-drawn with
# matplotlib primitives because plot_gate_map needs the Graphviz binary, which
# the pinned environment lacks. The edges drawn are READ FROM the backend's
# coupling map and asserted against the literal EDGES below; the proof asserts
# the same literal and re-renders draw_map() from the backend's own coupling
# map (stem-figure rule: drift fails at render time).
# SYNC DUTY: keep EDGES, POS and draw_map() identical in the proof script.
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from qiskit_ibm_runtime.fake_provider import FakeNairobiV2

EDGES = [(0, 1), (1, 2), (1, 3), (3, 5), (4, 5), (5, 6)]   # undirected pairs drawn
POS = {0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (1, -1), 4: (0, -2), 5: (1, -2), 6: (2, -2)}


def draw_map(edges, pos):
    fig, ax = plt.subplots(figsize=(3.2, 3.2))
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-2.5, 0.5)
    ax.set_aspect("equal")
    ax.axis("off")
    for a, b in edges:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        ax.plot([x1, x2], [y1, y2], color="#555555", linewidth=4, zorder=1)
    for q in sorted(pos):
        x, y = pos[q]
        ax.add_patch(Circle((x, y), 0.24, facecolor="#9ecae1", edgecolor="black",
                            linewidth=1.0, zorder=2))
        ax.text(x, y, str(q), ha="center", va="center", fontsize=12, zorder=3)
    return fig


backend = FakeNairobiV2()
drawn = sorted({tuple(sorted(e)) for e in backend.coupling_map.get_edges()})
assert drawn == EDGES, drawn
assert backend.num_qubits == 7

draw_map(EDGES, POS).savefig("s4-q062-stem.svg")

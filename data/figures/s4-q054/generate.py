# Figure for s4-q054: the STEM figure — the gate map (qubits + two-qubit
# connections) of the target device, FakeLimaV2. Hand-drawn with matplotlib
# primitives because plot_gate_map needs the Graphviz binary, which the pinned
# environment lacks (ledger: "Graphviz is NOT installed"). The edges drawn are
# READ FROM the backend's coupling map and asserted against the literal EDGES
# below; the proof script asserts the same literal (stem-figure rule: drift
# fails at render time). Keep EDGES identical in the proof.
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: fixed coordinates, no sampling.
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from qiskit_ibm_runtime.fake_provider import FakeLimaV2

EDGES = [(0, 1), (1, 2), (1, 3), (3, 4)]          # undirected pairs drawn
backend = FakeLimaV2()
drawn = sorted({tuple(sorted(e)) for e in backend.coupling_map.get_edges()})
assert drawn == EDGES, drawn
assert backend.num_qubits == 5

POS = {0: (0.0, 0.0), 1: (1.0, 0.0), 2: (2.0, 0.0), 3: (1.0, -1.0), 4: (1.0, -2.0)}

fig, ax = plt.subplots(figsize=(3.6, 3.6))
ax.set_xlim(-0.5, 2.5)
ax.set_ylim(-2.5, 0.5)
ax.set_aspect("equal")
ax.axis("off")
for a, b in EDGES:
    (x1, y1), (x2, y2) = POS[a], POS[b]
    ax.plot([x1, x2], [y1, y2], color="#555555", linewidth=4, zorder=1)
for q, (x, y) in POS.items():
    ax.add_patch(Circle((x, y), 0.24, facecolor="#9ecae1", edgecolor="black",
                        linewidth=1.0, zorder=2))
    ax.text(x, y, str(q), ha="center", va="center", fontsize=12, zorder=3)
fig.savefig("s4-q054-stem.svg")

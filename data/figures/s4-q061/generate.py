# Figures for s4-q061: four hand-drawn 5-qubit gate maps (numbered circles,
# lines = two-qubit couplings). Hand-drawn because plot_gate_map needs the
# Graphviz binary, which the pinned environment lacks. A, B and C are the
# coupling maps of FakeLimaV2, FakeManilaV2 and FakeYorktownV2 (asserted
# below); D is a T shape with a different centre. The proof builds a
# GenericBackendV2 for every MAPS entry, re-renders draw_map() from that
# backend's own coupling map (byte-identity with the literal's render) and runs
# the stem's ISA circuit on it with SamplerV2.
# SYNC DUTY: keep MAPS and draw_map() identical in the proof script.
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from qiskit_ibm_runtime.fake_provider import FakeLimaV2, FakeManilaV2, FakeYorktownV2

# key: (undirected edges, node positions)
MAPS = {
    "A": ([(0, 1), (1, 2), (1, 3), (3, 4)],
          {0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (1, -1), 4: (1, -2)}),
    "B": ([(0, 1), (1, 2), (2, 3), (3, 4)],
          {0: (0, 0), 1: (1, 0), 2: (2, 0), 3: (3, 0), 4: (4, 0)}),
    "C": ([(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4)],
          {0: (0, 0), 1: (0, -2), 2: (1, -1), 3: (2, 0), 4: (2, -2)}),
    "D": ([(0, 1), (1, 3), (2, 3), (3, 4)],
          {2: (0, 0), 3: (1, 0), 4: (2, 0), 1: (1, -1), 0: (1, -2)}),
}


def draw_map(edges, pos):
    fig, ax = plt.subplots(figsize=(3.6, 2.6))
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-2.5, 0.5)
    ax.set_aspect("equal")
    ax.axis("off")
    for a, b in edges:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        ax.plot([x1, x2], [y1, y2], color="#555555", linewidth=4, zorder=1)
    for q in sorted(pos):
        x, y = pos[q]
        ax.add_patch(Circle((x, y), 0.26, facecolor="#9ecae1", edgecolor="black",
                            linewidth=1.0, zorder=2))
        ax.text(x, y, str(q), ha="center", va="center", fontsize=12, zorder=3)
    return fig


def undirected(backend):
    return sorted({tuple(sorted(e)) for e in backend.coupling_map.get_edges()})


assert undirected(FakeLimaV2()) == MAPS["A"][0]
assert undirected(FakeManilaV2()) == MAPS["B"][0]
assert undirected(FakeYorktownV2()) == MAPS["C"][0]

for key, (edges, pos) in MAPS.items():
    draw_map(edges, pos).savefig(f"s4-q061-{key}.svg")

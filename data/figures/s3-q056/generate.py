# Figures for s3-q056: mpl renderings of the transpiled stem circuit and four
# misconception variants. Every option is a REAL pass-manager output (so the
# "q_v -> p" layout labels are not a tell), and the proof script builds THE SAME
# five circuits and compares wire labels + gate sequences — keep the two
# definitions in sync (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: seed_transpiler is pinned and the layout is given explicitly.
from qiskit import QuantumCircuit
from qiskit.transpiler import CouplingMap, generate_preset_pass_manager

LINE = CouplingMap.from_line(3)
FULL = CouplingMap.from_full(3)


def stem_circuit():
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    return qc


def flipped_circuit():
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(2, 0)
    return qc


def routed(circ, coupling_map, initial_layout, **kwargs):
    pm = generate_preset_pass_manager(
        optimization_level=0, coupling_map=coupling_map,
        initial_layout=initial_layout, seed_transpiler=42, **kwargs,
    )
    return pm.run(circ)


VARIANTS = {
    # A — the line's missing 0-2 edge ignored (a fully connected map).
    "A": routed(stem_circuit(), FULL, [0, 1, 2]),
    # B — the stem code, verbatim.
    "B": routed(stem_circuit(), LINE, [0, 1, 2]),
    # C — initial_layout read as physical -> virtual.
    "C": routed(stem_circuit(), LINE, [2, 1, 0]),
    # D — routing confused with basis translation (SWAP as three CX).
    "D": routed(stem_circuit(), LINE, [0, 1, 2],
                basis_gates=["rz", "sx", "x", "cx"]),
    # E — CX control and target treated as interchangeable.
    "E": routed(flipped_circuit(), LINE, [0, 1, 2]),
}

for key, circ in VARIANTS.items():
    fig = circ.draw(output="mpl")
    fig.savefig(f"s3-q056-{key}.svg")

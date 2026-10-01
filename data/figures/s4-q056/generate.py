# Figure for s4-q056: the STEM figure is the mpl drawing of a real level-0
# preset-pass-manager output (3-qubit line, initial_layout=[1, 0, 2],
# coupling map only, so the routing SWAP is drawn as a SWAP). The proof runs
# the same pass manager on the same circuit and asserts the literal TARGET
# below (stem-figure rule: drift fails at render time). Keep this block
# identical in the proof.
# Runs under pipeline/render_figures.py's deterministic prelude.
# Determinism: initial_layout and seed_transpiler are pinned.
from qiskit import QuantumCircuit
from qiskit.transpiler import CouplingMap, generate_preset_pass_manager

qc = QuantumCircuit(3)
qc.h(1)
qc.cx(1, 0)
qc.cx(1, 2)

pm = generate_preset_pass_manager(
    optimization_level=0,
    coupling_map=CouplingMap.from_line(3),
    initial_layout=[1, 0, 2],
    seed_transpiler=42,
)
isa = pm.run(qc)

# Physical-wire gate list, initial layout, final layout (literal target).
TARGET = (
    (("h", (0,)), ("cx", (0, 1)), ("swap", (1, 2)), ("cx", (0, 1))),
    (1, 0, 2),
    (2, 0, 1),
)
got = (
    tuple((i.operation.name, tuple(isa.find_bit(b).index for b in i.qubits)) for i in isa.data),
    tuple(isa.layout.initial_index_layout()),
    tuple(isa.layout.final_index_layout()),
)
assert got == TARGET, got
fig = isa.draw(output="mpl")
fig.savefig("s4-q056-stem.svg")

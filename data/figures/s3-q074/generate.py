# Figure for s3-q074: the STEM figure — the mpl drawing of a real level-0
# preset-pass-manager output (4-qubit line, trivial initial layout) in which
# routing inserts two SWAPs. The proof runs the same pass manager on the same
# circuit, asserts the same TARGET literal (stem-figure rule: drift fails at
# render time) and reads final_index_layout() off the result.
# SYNC DUTY: keep the circuit, the pass manager and TARGET identical in the proof.
# Runs under pipeline/render_figures.py's deterministic prelude.
# Determinism: initial_layout and seed_transpiler are pinned.
from qiskit import QuantumCircuit
from qiskit.transpiler import CouplingMap, generate_preset_pass_manager

qc = QuantumCircuit(4)
qc.h(3)
qc.cx(3, 1)
qc.cx(3, 0)

pm = generate_preset_pass_manager(
    optimization_level=0,
    coupling_map=CouplingMap.from_line(4),
    initial_layout=[0, 1, 2, 3],
    seed_transpiler=42,
)
isa = pm.run(qc)

# What the figure shows: gates on physical wires, in drawing order.
TARGET = (("h", (3,)), ("swap", (2, 3)), ("cx", (2, 1)), ("swap", (1, 2)), ("cx", (1, 0)))
ops = tuple((i.operation.name, tuple(isa.find_bit(b).index for b in i.qubits)) for i in isa.data)
assert ops == TARGET, ops
assert isa.layout.initial_index_layout() == [0, 1, 2, 3]

fig = isa.draw(output="mpl")
fig.savefig("s3-q074-stem.svg")

# Figure for s4-q063: the STEM figure — the mpl drawing (idle wires hidden) of
# a real level-1 ISA circuit for FakeManilaV2 with a pinned initial layout.
# The question hides the source circuit: the figure IS the circuit. The proof
# rebuilds the same `isa` with the same pass manager, asserts the TARGET
# literal below (stem-figure rule: drift fails at render time), and runs it.
# SYNC DUTY: keep the source circuit, the pass manager and TARGET identical in
# the proof script.
# Runs under pipeline/render_figures.py's deterministic prelude.
# Determinism: initial_layout and seed_transpiler are pinned; no sampling here.
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeManilaV2

qc = QuantumCircuit(3)
qc.x(2)
qc.cx(2, 1)
qc.measure_all()

pm = generate_preset_pass_manager(optimization_level=1, backend=FakeManilaV2(),
                                  initial_layout=[3, 0, 1], seed_transpiler=7)
isa = pm.run(qc)

# What the figure shows: (gate, physical qubits, meas bits), in drawing order.
TARGET = (("x", (1,), ()), ("cx", (1, 0), ()), ("barrier", (3, 0, 1), ()),
          ("measure", (3,), (0,)), ("measure", (0,), (1,)), ("measure", (1,), (2,)))
ops = tuple((i.operation.name, tuple(isa.find_bit(b).index for b in i.qubits),
             tuple(isa.find_bit(b).index for b in i.clbits)) for i in isa.data)
assert ops == TARGET, ops

fig = isa.draw(output="mpl", idle_wires=False)
fig.savefig("s4-q063-stem.svg")

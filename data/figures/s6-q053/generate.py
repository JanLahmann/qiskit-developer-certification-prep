# Figure for s6-q053: an ISA circuit for FakeManilaV2 whose drawing carries the
# layout (wire labels "q_i -> p"). The proof script builds the SAME isa with the
# same pass-manager call and asserts the same LAYOUT literal — keep the two in
# sync (ledger rule: figure content == proof target). The assert is the sync check.
# Runs under pipeline/render_figures.py's deterministic prelude.
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeManilaV2

# virtual qubit -> physical qubit, as printed on the drawing's wire labels
LAYOUT = [2, 3]

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

pm = generate_preset_pass_manager(optimization_level=1, backend=FakeManilaV2(),
                                  initial_layout=[2, 3], seed_transpiler=42)
isa = pm.run(qc)
assert isa.layout.final_index_layout() == LAYOUT, isa.layout.final_index_layout()
assert isa.num_qubits == 5

isa.draw(output="mpl", idle_wires=True).savefig("s6-q053-stem.svg")

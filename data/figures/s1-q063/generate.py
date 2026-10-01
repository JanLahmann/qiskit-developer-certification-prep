# Figure for s1-q063: the mpl drawing of the phase-kickback circuit the
# question asks about. The proof script hardcodes the SAME gate list (STEM)
# and the probabilities the drawn circuit yields (TARGET) — keep the two in
# sync (ledger rule: figure content == proof target). The assert is the sync
# check: if the drawn circuit ever stops producing TARGET, the render fails.
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

STEM = [("x", 1), ("h", 1), ("h", 0), ("cx", 0, 1), ("h", 0), ("h", 1)]
TARGET = {"11": 1.0}

qc = QuantumCircuit(2)
for name, *args in STEM:
    getattr(qc, name)(*args)

probs = {str(k): round(float(v), 6)
         for k, v in Statevector(qc).probabilities_dict().items() if float(v) > 1e-9}
assert probs == TARGET, probs

fig = qc.draw(output="mpl")
fig.savefig("s1-q063-stem.svg")

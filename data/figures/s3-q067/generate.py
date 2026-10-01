# Figure for s3-q067: the stem figure is the mpl drawing of a real level-0
# preset-pass-manager output (3-qubit line, initial_layout=[2, 1, 0]).
# The options are candidate INPUT circuits; the proof runs every candidate
# through the same pass manager and compares against the literal TARGET below,
# which this generator asserts for the drawn circuit (stem-figure rule: drift
# fails at render time). Keep the block below identical in the proof.
# Runs under pipeline/render_figures.py's deterministic prelude.
# Determinism: initial_layout and seed_transpiler are pinned.
from qiskit import QuantumCircuit
from qiskit.transpiler import CouplingMap, generate_preset_pass_manager

pm = generate_preset_pass_manager(
    optimization_level=0,
    coupling_map=CouplingMap.from_line(3),
    initial_layout=[2, 1, 0],
    seed_transpiler=42,
)

# Candidate input circuits, one per option (gate lists exactly as the options print them).
CANDIDATES = {
    "A": [("h", 0), ("cx", 0, 1), ("cx", 0, 1)],
    "B": [("h", 2), ("cx", 2, 1), ("cx", 2, 0)],
    "C": [("h", 0), ("cx", 0, 2), ("cx", 0, 1)],
    "D": [("h", 0), ("cx", 0, 1), ("cx", 0, 2)],
    "E": [("h", 0), ("cx", 0, 1), ("cx", 1, 2)],
}
STEM_KEY = "D"   # the circuit whose transpiled drawing is the stem figure


def build(ops):
    qc = QuantumCircuit(3)
    for name, *qargs in ops:
        getattr(qc, name)(*qargs)
    return qc


def sig(circ):
    """Physical-wire gate sequence plus the layout the drawer prints."""
    ops = tuple((i.operation.name, tuple(circ.find_bit(b).index for b in i.qubits))
                for i in circ.data)
    return ops, tuple(circ.layout.initial_index_layout())


# What the stem figure shows (literal target; the generator asserts it).
TARGET = ((("h", (2,)), ("cx", (2, 1)), ("swap", (1, 0)), ("cx", (2, 1))), (2, 1, 0))

isa = pm.run(build(CANDIDATES[STEM_KEY]))
assert sig(isa) == TARGET, sig(isa)
fig = isa.draw(output="mpl")
fig.savefig("s3-q067-stem.svg")

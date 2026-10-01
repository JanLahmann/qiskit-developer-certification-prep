# Figures for s1-q061: mpl drawings of real_amplitudes(3, reps=1) with four
# different `entanglement` strategies. The proof script builds THE SAME four
# circuits and compares their CX (control, target) lists with the stem call —
# keep the two definitions in sync (ledger rule: figure variants == proof
# variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
from qiskit.circuit.library import real_amplitudes

VARIANTS = {
    "A": "circular",        # nearest-neighbour chain plus a wrap-around pair
    "B": "full",            # the stem call: every pair of qubits
    "C": "linear",          # nearest-neighbour chain only
    "D": "reverse_linear",  # the function's default chain, applied in reverse
}

for key, ent in VARIANTS.items():
    fig = real_amplitudes(3, reps=1, entanglement=ent).draw(output="mpl")
    fig.savefig(f"s1-q061-{key}.svg")

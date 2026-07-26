# Figures for s3-q057: mpl renderings of five genuine preset-pass-manager
# outputs. Every option is a real `generate_preset_pass_manager(...).run(...)`
# result (no hand-built circuits), so the drawings share the same drawer
# conventions and nothing but the optimization behaviour distinguishes them.
# The proof script builds THE SAME five pass-manager runs and compares the gate
# sequence each drawer receives — keep the two definitions in sync
# (ledger rule: figure variants == proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: seed_transpiler is pinned and no coupling map/target is given,
# so no layout or routing randomness enters.
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager


def build(z_pair=True, cx_pair=True, once=False):
    """The stem circuit (defaults) and the three edited versions whose level-0
    output is what each misconception expects to see."""
    qc = QuantumCircuit(3)
    qc.h(0)
    if cx_pair or once:
        qc.cx(0, 1)
    if cx_pair and not once:
        qc.cx(0, 1)
    qc.t(1)
    qc.h(2)
    if z_pair or once:
        qc.z(2)
    if z_pair and not once:
        qc.z(2)
    qc.cx(1, 2)
    qc.cx(0, 2)
    return qc


def run(circ, level):
    pm = generate_preset_pass_manager(optimization_level=level,
                                      seed_transpiler=42)
    return pm.run(circ)


VARIANTS = {
    # A — both repeated pairs cancelled (what level 2 really produces).
    "A": lambda: run(build(), 2),
    # B — only the Z pair removed.
    "B": lambda: run(build(z_pair=False), 0),
    # C — the stem code, verbatim.
    "C": lambda: run(build(), 0),
    # D — only the CX(0, 1) pair removed.
    "D": lambda: run(build(cx_pair=False), 0),
    # E — each repeated gate kept once instead of cancelling in pairs.
    "E": lambda: run(build(once=True), 0),
}

for key, make in VARIANTS.items():
    fig = make().draw(output="mpl")
    fig.savefig(f"s3-q057-{key}.svg")

# Figures for s2-q045: plot_histogram renderings of the stem call and four
# misconception variants of what `number_to_keep` does. The proof script builds
# THE SAME five calls and reads the bar labels/heights back off the rendered
# figures — keep the two definitions in sync (ledger rule: figure variants ==
# proof variants).
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
# Determinism: the counts are a fixed literal dict — nothing is sampled.
from qiskit.visualization import plot_histogram

COUNTS = {"000": 400, "111": 380, "001": 120, "010": 70, "100": 30}

VARIANTS = {
    # A — folded outcomes simply dropped instead of pooled.
    "A": ({"000": 400, "001": 120, "111": 380}, {}),
    # B — "rest" read as the largest folded outcome.
    "B": ({"000": 400, "001": 120, "111": 380, "rest": 70}, {}),
    # C — number_to_keep believed to affect only the legend/sorting.
    "C": (COUNTS, {}),
    # D — the stem call, verbatim.
    "D": (COUNTS, {"number_to_keep": 3}),
    # E — "rest" read as the average of the folded outcomes.
    "E": ({"000": 400, "001": 120, "111": 380, "rest": 50}, {}),
}

for key, (counts, kwargs) in VARIANTS.items():
    fig = plot_histogram(counts, **kwargs)
    fig.savefig(f"s2-q045-{key}.svg")

# Figure for s6-q041: the error-bar plot the DISPLAYED stem code draws when the
# missing options line is `estimator.options.default_precision = 0.1`. STEM_CODE is the
# question's `code` field verbatim (sync duty: edit both together); the proof executes
# the same text with each candidate line and compares against TARGET_* below, which
# the asserts pin to what this figure draws.
# Runs under pipeline/render_figures.py's deterministic prelude (Agg backend,
# fixed svg.hashsalt, no Date metadata); writes bare filenames into cwd.
import matplotlib.pyplot as plt
import numpy as np

STEM_CODE = 'import matplotlib.pyplot as plt\nimport numpy as np\nfrom qiskit import QuantumCircuit\nfrom qiskit.circuit import Parameter\nfrom qiskit.quantum_info import SparsePauliOp\nfrom qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager\nfrom qiskit_ibm_runtime import EstimatorV2\nfrom qiskit_ibm_runtime.fake_provider import FakeManilaV2\n\ntheta = Parameter("theta")\nqc = QuantumCircuit(1)\nqc.ry(theta, 0)\n\nbackend = FakeManilaV2()\npm = generate_preset_pass_manager(optimization_level=1, backend=backend,\n                                  seed_transpiler=42)\nisa = pm.run(qc)\nobs = SparsePauliOp("Z").apply_layout(isa.layout)\n\nangles = np.array([[0.0], [np.pi / 3], [2 * np.pi / 3], [np.pi]])\nestimator = EstimatorV2(mode=backend)\nestimator.options.simulator.seed_simulator = 7\n# <- the options line goes here\npub_result = estimator.run([(isa, obs, angles)]).result()[0]\n\nplt.errorbar(angles.ravel(), pub_result.data.evs,\n             yerr=pub_result.data.stds, fmt="o-", capsize=4)\nplt.xlabel("theta")\nplt.ylabel("expectation value")'
KEY_LINE = "estimator.options.default_precision = 0.1"

# What the drawing shows: the marker heights and the error-bar half-lengths.
TARGET_EVS = (0.92, 0.48, -0.32, -0.92)
TARGET_STDS = (0.039, 0.088, 0.095, 0.039)

ns = {}
exec(STEM_CODE.replace("# <- the options line goes here", KEY_LINE), ns)
evs = np.asarray(ns["pub_result"].data.evs)
stds = np.asarray(ns["pub_result"].data.stds)
assert tuple(np.round(evs, 3)) == TARGET_EVS, tuple(np.round(evs, 3))
assert tuple(np.round(stds, 3)) == TARGET_STDS, tuple(np.round(stds, 3))

plt.gcf().savefig("s6-q041-stem.svg")

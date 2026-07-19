"""Offline patching for proof execution.

Proof scripts run with no IBM Quantum credentials and no network. The rule
for generated questions is to use local primitives with fake backends
directly (qiskit-ibm-runtime local testing mode: passing a fake backend as
`mode=` executes locally). This patch is the safety net for question code
that instantiates QiskitRuntimeService the way real exam-relevant snippets
do.

Pattern adapted from doQumentation's CI harness (00_patch_runtime.py),
simplified: only QiskitRuntimeService is replaced; Session/Batch and the
V2 primitives already work locally with fake backends.
"""

from __future__ import annotations

_FAKE_CACHE: dict = {}


def _fake(name: str):
    from qiskit_ibm_runtime.fake_provider import (  # noqa: PLC0415
        FakeBrisbane,
        FakeFez,
        FakeMarrakesh,
    )

    classes = {
        "ibm_brisbane": FakeBrisbane,
        "ibm_fez": FakeFez,
        "ibm_marrakesh": FakeMarrakesh,
    }
    cls = classes.get(name, FakeBrisbane)
    if cls not in _FAKE_CACHE:
        _FAKE_CACHE[cls] = cls()
    return _FAKE_CACHE[cls]


class _OfflineRuntimeService:
    """Stands in for QiskitRuntimeService; returns fake backends."""

    def __init__(self, *args, **kwargs):  # accept and ignore credentials
        pass

    def backend(self, name=None, **kwargs):
        return _fake(name or "ibm_brisbane")

    def backends(self, **kwargs):
        return [_fake(n) for n in ("ibm_brisbane", "ibm_fez", "ibm_marrakesh")]

    def least_busy(self, **kwargs):
        return _fake("ibm_brisbane")

    # Anything else (jobs, saved accounts) is out of scope for proofs.
    def __getattr__(self, item):
        raise AttributeError(
            f"QiskitRuntimeService.{item} is not available in the offline proof "
            "environment — proof scripts must stay local (fake backends)."
        )


def apply_patches() -> None:
    import qiskit_ibm_runtime as rt  # noqa: PLC0415

    rt.QiskitRuntimeService = _OfflineRuntimeService
    # Also patch the symbol where commonly imported from.
    try:
        import qiskit_ibm_runtime.qiskit_runtime_service as qrs  # noqa: PLC0415

        qrs.QiskitRuntimeService = _OfflineRuntimeService
    except Exception:
        pass

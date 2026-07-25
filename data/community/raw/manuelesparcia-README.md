# 1.What is the main difference between qc.measure_all() and manually calling qc.measure(q, c)?

A) measure_all() adds measurements but never adds classical bits\
B) measure_all() measures all qubits into classical bits (creating them if needed), while manual measurement lets you choose mapping\
C) Manual measurement always measures in the X basis\
D) They are identical in every case 

# 2.You build a parameterized circuit with a Parameter("θ"). What is a correct way to evaluate it at θ = 0.3?

A) qc(0.3)\
B) qc.bind_parameters({"θ": 0.3}) only (no other option exists)\
C) Use parameter binding (e.g., assign/bind) to produce a bound circuit before execution/sampling\
D) Parameters cannot be bound in Qiskit v2.x

# 3. What does qc.cx(0,1) do?

A) Applies X on qubit 1 unconditionally\
B) Applies X on qubit 0 controlled by qubit 1\
C) Applies X on qubit 1 controlled by qubit 0\
D) Swaps qubit 0 and 1

# 4. In Qiskit, which statement is generally true about measured bitstrings?

A) The leftmost bit is always qubit 0\
B) Bitstring order depends on classical bit/register ordering; always verify mapping used for measurement\
C) Bitstrings are always returned in little-endian order, regardless of measurement mapping\
D) Qiskit returns integers only, never bitstrings

# 5. Which tool is most appropriate for quickly prototyping an algorithm with exact (noise-free) statevector simulation using SDK primitives?

A) StatevectorSampler / StatevectorEstimator\
B) BackendSamplerV2 with a noisy device backend only\
C) Only IBM Runtime can do statevector simulation\
D) plot_histogram

# 6. Which function is commonly used to visualize shot-count outcomes as a histogram?

A) plot_histogram\
B) plot_bloch_multivector\
C) plot_gate_map only\
D) draw("mpl") is the only option

# 7. plot_bloch_multivector(state) expects state to be:

A) A QuantumCircuit only\
B) A quantum state object (e.g., Statevector/DensityMatrix) or equivalent array representation\
C) A dict of counts\
D) A backend object

# 8. What is the primary goal of transpilation?

A) Convert quantum circuits into Python bytecode\
B) Rewrite/optimize a circuit to satisfy a backend’s constraints (basis gates, connectivity, timing)\
C) Encrypt a circuit so it can run securely\
D) Replace quantum gates with classical logic gates

# 9. In transpile(circuit, optimization_level=n), higher n generally means:

A) Fewer transformations and faster compilation always\
B) More aggressive optimization passes (often slower compile time, potentially better circuits)\
C) More shots during execution\
D) More qubits are automatically added

# 10. What is the role of a Target in the Qiskit transpiler?

A) It stores measurement results\
B) It describes backend constraints/instructions to guide compilation\
C) It is only used for visualization\
D) It is a synonym for QuantumCircuit

# 11. If you pass backend=... to transpile() and also pass an explicit coupling_map=..., which is true?

A) The explicit coupling_map can override backend-derived constraints\
B) The backend is ignored if any option is set\
C) transpile() raises an error\
D) The circuit is not modified

# 12. Which statement is true?

A) A PassManager is a sequence of transpiler passes you can run on a circuit\
B) Pass managers are only for classical compilation\
C) Pass managers cannot be customized\
D) Optimization levels do not use pass managers internally

# 13. Preset pass managers are best described as:

A) Random pass sequences that change each run\
B) Prebuilt staged pass managers corresponding to standard optimization levels and configurations\
C) Only available in IBM Runtime\
D) Deprecated in Qiskit v2.x

# 14. Which pairing is correct?

A) Sampler → expectation values; Estimator → bitstring samples\
B) Sampler → bitstring samples (from classical outputs); Estimator → expectation values of observables\
C) Sampler → transpilation; Estimator → visualization\
D) Both do exactly the same thing

# 15. In Qiskit v2.x, which statement is most accurate?

A) Only V1 primitives exist\
B) V2 primitives (BaseSamplerV2, BaseEstimatorV2) are the current interfaces; older V1 interfaces are deprecated\
C) Primitives were removed entirely\
D) Primitives only work on hardware, not simulators

# 16. What is BackendSamplerV2 mainly used for?

A) Wrapping a BackendV2 so it can be used through the SamplerV2 interface\
B) Drawing circuits\
C) Importing OpenQASM 3\
D) Building a Target from scratch

# 17. Calling StatevectorEstimator.run(...) returns:

A) A matplotlib figure\
B) A primitive job object; you retrieve the result via .result()\
C) A dict of counts directly\
D) A QuantumCircuit

# 18. A Sampler is designed to return:

A) Samples from classical output registers (bitstrings), possibly as quasi-probabilities depending on implementation\
B) Only a unitary matrix\
C) Only a density matrix\
D) Only expectation values of Paulis

# 19. To estimate ⟨Z⊗Z⟩ for a circuit with two qubits, Estimator conceptually needs:

A) Only the circuit, no observable\
B) Only the observable, no circuit\
C) A circuit and an observable (or list of observables)\
D) Two circuits, no observables

# 20. Which function exports a QuantumCircuit to an OpenQASM 3 string?

A) qiskit.qasm3.dump()\
B) qiskit.qasm3.dumps()\
C) qiskit.qasm2.dumps() only\
D) QuantumCircuit.to_qasm3() only

# 21. Which statement is most accurate about parsing OpenQASM 3 into a QuantumCircuit?

A) qiskit.qasm3.loads() works out-of-the-box for all OpenQASM 3 programs with no extra components\
B) Import support can require the qiskit-qasm3-import extension, and feature support is evolving\
C) Qiskit cannot export OpenQASM 3 at all\
D) OpenQASM 3 is only for visualization

# 22. When is transpilation typically necessary?

A) Always, even for pure statevector reference primitives\
B) Typically when targeting a specific backend (hardware or backend-based execution) with constraints\
C) Only when using OpenQASM 2\
D) Never; Qiskit runs any circuit on any backend

# 23. Which is a common way to render a circuit diagram inside notebooks?

A) qc.draw() (and optionally qc.draw("mpl") when matplotlib is available)\
B) plot_bloch_vector(qc)\
C) transpile(qc).histogram()\
D) Target.draw(qc)

# 24. You measure qubit 1 into classical bit 0 and qubit 0 into classical bit 1. Which is true?

A) The resulting bitstrings will reflect that mapping; you must interpret bit positions via classical bits, not qubit indices\
B) Qiskit automatically reorders results to qubit index order\
C) This mapping is invalid and raises an error\
D) The circuit becomes non-unitary and cannot run

# Anwers

1. B 
2. C 
3. C
4. B 
5. A 
6. A 
7. B 
8. B 
9. B 
10. B 
11. A 
12. A 
13. B 
14. B 
15. B 
16. A 
17. B 
18. A 
19. C 
20. B 
21. B 
22. B 
23. A 
24. A 

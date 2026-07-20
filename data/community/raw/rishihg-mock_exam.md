# Qiskit v2.X Certification Practice Questions `(Verified)`

> **Note**: These 25 questions cover all 8 sections of the official [IBM Qiskit v2.X Certification](https://www.ibm.com/training/certification/ibm-certified-quantum-computation-using-qiskit-v2x-developer-associate-C9008400).

## Question 1
What is the primary package for circuit construction?

- A) `qiskit.providers`
- B) `qiskit.circuit`
- C) `qiskit.quantum_info`
- D) `qiskit.algorithms`

---

## Question 2
Which method is used to add a Hadamard gate to a quantum circuit?

- A) `circuit.hadamard()`
- B) `circuit.h()`
- C) `circuit.add_h()`
- D) `circuit.apply_hadamard()`

---

## Question 3
What does the `QuantumCircuit.measure()` method do?

- A) Measures all qubits automatically
- B) Adds a measurement operation to specified qubits
- C) Returns measurement results
- D) Initializes classical bits

---

## Question 4
What is the correct way to create a 3-qubit quantum circuit?

- A) `QuantumCircuit(3)`
- B) `Circuit(qubits=3)`
- C) `QCircuit(3)`
- D) `create_circuit(3)`

---

## Question 5
Which V2 primitive is used for running circuits and getting quasi-probability distributions?

- A) `Executor`
- B) `SamplerV2`
- C) `Runner`
- D) `EstimatorV2`

---

## Question 6
What does the `EstimatorV2` primitive calculate?

- A) Circuit depth
- B) Expectation values of observables
- C) Probability distributions
- D) Gate fidelity

---

## Question 7
Which method applies a CNOT gate with control qubit 0 and target qubit 1?

- A) `circuit.cnot(0, 1)`
- B) `circuit.cx(0, 1)`
- C) `circuit.controlled_x(0, 1)`
- D) `circuit.c_not(0, 1)`

---

## Question 8
What is the purpose of `transpile()` in Qiskit?

- A) To execute quantum circuits
- B) To convert circuits to be compatible with specific backend hardware
- C) To simulate quantum noise
- D) To visualize circuits

---

## Question 9
Which class represents a quantum gate?

- A) `QuantumGate`
- B) `Gate`
- C) `QGate`
- D) `Instruction`

---

## Question 10
How do you create a classical register with 3 bits?

- A) `ClassicalRegister(3)`
- B) `CBit(3)`
- C) `ClassicBits(3)`
- D) `CRegister(3)`

---

## Question 11
What does the `qiskit.quantum_info.Statevector` class represent?

- A) A quantum circuit
- B) A quantum state as a state vector
- C) A measurement outcome
- D) A quantum operator

---

## Question 12
Which method is used to draw/visualize a quantum circuit?

- A) `circuit.show()`
- B) `circuit.display()`
- C) `circuit.draw()`
- D) `circuit.visualize()`

---

## Question 13
What is the purpose of the `qiskit.primitives` module?

- A) To provide basic quantum gates
- B) To offer simplified interfaces for running quantum computations
- C) To create primitive quantum circuits
- D) To define elementary quantum states

---

## Question 14
Which rotation gate rotates a qubit around the X-axis by angle θ?

- A) `rx(θ)`
- B) `rotx(θ)`
- C) `x_rotation(θ)`
- D) `rotate_x(θ)`

---

## Question 15
What does the `barrier()` method do in a quantum circuit?

- A) Prevents qubits from being measured
- B) Acts as a visual separator and prevents certain optimizations across it
- C) Creates an error correction barrier
- D) Blocks gate application

---

## Question 16
In Qiskit Aer, what is the default simulator backend called?

- A) `qasm_simulator`
- B) `AerSimulator`
- C) `statevector_simulator`
- D) `BasicSimulator`

---

## Question 17
Which method adds a Pauli-Z gate to qubit 2 in a circuit?

- A) `circuit.z(2)`
- B) `circuit.pauli_z(2)`
- C) `circuit.pz(2)`
- D) `circuit.apply_z(2)`

---

## Question 18
What does `QuantumCircuit.compose()` do?

- A) Decomposes a circuit into basic gates
- B) Combines two quantum circuits
- C) Compiles a circuit
- D) Creates a composite gate

---

## Question 19
Which package contains the `Operator` class for representing quantum operators?

- A) `qiskit.circuit`
- B) `qiskit.operators`
- C) `qiskit.quantum_info`
- D) `qiskit.extensions`

---

## Question 20
What is the recommended way to get intermediate statevectors?

- A) Use `circuit.save_statevector()` from Qiskit Aer for simulation
- B) Use the `Statevector.from_instruction()` method
- C) Use the reference `StatevectorSampler` primitive
- D) All of the above are valid approaches

---

## Question 21
How do you retrieve a previously submitted job using its job ID?

- A) `service.get_job(job_id)`
- B) `service.retrieve_job(job_id)`
- C) `service.job(job_id)`
- D) `service.load_job(job_id)`

---

## Question 22
Which execution mode should you use for running multiple related jobs with reduced queue times?

- A) Job mode
- B) Session mode
- C) Batch mode
- D) Runtime mode

---

## Question 23
In OpenQASM 3, how do you declare a classical bit register with 5 bits?

- A) `creg myregister[5];`
- B) `bit[5] myregister;`
- C) `classical[5] myregister;`
- D) `register bit myregister[5];`

---

## Question 24
How do you set the resilience level to 1 for error mitigation in the Sampler primitive?

- A) `sampler.set_resilience(1)`
- B) `sampler.options.resilience_level = 1`
- C) `sampler.resilience = 1`
- D) `sampler.error_mitigation(level=1)`

---

## Question 25
Which method correctly implements classical feedforward in a dynamic circuit?

- A) `circuit.if_test((clbit, 1), true_body)`
- B) `circuit.conditional(clbit, true_body)`
- C) `circuit.if_clause(clbit == 1, true_body)`
- D) `circuit.measure_and_branch(clbit, true_body)`

---

## Answer Key

<details>
<summary>Click to reveal answers</summary>

```
1. B     6. B     11. B     16. B     21. C
2. B     7. B     12. C     17. A     22. B
3. B     8. B     13. B     18. B     23. B
4. A     9. B     14. A     19. C     24. B
5. B     10. A    15. B     20. D     25. A
```

</details>

---

**Verified against:**
- Official IBM Qiskit v2.X certification exam guidelines
- Qiskit SDK latest documentation
- Qiskit Runtime V2 primitives API

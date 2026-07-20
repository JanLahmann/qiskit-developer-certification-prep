# C1000-179 Qiskit v2.x Developer Certification — Qiskit SDK 2.4 Programming Practice Exam

**Unofficial practice exam for learners preparing for the IBM Qiskit v2.x Developer certification.**

This practice exam is designed to test knowledge of using Qiskit SDK 2.4 and preparing the real exam of the IBM Qiskit v2.x Developer certification.

> **Disclaimer:** This is a community-created, unofficial study resource. It is not endorsed by IBM, Qiskit, or IBM Quantum.

## Exam Simulation

| Item | Practice Exam Setting |
|---|---:|
| Questions | 68 mixed-response questions |
| Time limit | 90 minutes |
| Suggested pass target | 47 / 68 |
| Main focus | Qiskit SDK 2.4-style programming, Runtime V2, result handling, and error-mitigation coding |
| Answer format | Single-answer and select-all-that-apply questions |

## Instructions

1. Time yourself for **90 minutes**.
2. For single-answer questions, choose one answer. For **select-all-that-apply** questions, select every correct answer and no incorrect answers.
3. Open **Answer and explanation** only after you have selected your answer(s).
4. Review the full answer key only after completing all 68 questions. Multiple-response questions receive credit only when all correct choices are selected.
---

## Practice Questions

### Question 01 of 68

You are asked to build a two-qubit Bell-state circuit: apply H on qubit 0, apply CX with qubit 0 as control and qubit 1 as target, then measure qubits 0 and 1 into classical bits 0 and 1. Which code does that?

**A.**

```python
from qiskit import QuantumCircuit
qc = QuantumCircuit(2, 2)
qc.x(0)
qc.cx(0, 1)
qc.measure_all()
```

**B.**

```python
from qiskit import QuantumCircuit
qc = QuantumCircuit(2, 2)
qc.h(1)
qc.cx(1, 0)
qc.measure([0, 1], [0, 1])
```

**C.**

```python
from qiskit import QuantumCircuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])
```

**D.**

```python
from qiskit import QuantumCircuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** C

**Explanation:** The requested operations are exactly H(0), CX(0,1), and measurement into the two existing classical bits.

</details>

---

### Question 02 of 68

Which code creates a circuit with 3 qubits and 2 classical bits, then measures qubit 1 into classical bit 0?

**A.**

```python
from qiskit import QuantumCircuit
qc = QuantumCircuit(3)
qc.measure(1, 0)
```

**B.**

```python
from qiskit import QuantumCircuit
qc = QuantumCircuit(2, 3)
qc.measure(1, 0)
```

**C.**

```python
from qiskit import QuantumCircuit
qc = QuantumCircuit(3, 2)
qc.measure(1, 0)
```

**D.**

```python
from qiskit import QuantumCircuit
qc = QuantumCircuit(3, 2)
qc.measure(0, 1)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** C

**Explanation:** `QuantumCircuit(3, 2)` allocates 3 qubits and 2 classical bits; `measure(1, 0)` maps qubit 1 to classical bit 0.

</details>

---

### Question 03 of 68

After this code runs, what does `qc.count_ops().get("cx", 0)` return?

```python
from qiskit import QuantumCircuit
qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.x(2)
```

**A.**

`0`

**B.**

`2`

**C.**

`3`

**D.**

`1`

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** B

**Explanation:** There are two CX instructions: `cx(0, 1)` and `cx(1, 2)`.

</details>

---

### Question 04 of 68

Which line correctly applies an S-dagger gate to qubit 0?

**A.**

`qc.s_dagger(0)`

**B.**

`qc.s(-1, 0)`

**C.**

`qc.sx(0).inverse()`

**D.**

`qc.sdg(0)`

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** D

**Explanation:** Qiskit's method name for S† is `sdg`.

</details>

---

### Question 05 of 68

**Select all correct answers.** You have a measurement-free circuit `qc`. Which snippets correctly obtain either the operator object or its matrix representation?

**A.**

```python
from qiskit.quantum_info import Operator
U = Operator(qc)
```

**B.**

```python
U = qc.operator()
```

**C.**

```python
from qiskit.quantum_info import Operator
U_matrix = Operator(qc).data
```

**D.**

```python
from qiskit import Operator
U = Operator.from_circuit(qc)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answers:** A, C

**Explanation:** `qiskit.quantum_info.Operator(qc)` constructs the operator for a unitary circuit, and `.data` gives its matrix. `qc.operator()` and `qiskit.Operator.from_circuit` are not the standard Qiskit SDK calls.

</details>

---

### Question 06 of 68

You want the final statevector for a circuit that has no measurements. Which code is correct?

**A.**

```python
from qiskit.quantum_info import Statevector
psi = Statevector.from_instruction(qc)
```

**B.**

```python
psi = qc.run_statevector()
```

**C.**

```python
from qiskit import Statevector
psi = qc.statevector()
```

**D.**

```python
psi = qc.measure_all()
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** A

**Explanation:** `Statevector.from_instruction(qc)` is the standard Qiskit SDK way to simulate the statevector of an instruction/circuit without measurement.

</details>

---

### Question 07 of 68

This circuit is prepared:

```python
from qiskit import QuantumCircuit
qc = QuantumCircuit(1)
qc.x(0)
qc.h(0)
```

Which state should `Statevector.from_instruction(qc)` represent?

**A.**

`|0>`

**B.**

`(|0> + |1>)/sqrt(2)`

**C.**

`(|0> - |1>)/sqrt(2)`

**D.**

`|1>`

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** C

**Explanation:** `X|0> = |1>`, and `H|1> = (|0> - |1>)/sqrt(2)`.

</details>

---

### Question 08 of 68

Which code correctly creates a Pauli operator for the observable `0.5 * ZZ - 1.2 * IX`?

**A.**

```python
from qiskit import SparsePauliOp
obs = SparsePauliOp([("ZZ", 0.5), ("IX", -1.2)])
```

**B.**

```python
from qiskit.quantum_info import SparsePauliOp
obs = SparsePauliOp.from_list([("ZZ", 0.5), ("IX", -1.2)])
```

**C.**

```python
obs = PauliSumOp("0.5 ZZ - 1.2 IX")
```

**D.**

```python
obs = SparsePauliOp.from_list([(0.5, "ZZ"), (-1.2, "IX")])
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** B

**Explanation:** `SparsePauliOp.from_list` takes `(pauli_string, coefficient)` pairs.

</details>

---

### Question 09 of 68

Which code calculates the expectation value of `ZZ` on a Bell circuit `qc` that has no final measurements?

**A.**

```python
from qiskit.primitives import StatevectorSampler
value = StatevectorSampler().run([(qc, "ZZ")]).result()[0]
```

**B.**

```python
value = qc.measure("ZZ")
```

**C.**

```python
from qiskit.quantum_info import Statevector, SparsePauliOp
psi = Statevector.from_instruction(qc)
obs = SparsePauliOp.from_list([("ZZ", 1.0)])
value = psi.expectation_value(obs)
```

**D.**

```python
from qiskit.quantum_info import SparsePauliOp
obs = SparsePauliOp.from_list([("ZZ", 1.0)])
value = qc.expectation_value(obs)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** C

**Explanation:** For exact statevector evaluation, build the statevector and call `expectation_value` with a `SparsePauliOp`.

</details>

---

### Question 10 of 68

**Select all correct answers.** A circuit `qc` already contains final measurements. You want a measurement-free copy while keeping the original `qc` unchanged. Which snippets accomplish that?

**A.**

```python
qc_nom = qc.remove_final_measurements(inplace=False)
```

**B.**

```python
qc.remove_final_measurements(inplace=True)
qc_nom = qc
```

**C.**

```python
qc_nom = qc.measure_all(inplace=False)
```

**D.**

```python
qc_nom = qc.copy()
qc_nom.remove_final_measurements(inplace=True)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answers:** A, D

**Explanation:** `inplace=False` returns a modified copy. Copying first and then removing final measurements in place also preserves the original circuit. Option B mutates the original, and option C adds measurements instead of removing them.

</details>

---

### Question 11 of 68

What is the correct Qiskit bitstring meaning for this one-qubit circuit?

```python
qc = QuantumCircuit(1, 1)
qc.x(0)
qc.measure(0, 0)
```

If sampled ideally, the dominant count key is:

**A.**

`1` as an integer only

**B.**

`'10'`

**C.**

`'1'`

**D.**

`'0'`

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** C

**Explanation:** The X gate flips `|0>` to `|1>`, so measuring the only qubit gives bitstring `'1'`.

</details>

---

### Question 12 of 68

Which line draws a circuit as a Matplotlib figure?

**A.**

`qc.plot(output="mpl")`

**B.**

`qc.draw(style="matplotlib")`

**C.**

`qc.mpl()`

**D.**

`qc.draw(output="mpl")`

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** D

**Explanation:** `QuantumCircuit.draw(output="mpl")` requests Matplotlib output.

</details>

---

### Question 13 of 68

Which code gets a text drawing string for a circuit?

**A.**

```python
drawing = qc.text_diagram()
```

**B.**

```python
drawing = qc.draw("ascii=False")
```

**C.**

```python
drawing = qc.draw(output="text")
```

**D.**

```python
drawing = str(qc.draw(output="mpl"))
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** C

**Explanation:** `output="text"` is the text-circuit drawer.

</details>

---

### Question 14 of 68

Which code plots a histogram from a counts dictionary named `counts`?

**A.**

```python
from qiskit.visualization import plot_state_qsphere
plot_state_qsphere(counts)
```

**B.**

```python
from qiskit import plot_histogram
plot_histogram(qc)
```

**C.**

```python
from qiskit.visualization import plot_histogram
plot_histogram(counts)
```

**D.**

```python
counts.plot_histogram()
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** C

**Explanation:** `plot_histogram` is imported from `qiskit.visualization` and takes count-like data.

</details>

---

### Question 15 of 68

What does the following code return ideally?

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(1)
qc.h(0)
Statevector.from_instruction(qc).probabilities_dict()
```

**A.**

`{'0': 1.0}`

**B.**

`{'1': 1.0}`

**C.**

`{'0': 0.5, '1': 0.5}`

**D.**

`{'00': 0.5, '11': 0.5}`

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** C

**Explanation:** A Hadamard on `|0>` prepares `|+>`, giving equal probabilities for `0` and `1`.

</details>

---

### Question 16 of 68

Which code gets the exact probabilities of all computational-basis outcomes from a measurement-free circuit `qc`?

**A.**

```python
from qiskit.quantum_info import Statevector
probs = Statevector.from_instruction(qc).probabilities_dict()
```

**B.**

```python
from qiskit.visualization import plot_histogram
probs = plot_histogram(qc)
```

**C.**

```python
probs = qc.get_counts()
```

**D.**

```python
probs = qc.probabilities_dict()
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** A

**Explanation:** The exact statevector object provides `probabilities_dict()`.

</details>

---

### Question 17 of 68

For this circuit, what is the ideal statevector probability dictionary?

```python
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(2)
qc.x(0)
Statevector.from_instruction(qc).probabilities_dict()
```

**A.**

`{'10': 1.0}`

**B.**

`{'01': 1.0}`

**C.**

`{'00': 1.0}`

**D.**

`{'1': 1.0}`

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** B

**Explanation:** Qiskit displays bitstrings with the highest-index qubit on the left, so X on qubit 0 gives `|01>`.

</details>

---

### Question 18 of 68

Which code visualizes the statevector `psi` on a Bloch sphere for each qubit?

**A.**

```python
from qiskit.visualization import plot_bloch_multivector
plot_bloch_multivector(psi)
```

**B.**

```python
psi.draw(output="bloch")
```

**C.**

```python
from qiskit.visualization import plot_histogram
plot_histogram(psi)
```

**D.**

```python
from qiskit.visualization import circuit_drawer
circuit_drawer(psi)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** A

**Explanation:** `plot_bloch_multivector` is the Qiskit visualization helper for statevector Bloch views.

</details>

---

### Question 19 of 68

Which code adds a measurement to every qubit and creates a classical register automatically?

**A.**

```python
qc.add_measurements()
```

**B.**

```python
qc.measure(qc.qubits)
```

**C.**

```python
qc.measure_all()
```

**D.**

```python
qc.measure_each()
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** C

**Explanation:** `measure_all()` measures every qubit and creates classical bits/registers if needed.

</details>

---

### Question 20 of 68

Which code creates a one-parameter RX circuit?

**A.**

```python
from qiskit import QuantumCircuit
qc = QuantumCircuit(1)
qc.rx(Parameter("theta"))
```

**B.**

```python
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

theta = Parameter("theta")
qc = QuantumCircuit(1)
qc.rx(theta, 0)
```

**C.**

```python
from qiskit import QuantumCircuit
theta = "theta"
qc = QuantumCircuit(1)
qc.rx(theta, 0)
```

**D.**

```python
qc = QuantumCircuit(Parameter("theta"), 1)
qc.rx(theta, 0)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** B

**Explanation:** Qiskit parameters are `Parameter` objects, and `rx` needs the angle and qubit index.

</details>

---

### Question 21 of 68

You have this circuit:

```python
theta = Parameter("theta")
qc = QuantumCircuit(1)
qc.ry(theta, 0)
```

Which code returns a new circuit with `theta = 0.3` while leaving `qc` unchanged?

**A.**

```python
bound = qc.assign_parameters(theta=0.3)
```

**B.**

```python
qc.assign_parameters({theta: 0.3}, inplace=True)
bound = qc
```

**C.**

```python
bound = qc.assign_parameters({theta: 0.3}, inplace=False)
```

**D.**

```python
bound = qc.bind({theta: 0.3})
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** C

**Explanation:** `assign_parameters(..., inplace=False)` returns a bound copy.

</details>

---

### Question 22 of 68

Which code creates three independent parameters named `x[0]`, `x[1]`, and `x[2]` and uses them in RX gates?

**A.**

```python
from qiskit.circuit import ParameterVector
x = ParameterVector("x", 3)
qc = QuantumCircuit(3)
for i in range(3):
    qc.rx(x[i], i)
```

**B.**

```python
x = Parameter("x", 3)
qc = QuantumCircuit(3)
qc.rx(x, [0, 1, 2])
```

**C.**

```python
x = ParameterVector("x")
qc = QuantumCircuit(3)
qc.rx(x, range(3))
```

**D.**

```python
x = ["x0", "x1", "x2"]
qc = QuantumCircuit(3)
for i in range(3):
    qc.rx(x[i], i)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** A

**Explanation:** `ParameterVector("x", 3)` creates indexed symbolic parameters usable in parameterized gates.

</details>

---

### Question 23 of 68

**Select all correct answers.** You have a two-qubit subcircuit `sub` and a three-qubit circuit `qc`. Which snippets correctly insert the subcircuit operations onto qubits 1 and 2 of `qc`?

**A.**

```python
qc.compose(sub, wires=[1, 2], inplace=True)
```

**B.**

```python
qc.compose(sub, qubits=[1, 2], inplace=True)
```

**C.**

```python
qc.append(sub, control=1, target=2)
```

**D.**

```python
gate = sub.to_gate()
qc.append(gate, [1, 2])
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answers:** B, D

**Explanation:** `compose(..., qubits=[1, 2], inplace=True)` inserts the subcircuit directly. Converting the subcircuit to a gate and appending it to `[1, 2]` also adds the same logical block, though it appears as a single gate instruction unless decomposed.

</details>

---

### Question 24 of 68

Which code composes `block` onto qubits `[2, 0]` of `qc` in place?

**A.**

```python
qc.append(block, qubits=[2, 0], inplace=True)
```

**B.**

```python
qc.merge(block, qubits=[2, 0])
```

**C.**

```python
qc.compose(block, qubits=[2, 0], inplace=True)
```

**D.**

```python
qc.compose(block, wires=[2, 0])
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** C

**Explanation:** `compose(..., qubits=[...], inplace=True)` composes another circuit/instruction into the chosen qubit positions.

</details>

---

### Question 25 of 68

Which code creates a controlled version of a one-qubit gate object `g` and appends it with control qubit 0 and target qubit 1?

**A.**

```python
qc.append(g.controlled, [0, 1])
```

**B.**

```python
cg = g.make_controlled()
qc.append(cg, control=0, target=1)
```

**C.**

```python
qc.control(g, 0, 1)
```

**D.**

```python
cg = g.control(1)
qc.append(cg, [0, 1])
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** D

**Explanation:** Most Qiskit gate objects support `.control(1)`, and the appended qubit order is `[control, target]` for a singly controlled one-qubit gate.

</details>

---

### Question 26 of 68

Which code resets qubit 0 before reusing it?

**A.**

`qc.measure(0)`

**B.**

`qc.reset(0)`

**C.**

`qc.reinitialize(0)`

**D.**

`qc.clear_qubit(0)`

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** B

**Explanation:** `reset` returns a qubit to `|0>` for later circuit use.

</details>

---

### Question 27 of 68

Which code creates the inverse of a measurement-free circuit `qc`?

**A.**

`qc_inv = qc.dagger()`

**B.**

`qc_inv = inverse(qc)`

**C.**

`qc_inv = qc.inverse()`

**D.**

`qc_inv = qc.adjoint(inplace=False)`

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** C

**Explanation:** `QuantumCircuit.inverse()` returns the inverse circuit when the circuit instructions are invertible.

</details>

---

### Question 28 of 68

**Select all correct answers.** Which snippets build a dynamic circuit that measures qubit 0 and applies `X` to qubit 1 only when the one-bit classical result is 1?

**A.**

```python
q = QuantumRegister(2, "q")
c = ClassicalRegister(1, "c")
qc = QuantumCircuit(q, c)
qc.h(q[0])
qc.measure(q[0], c[0])
with qc.if_test((c, 1)):
    qc.x(q[1])
```

**B.**

```python
qc = QuantumCircuit(2, 1)
qc.h(0)
qc.measure(0, 0)
if qc.clbits[0] == 1:
    qc.x(1)
```

**C.**

```python
qc = QuantumCircuit(2, 1)
qc.h(0)
qc.measure(0, 0)
qc.x(1).c_if(0, 1)
```

**D.**

```python
q = QuantumRegister(2, "q")
c = ClassicalRegister(1, "c")
qc = QuantumCircuit(q, c)
qc.h(q[0])
qc.measure(q[0], c[0])
with qc.if_test((c[0], 1)):
    qc.x(q[1])
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answers:** A, D

**Explanation:** Qiskit dynamic circuits encode hardware-time branching with circuit control-flow operations such as `if_test`. The condition can refer to the one-bit register or to the measured classical bit. Python `if` executes while constructing the circuit, not during the quantum run.

</details>

---

### Question 29 of 68

Which code correctly creates an if/else block: apply `X(0)` when classical register `c == 1`; otherwise apply `Z(0)`?

**A.**

```python
if c == 1:
    qc.x(0)
else:
    qc.z(0)
```

**B.**

```python
with qc.if_test((c, 1)) as else_:
    qc.x(0)
with else_:
    qc.z(0)
```

**C.**

```python
with qc.if_else((c, 1)):
    qc.x(0)
else:
    qc.z(0)
```

**D.**

```python
qc.if_test(c == 1, qc.x(0), qc.z(0))
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** B

**Explanation:** The context-manager form can expose `else_`, which is then used in a second `with` block.

</details>

---

### Question 30 of 68

**Select all correct answers.** Which `switch`/`case` snippets are valid Qiskit circuit-builder patterns?

**A.**

```python
with qc.switch(c) as case:
    with case(0):
        qc.x(0)
    with case(1):
        qc.z(0)
    with case(case.DEFAULT):
        qc.h(0)
```

**B.**

```python
with qc.switch(c) as case:
    with case(0, 3):
        qc.x(0)
    with case(1):
        qc.z(0)
    with case(case.DEFAULT):
        qc.h(0)
```

**C.**

```python
switch c:
    case 0:
        qc.x(0)
```

**D.**

```python
qc.switch(c, {0: qc.x(0), 1: qc.z(0)})
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answers:** A, B

**Explanation:** Qiskit uses the context-manager form `with qc.switch(...) as case:`. A case can contain one value or several values, and `case.DEFAULT` can define the default branch. Python's `switch` syntax and a dictionary-style shortcut are not Qiskit circuit-builder syntax.

</details>

---

### Question 31 of 68

Which code repeats `X(0)` three times as a circuit-level `for_loop` operation?

**A.**

```python
for _ in range(3):
    qc.for_loop(qc.x(0))
```

**B.**

```python
with qc.loop(3):
    qc.x(0)
```

**C.**

```python
qc.repeat(3, qc.x(0))
```

**D.**

```python
with qc.for_loop(range(3)):
    qc.x(0)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** D

**Explanation:** `with qc.for_loop(range(3)):` creates a circuit-level loop operation containing the body.

</details>

---

### Question 32 of 68

**Select all correct answers.** You want a backend-compatible circuit before using Runtime V2 primitives on IBM hardware. Which snippets are reasonable Qiskit SDK patterns?

**A.**

```python
isa_circuit = backend.compile(qc, isa=True)
```

**B.**

```python
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(qc)
```

**C.**

```python
from qiskit import transpile

isa_circuit = transpile(qc, backend=backend, optimization_level=1)
```

**D.**

```python
isa_circuit = qc.to_isa(backend)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answers:** B, C

**Explanation:** The preset pass manager is the commonly recommended Runtime V2 pattern for producing an ISA circuit. The `transpile` helper is also a valid Qiskit SDK way to target a backend. The other two APIs are not standard circuit methods.

</details>

---

### Question 33 of 68

Which import is correct for IBM Runtime Sampler V2?

**A.**

```python
from qiskit import SamplerV2 as Sampler
```

**B.**

```python
from qiskit_ibm_runtime import SamplerV2 as Sampler
```

**C.**

```python
from qiskit.runtime import IBMRuntimeSampler
```

**D.**

```python
from qiskit.providers.ibm import SamplerV2
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** B

**Explanation:** IBM Runtime V2 primitives are imported from `qiskit_ibm_runtime`.

</details>

---

### Question 34 of 68

Which code submits two already-transpiled circuits to a Runtime Sampler V2 object `sampler` with 1024 shots each?

**A.**

```python
job = sampler.submit([isa_circuit1, isa_circuit2], shots=1024)
```

**B.**

```python
job = sampler.run([isa_circuit1, isa_circuit2], shots=1024)
```

**C.**

```python
job = sampler.run(isa_circuit1, isa_circuit2, shots=1024)
```

**D.**

```python
job = sampler.run(circuits=[isa_circuit1, isa_circuit2], nshots=1024)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** B

**Explanation:** Sampler V2 `run` accepts an iterable of circuits or PUBs; `shots` can be supplied to `run`.

</details>

---

### Question 35 of 68

Which code uses different shot counts for two Sampler V2 PUBs that have no parameter values?

**A.**

```python
job = sampler.run([
    (isa_circuit1, None, 512),
    (isa_circuit2, None, 2048),
])
```

**B.**

```python
job = sampler.run([isa_circuit1, isa_circuit2], shots=[512, 2048])
```

**C.**

```python
job = sampler.run([(512, isa_circuit1), (2048, isa_circuit2)])
```

**D.**

```python
job = sampler.run([
    (isa_circuit1, 512),
    (isa_circuit2, 2048),
])
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** A

**Explanation:** A Sampler V2 PUB can be `(circuit, parameter_values, shots)`; use `None` when there are no parameter values.

</details>

---

### Question 36 of 68

Which code selects the least-busy operational non-simulator backend from a configured IBM Quantum service?

**A.**

```python
backend = service.least_busy(operational=True, simulator=False)
```

**B.**

```python
backend = service.get_least_busy(device=True)
```

**C.**

```python
backend = least_busy(service.backends())
```

**D.**

```python
backend = service.backend("least_busy")
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** A

**Explanation:** `QiskitRuntimeService.least_busy` supports filters such as `operational=True` and `simulator=False`.

</details>

---

### Question 37 of 68

You have a parameterized circuit `qc` with parameter `theta`. Which Sampler V2 PUB gives two parameter values and 1000 shots?

**A.**

```python
pub = (qc, 1000, [[0.1], [0.2]])
```

**B.**

```python
pub = (qc, [theta], [0.1, 0.2], 1000)
```

**C.**

```python
pub = (qc, [[0.1], [0.2]], 1000)
```

**D.**

```python
pub = (qc, {"theta": [0.1, 0.2]}, 1000)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** C

**Explanation:** In V2 PUB style, parameter values are passed as the second tuple element and shots as the third.

</details>

---

### Question 38 of 68

Which code pattern is preferred in Qiskit 2.x instead of old-style `execute(qc, backend)`?

**A.**

```python
job = qc.execute(backend, shots=1024)
```

**B.**

```python
job = backend.execute(qc, shots=1024)
```

**C.**

```python
from qiskit import execute
job = execute(qc, backend, shots=1024)
```

**D.**

```python
# Use primitives or backend.run on transpiled circuits, depending on workflow.
job = sampler.run([isa_circuit], shots=1024)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** D

**Explanation:** For v2-style Qiskit workflows, use primitives such as Sampler/Estimator or backend execution workflows rather than the old global `execute` helper.

</details>

---

### Question 39 of 68

**Select all correct answers.** Which snippets correctly create or configure a Runtime Estimator V2 object with resilience level 1?

**A.**

```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator

estimator = Estimator(mode=backend)
estimator.options.resilience_level = 1
```

**B.**

```python
from qiskit import EstimatorV2

estimator = EstimatorV2(backend)
estimator.set_resilience(1)
```

**C.**

```python
estimator = backend.estimator()
estimator.resilience = True
```

**D.**

```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator

estimator = Estimator(mode=backend, options={"resilience_level": 1})
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answers:** A, D

**Explanation:** Runtime V2 primitives are imported from `qiskit_ibm_runtime`. `resilience_level` can be set after construction through `estimator.options` or supplied as an initialization option.

</details>

---

### Question 40 of 68

For a circuit `qc` containing dynamic control flow, which statement is the best programming check before running it on hardware?

**A.**

`Check that the selected backend target supports the instructions/control flow used by the circuit, then transpile appropriately.`

**B.**

`Dynamic circuits never require backend support checks.`

**C.**

`Remove all classical registers, because hardware only accepts quantum bits.`

**D.**

`Convert every if/else into Python if/else before submission.`

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** A

**Explanation:** Dynamic circuits are hardware/backend capability dependent, so you should check support and use a compatible transpilation/runtime path.

</details>

---

### Question 41 of 68

**Select all correct answers.** Which snippets use a Runtime `Session` so several primitive calls can share the same execution context?

**A.**

```python
from qiskit_ibm_runtime import Session, SamplerV2 as Sampler

with Session(backend=backend) as session:
    sampler = Sampler(mode=session)
    job = sampler.run([isa_circuit], shots=1024)
```

**B.**

```python
sampler = Sampler(session=True, backend=backend)
job = sampler.run(qc)
```

**C.**

```python
with backend.session() as session:
    job = session.run(qc)
```

**D.**

```python
from qiskit_ibm_runtime import Session, EstimatorV2 as Estimator

with Session(backend=backend) as session:
    estimator = Estimator(mode=session)
    job = estimator.run([(isa_circuit, isa_observable)])
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answers:** A, D

**Explanation:** A Runtime session is created with `Session(...)`, and V2 primitives use that session through their `mode` argument. This works for Sampler V2 and Estimator V2 workflows.

</details>

---

### Question 42 of 68

Which code uses the local `StatevectorSampler` to sample a measured circuit `qc`?

**A.**

```python
from qiskit.primitives import Sampler

sampler = Sampler()
result = sampler(qc, shots=1024)
```

**B.**

```python
from qiskit.primitives import StatevectorSampler

sampler = StatevectorSampler()
job = sampler.run([qc], shots=1024)
result = job.result()
```

**C.**

```python
from qiskit.quantum_info import Statevector

result = StatevectorSampler(qc, shots=1024)
```

**D.**

```python
sampler = qc.sampler()
result = sampler.run(shots=1024)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** B

**Explanation:** `StatevectorSampler` is a local primitive; `run` takes a list of circuits/PUBs and a shot count.

</details>

---

### Question 43 of 68

**Select all correct answers.** A measured circuit used the default register created by `measure_all()`. Which snippets get counts from the first Sampler V2 result?

**A.**

```python
pub_result = job.result()[0]
counts = pub_result.data.meas.get_counts()
```

**B.**

```python
result = job.result()
counts = result[0].data.meas.get_counts()
```

**C.**

```python
counts = job.result().get_counts(qc)
```

**D.**

```python
counts = job.result()[0].quasi_dists[0]
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answers:** A, B

**Explanation:** Sampler V2 results are indexed by submitted circuit/PUB, and bit arrays are stored under the classical register name. The default `measure_all()` register is `meas`, so `data.meas.get_counts()` is the expected access pattern.

</details>

---

### Question 44 of 68

Your circuit has an explicit classical register named `alpha`. Which code is the most likely Sampler V2 result-access pattern?

**A.**

```python
counts = job.result()[0].data.alpha.get_counts()
```

**B.**

```python
counts = job.result()[0].get_counts("alpha")
```

**C.**

```python
counts = job.result().alpha_counts()
```

**D.**

```python
counts = job.result()[0].data.meas.get_counts()
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** A

**Explanation:** Sampler V2 organizes data by classical register name; a register named `alpha` is accessed as `data.alpha`.

</details>

---

### Question 45 of 68

Which Sampler V2 code requests per-shot bitstrings instead of aggregated counts, assuming the register name is `meas`?

**A.**

```python
bitstrings = job.result().get_bitstrings(qc)
```

**B.**

```python
bitstrings = job.result()[0].data.meas.get_bitstrings()
```

**C.**

```python
bitstrings = job.result()[0].get_memory()
```

**D.**

```python
bitstrings = job.result()[0].data.meas.bitstrings
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** B

**Explanation:** The V2 bit-array object provides convenience methods such as `get_bitstrings()`.

</details>

---

### Question 46 of 68

You want to sample three circuits with the same shot count using `StatevectorSampler`. Which code is correct?

**A.**

```python
sampler = StatevectorSampler()
job = sampler.run([qc1, qc2, qc3], shots=500)
```

**B.**

```python
sampler = StatevectorSampler()
job = sampler.run(qc1, qc2, qc3, shots=500)
```

**C.**

```python
sampler = StatevectorSampler(shots=500)
job = sampler.run(qc1 + qc2 + qc3)
```

**D.**

```python
job = StatevectorSampler.run([qc1, qc2, qc3], 500)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** A

**Explanation:** `run` takes a list/iterable of circuits or PUBs; `shots` can be passed as a keyword.

</details>

---

### Question 47 of 68

Which code correctly samples a parameterized circuit `qc` with two parameter-value rows using `StatevectorSampler`?

**A.**

```python
job = StatevectorSampler().run(qc, [[0.0], [3.14159]], 1000)
```

**B.**

```python
sampler = StatevectorSampler()
job = sampler.run([qc], parameters=[0.0, 3.14159], shots=1000)
```

**C.**

```python
job = StatevectorSampler().run([(qc, 1000, [[0.0], [3.14159]])])
```

**D.**

```python
sampler = StatevectorSampler()
job = sampler.run([(qc, [[0.0], [3.14159]])], shots=1000)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** D

**Explanation:** The PUB tuple places parameter values second: `(circuit, parameter_values)`; `shots` may be given to `run`.

</details>

---

### Question 48 of 68

Which statement best describes the Sampler V2 output style in code?

**A.**

`It returns only a statevector and never includes counts.`

**B.**

`It returns V1-style quasi-probability dictionaries only.`

**C.**

`It returns shot samples organized by classical register names, with helpers such as get_counts().`

**D.**

`It returns expectation values in data.evs.`

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** C

**Explanation:** Sampler V2 is sample-oriented; Estimator V2 is expectation-value-oriented.

</details>

---

### Question 49 of 68

A circuit has no measurements. You want Sampler-style bitstring counts. What is the most direct fix?

**A.**

`Add measurements, for example with qc.measure_all(), before using the sampler.`

**B.**

`Use SparsePauliOp.from_list first.`

**C.**

`Call qc.remove_final_measurements(inplace=True).`

**D.**

`Use EstimatorV2, because it automatically adds measurements and returns counts.`

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** A

**Explanation:** Sampler-style counts require classical measurement outputs; `measure_all()` is a direct way to add them.

</details>

---

### Question 50 of 68

**Select all correct answers.** Which snippets can compute the expectation value of `Z` for a measurement-free one-qubit circuit `qc`?

**A.**

```python
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp

estimator = StatevectorEstimator()
obs = SparsePauliOp.from_list([("Z", 1.0)])
job = estimator.run([(qc, obs)])
ev = job.result()[0].data.evs
```

**B.**

```python
from qiskit.quantum_info import Statevector, SparsePauliOp

psi = Statevector.from_instruction(qc)
obs = SparsePauliOp.from_list([("Z", 1.0)])
ev = psi.expectation_value(obs)
```

**C.**

```python
from qiskit.primitives import StatevectorSampler

ev = StatevectorSampler().run([(qc, "Z")]).result()[0].data.evs
```

**D.**

```python
ev = qc.get_counts("Z")
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answers:** A, B

**Explanation:** `StatevectorEstimator` is the local primitive for Estimator-style expectation values. For exact simulation, `Statevector.from_instruction(qc).expectation_value(obs)` is also valid. Sampler-style workflows return samples/counts, not `evs`.

</details>

---

### Question 51 of 68

Which Estimator V2 PUB format is correct for a parameterized circuit?

**A.**

`(parameter_values, circuit, observables, shots)`

**B.**

`(circuit, observables, parameter_values)`

**C.**

`(circuit, shots, observables)`

**D.**

`(observables, circuit, parameter_values)`

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** B

**Explanation:** Estimator V2 PUBs are circuit first, then observables, then optional parameter values/precision.

</details>

---

### Question 52 of 68

**Select all correct answers.** You transpiled a circuit to `isa_circuit` before Estimator V2 execution. Which snippets correctly address observable layout alignment?

**A.**

```python
isa_obs = obs.apply_layout(isa_circuit.layout)
```

**B.**

```python
isa_obs = obs.transpile(isa_circuit)
```

**C.**

```python
isa_obs = obs.apply_layout(isa_circuit.layout, num_qubits=isa_circuit.num_qubits)
```

**D.**

```python
isa_obs = isa_circuit.layout.apply(obs)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answers:** A, C

**Explanation:** After layout-changing transpilation, apply the circuit layout to the observable using `SparsePauliOp.apply_layout`. Supplying `num_qubits` is also valid when you need to control the final observable width.

</details>

---

### Question 53 of 68

Which code asks Runtime Estimator V2 for expectation values with target precision `0.05`?

**A.**

```python
job = estimator.estimate(isa_circuit, isa_observable, precision=0.05)
```

**B.**

```python
job = estimator.run(isa_circuit, isa_observable, error=0.05)
```

**C.**

```python
job = estimator.run([(isa_circuit, isa_observable)], precision=0.05)
```

**D.**

```python
job = estimator.run([(isa_circuit, isa_observable)], shots=0.05)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** C

**Explanation:** Estimator V2 supports a `precision` argument in `run` for target expectation-value precision.

</details>

---

### Question 54 of 68

Which code constructs a Hamiltonian `H = 0.7 * ZZ + 0.2 * IX - 1.1 * ZI`?

**A.**

```python
H = PauliHamiltonian({"ZZ": 0.7, "IX": 0.2, "ZI": -1.1})
```

**B.**

```python
H = 0.7 * "ZZ" + 0.2 * "IX" - 1.1 * "ZI"
```

**C.**

```python
H = SparsePauliOp.from_list([
    (0.7, "ZZ"),
    (0.2, "IX"),
    (-1.1, "ZI"),
])
```

**D.**

```python
from qiskit.quantum_info import SparsePauliOp
H = SparsePauliOp.from_list([
    ("ZZ", 0.7),
    ("IX", 0.2),
    ("ZI", -1.1),
])
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** D

**Explanation:** `SparsePauliOp.from_list` uses `(label, coefficient)` tuples.

</details>

---

### Question 55 of 68

This circuit is prepared:

```python
qc = QuantumCircuit(1)
qc.x(0)
```

Which Estimator observable should give an ideal expectation value of `-1`?

**A.**

`SparsePauliOp.from_list([("Z", 1.0)])`

**B.**

`SparsePauliOp.from_list([("I", 1.0)])`

**C.**

`SparsePauliOp.from_list([("X", 1.0)])`

**D.**

`SparsePauliOp.from_list([("Z", -1.0)])`

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** A

**Explanation:** `X|0> = |1>`, and `<1|Z|1> = -1`.

</details>

---

### Question 56 of 68

**Select all correct answers.** Which snippets enable dynamical decoupling for Runtime Estimator V2 and select the `XpXm` sequence?

**A.**

```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator

estimator = Estimator(mode=backend)
estimator.options.dynamical_decoupling.enable = True
estimator.options.dynamical_decoupling.sequence_type = "XpXm"
```

**B.**

```python
from qiskit_ibm_runtime import SamplerV2 as Sampler

sampler = Sampler(mode=backend)
sampler.options.dynamical_decoupling = "XpXm"
```

**C.**

```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator

estimator = Estimator(
    mode=backend,
    options={"dynamical_decoupling": {"enable": True, "sequence_type": "XpXm"}},
)
```

**D.**

```python
estimator.options.resilience.zne.sequence_type = "XpXm"
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answers:** A, C

**Explanation:** Runtime Estimator options include a `dynamical_decoupling` options group. You can set its fields directly or provide the nested options dictionary when constructing the estimator.

</details>

---

### Question 57 of 68

**Select all correct answers.** Which snippets enable Pauli gate twirling for Runtime Estimator V2 and request 32 randomizations with 100 shots per randomization?

**A.**

```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator

estimator = Estimator(mode=backend)
estimator.options.twirling.enable_gates = True
estimator.options.twirling.num_randomizations = 32
estimator.options.twirling.shots_per_randomization = 100
```

**B.**

```python
estimator.options.resilience.pauli_twirling = (32, 100)
```

**C.**

```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator

estimator = Estimator(
    mode=backend,
    options={"twirling": {"enable_gates": True,
                          "num_randomizations": 32,
                          "shots_per_randomization": 100}},
)
```

**D.**

```python
estimator.options.resilience.zne.noise_factors = (32, 100)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answers:** A, C

**Explanation:** Pauli twirling is configured through the Estimator V2 `twirling` options group. It can be set field-by-field or supplied as a nested options dictionary.

</details>

---

### Question 58 of 68

**Select all correct answers.** Which snippets correctly enable Runtime Estimator measurement-error mitigation, with or without custom noise-learning settings?

**A.**

```python
estimator.options.resilience_level = 1
```

**B.**

```python
estimator.options.measurement_error_mitigation = "trex"
estimator.options.measurement_shots = 100
```

**C.**

```python
estimator.options.resilience.zne_mitigation = True
estimator.options.resilience.zne.noise_factors = (1, 3, 5)
```

**D.**

```python
estimator.options.resilience.measure_mitigation = True
estimator.options.resilience.measure_noise_learning.num_randomizations = 32
estimator.options.resilience.measure_noise_learning.shots_per_randomization = 100
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answers:** A, D

**Explanation:** Resilience level 1 enables readout-error mitigation at minimal mitigation cost. For explicit control, use `resilience.measure_mitigation` and the nested `measure_noise_learning` settings. ZNE controls a different mitigation family.

</details>

---

### Question 59 of 68

**Select all correct answers.** Which snippets enable zero-noise extrapolation with noise factors `(1, 3, 5)` and an exponential extrapolator?

**A.**

```python
estimator.options.zne = True
estimator.options.noise_factors = [1, 3, 5]
estimator.options.fit = "exp"
```

**B.**

```python
estimator.options.twirling.enable_gates = True
estimator.options.twirling.noise_factors = (1, 3, 5)
```

**C.**

```python
estimator.options.resilience.zne_mitigation = True
estimator.options.resilience.zne.noise_factors = (1, 3, 5)
estimator.options.resilience.zne.extrapolator = "exponential"
```

**D.**

```python
estimator.options.update(
    resilience={
        "zne_mitigation": True,
        "zne": {"noise_factors": (1, 3, 5), "extrapolator": "exponential"},
    }
)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answers:** C, D

**Explanation:** ZNE is controlled through `options.resilience.zne_mitigation`, and ZNE-specific settings live under `options.resilience.zne`. The options object also supports `update(**kwargs)`, which can be used with nested dictionaries.

</details>

---

### Question 60 of 68

You are testing your own mitigation method and want to turn off all built-in Runtime Estimator error mitigation and suppression. Which code is correct?

**A.**

```python
estimator.options.disable_mitigation = True
```

**B.**

```python
estimator.options.resilience_level = 0
```

**C.**

```python
estimator.options.resilience.measure_mitigation = None
estimator.options.resilience.zne_mitigation = None
```

**D.**

```python
estimator.options.twirling.enable_gates = False
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** B

**Explanation:** Runtime Estimator uses `resilience_level = 0` to turn off built-in error mitigation and suppression.

</details>

---

### Question 61 of 68

Which code creates a Runtime Estimator V2 configured with resilience level 2?

**A.**

```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator

estimator = Estimator(mode=backend, options={"resilience_level": 2})
```

**B.**

```python
from qiskit_ibm_runtime import SamplerV2 as Sampler

estimator = Sampler(mode=backend, options={"resilience_level": 2})
```

**C.**

```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator

estimator = Estimator(mode=backend)
estimator.resilience_level(2)
```

**D.**

```python
from qiskit_ibm_runtime import EstimatorV2 as Estimator

estimator = Estimator(mode=backend, mitigation=2)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** A

**Explanation:** Runtime V2 primitive options can be supplied during initialization; `resilience_level` is an Estimator option.

</details>

---

### Question 62 of 68

Which code requests Probabilistic Error Amplification (PEA) as the ZNE noise amplifier?

**A.**

```python
estimator.options.resilience.pea_mitigation = True
```

**B.**

```python
estimator.options.twirling.amplifier = "pea"
```

**C.**

```python
estimator.options.resilience.zne_mitigation = True
estimator.options.resilience.zne.amplifier = "pea"
```

**D.**

```python
estimator.options.resilience.measure_mitigation = True
estimator.options.resilience.measure_noise_learning.amplifier = "pea"
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** C

**Explanation:** PEA is selected as a ZNE amplifier, so ZNE must be enabled and `resilience.zne.amplifier` should be set to `"pea"`.

</details>

---

### Question 63 of 68

When ZNE is enabled, which code reads the extra ZNE data from the first Estimator V2 result?

**A.**

```python
zne_values = job.result().zne_values
zne_stds = job.result().zne_stds
```

**B.**

```python
pub_result = job.result()[0]
raw_by_factor = pub_result.data.evs_noise_factors
extrapolated = pub_result.data.evs_extrapolated
```

**C.**

```python
pub_result = job.result()[0]
raw_by_factor = pub_result.data.counts_noise_factors
extrapolated = pub_result.data.quasi_dists_extrapolated
```

**D.**

```python
raw_by_factor, extrapolated = estimator.get_zne_result(job)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** B

**Explanation:** V2 Estimator always returns `evs` and `stds`; with ZNE enabled, additional fields include values such as `evs_noise_factors` and `evs_extrapolated`.

</details>

---

### Question 64 of 68

Which code enables Probabilistic Error Cancellation (PEC) and sets a maximum overhead of 50?

**A.**

```python
estimator.options.resilience.zne_mitigation = True
estimator.options.resilience.zne.max_overhead = 50
```

**B.**

```python
estimator.options.pec = True
estimator.options.pec_overhead = 50
```

**C.**

```python
estimator.options.resilience_level = 3
estimator.options.resilience.max_overhead = 50
```

**D.**

```python
estimator.options.resilience.pec_mitigation = True
estimator.options.resilience.pec.max_overhead = 50
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** D

**Explanation:** PEC is controlled through `resilience.pec_mitigation`; PEC-specific settings such as `max_overhead` are configured under `resilience.pec`.

</details>

---

### Question 65 of 68

**Select all correct answers.** Which snippets export a Qiskit circuit `qc` to OpenQASM 3?

**A.**

```python
from qiskit import qasm3
qasm_text = qasm3.dumps(qc)
```

**B.**

```python
from qiskit import qasm3
with open("circuit.qasm", "w") as f:
    qasm3.dump(qc, f)
```

**C.**

```python
qasm_text = qc.qasm()
```

**D.**

```python
from qiskit.qasm2 import dumps
qasm_text = dumps(qc, version=3)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answers:** A, B

**Explanation:** `qiskit.qasm3.dumps(qc)` returns an OpenQASM 3 string, while `qiskit.qasm3.dump(qc, file_obj)` writes OpenQASM 3 to a file-like object. `qc.qasm()` is old OpenQASM 2-style usage and is not the Qiskit 2.x OpenQASM 3 export pattern.

</details>

---

### Question 66 of 68

Which code loads an OpenQASM 3 program string into a `QuantumCircuit` using Qiskit's qasm3 module?

**A.**

```python
from qiskit import qasm3
qc = qasm3.loads(program)
```

**B.**

```python
qc = QuantumCircuit.loads_qasm3(program)
```

**C.**

```python
qc = qasm3.load_string(program)
```

**D.**

```python
qc = QuantumCircuit.from_qasm_str(program, version=3)
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** A

**Explanation:** `qasm3.loads(program)` is the high-level function for loading an OpenQASM 3 string when the importer support is installed.

</details>

---

### Question 67 of 68

Which OpenQASM 3 snippet applies H to qubit 0 and CX from qubit 0 to qubit 1 using physical qubits?

**A.**

```qasm
OPENQASM 3.0;
h 0;
cx 0, 1;
```

**B.**

```qasm
OPENQASM 3.0;
include "stdgates.inc";
H(0);
CX(0, 1);
```

**C.**

```qasm
OPENQASM 3.0;
include "stdgates.inc";
h $0;
cx $0, $1;
```

**D.**

```qasm
OPENQASM 2.0;
include "qelib1.inc";
h q[0];
cx q[0], q[1];
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** C

**Explanation:** OpenQASM 3 physical qubits can be written with `$0`, `$1`, and standard gates come from `stdgates.inc`.

</details>

---

### Question 68 of 68

Which Qiskit code creates a circuit-level while loop that repeats a body while classical register `c` equals 0?

**A.**

```python
with qc.while_loop((c, 0)):
    qc.h(0)
    qc.measure(0, c[0])
```

**B.**

```python
qc.while_loop(c == 0, body=[qc.h(0), qc.measure(0, c[0])])
```

**C.**

```python
with qc.loop_while(c, 0):
    qc.h(0)
    qc.measure(0, c[0])
```

**D.**

```python
while c == 0:
    qc.h(0)
    qc.measure(0, c[0])
```

<details>
<summary><strong>Answer and explanation</strong></summary>

**Correct answer:** A

**Explanation:** Circuit-level while loops are represented with `with qc.while_loop((classical, value)):`; Python `while` would execute during circuit construction, not dynamically on the device.

</details>

---

---

## Review Mode: Full Answer Key

<details>
<summary><strong>Show full answer key</strong></summary>

> Multiple-response questions require all listed answers and no extra answers.

| Question | Answer |
|---:|:---:|
| 1 | C |
| 2 | C |
| 3 | B |
| 4 | D |
| 5 | A, C |
| 6 | A |
| 7 | C |
| 8 | B |
| 9 | C |
| 10 | A, D |
| 11 | C |
| 12 | D |
| 13 | C |
| 14 | C |
| 15 | C |
| 16 | A |
| 17 | B |

| Question | Answer |
|---:|:---:|
| 18 | A |
| 19 | C |
| 20 | B |
| 21 | C |
| 22 | A |
| 23 | B, D |
| 24 | C |
| 25 | D |
| 26 | B |
| 27 | C |
| 28 | A, D |
| 29 | B |
| 30 | A, B |
| 31 | D |
| 32 | B, C |
| 33 | B |
| 34 | B |

| Question | Answer |
|---:|:---:|
| 35 | A |
| 36 | A |
| 37 | C |
| 38 | D |
| 39 | A, D |
| 40 | A |
| 41 | A, D |
| 42 | B |
| 43 | A, B |
| 44 | A |
| 45 | B |
| 46 | A |
| 47 | D |
| 48 | C |
| 49 | A |
| 50 | A, B |
| 51 | B |

| Question | Answer |
|---:|:---:|
| 52 | A, C |
| 53 | C |
| 54 | D |
| 55 | A |
| 56 | A, C |
| 57 | A, C |
| 58 | A, D |
| 59 | C, D |
| 60 | B |
| 61 | A |
| 62 | C |
| 63 | B |
| 64 | D |
| 65 | A, B |
| 66 | A |
| 67 | C |
| 68 | A |

</details>

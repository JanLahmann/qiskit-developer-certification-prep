# IBM Qiskit 2.X | Practice Exam - 1

**Question 1:**  
Given an instance of `qiskit_ibm_runtime.EstimatorV2` called `estimator`, which resilience level enables Zero Noise Extrapolation (ZNE) and gate twirling as an error mitigation method?

○ A. `estimator.options.resilience_level = 1`  
○ B. `estimator.options.resilience_level = 0`  
○ C. `estimator.options.resilience_level = 2`  
○ D. `estimator.options.resilience_level = 3`

**Question 2:**  
Which one of the following patterns, expressed in terms of array broadcasting primitives, is represented by the given image?  
![Broadcasting Visualization](../Images/broadcasting.png)

○ A. Standard nd generalization  
○ B. Outer/Product  
○ C. Broadcast single observable  
○ D. Zip

**Question 3:**  
Applying the Qiskit `SdgGate` to a qubit in state `|1⟩` introduces which global phase?

○ A. π/2 phase  
○ B. π/4 phase  
○ C. -π/4 phase  
○ D. -π/2 phase

**Question 4:**  
Which one of the following code fragments will convert a `QuantumCircuit` object, named `circuit`, into an OpenQASM 3 **file output** in Qiskit?

○ A. `qiskit.qasm3.dumps(circuit)`  
○ B. `qiskit.qasm3.dump(circuit, file)`  
○ C. `qiskit.qasm3.to_qasm(circuit)`  
○ D. `qiskit.qasm3.export(circuit)`

**Question 5:**  
Given the following code fragment, what is the approximate probability that a measurement would result in a bit value of `0`?

```python
from qiskit import QuantumCircuit
import numpy as np

qc = QuantumCircuit(1)
qc.reset(0)
qc.rx(3 * np.pi / 4, 0)
qc.measure_all()
```

○ A. 0.1464  
○ B. 0.5  
○ C. 0.8536  
○ D. 1.0

**Question: 6**  
Which two of the following code fragments create a `QuantumCircuit` with 2 classical bits and 3 qubits?

○ A. `QuantumCircuit(2,3)`  
○ B. `QuantumCircuit(QuantumRegister(3, 'qr0'), QuantumRegister(2, 'qr1'))`  
○ C. `QuantumCircuit(QuantumRegister(3), ClassicalRegister(2))`  
○ D. `QuantumCircuit(3,2)`  
○ E. `QuantumCircuit(QuantumRegister(2, 'qr0'), QuantumRegister(3, 'qr1'))`

**Question 7:**  
Looking at the Bloch sphere visualization showing `|01⟩` and `|10⟩` states, which code would produce this quantum state?  
![QSphere State](../Images/qsphere.png)

○ A.  
`qc = QuantumCircuit(2)`  
`qc.x(1)`  
`qc.h(0)`  
`qc.cx(0, 1)`  
`state = Statevector(qc)`  
`plot_state_qsphere(state)`

○ B.  
`qc = QuantumCircuit(2)`  
`qc.h(0)`  
`qc.cx(0, 1)`  
`state = Statevector(qc)`  
`plot_state_qsphere(state)`

○ C.  
`qc = QuantumCircuit(2)`  
`qc.h(0)`  
`qc.z(0)`  
`qc.cx(0, 1)`  
`state = Statevector(qc)`  
`plot_state_qsphere(state)`

○ D.  
`qc = QuantumCircuit(2)`  
`qc.x(0)`  
`qc.x(1)`  
`qc.h(0)`  
`qc.cx(0, 1)`  
`state = Statevector(qc)`  
`plot_state_qsphere(state)`

**Question 8:**  
Which statement describes the expected behavior of the `QiskitRuntimeService.jobs` method?

○ A. It returns no jobs unless filtered by a specific criteria  
○ B. It retrieves all runtime jobs, subject to optional filtering  
○ C. It always retrieves all jobs submitted in the last 30 days (720 hours)  
○ D. It only returns all jobs submitted to the `ibm_foo` backend

**Question 9:**  
Which statement describes what the following line of OpenQASM 3 code does?

```qasm
uint[8] my_int;
```

○ A. Declare an unsigned 8-bit integer named my_int  
○ B. Declare a signed 8-bit integer named my_int  
○ C. Assign the 8th value of the list int to variable my_int  
○ D. Declare an integer named my_int with value 8

**Question 10:**  
A quantum circuit `qc` is initialized as follows:

```python
vector = np.sqrt([1/2, 1/2])
qc.initialize(vector, 0)
```

○ A. plot_bloch_vector([1, np.pi/2, 0],coord_type='spherical')  
○ B. plot_bloch_vector([0, 1, 0])  
○ C. plot_bloch_vector([0, 0, 1])  
○ D. plot_bloch_vector([1, 0, np.pi/2],coord_type='spherical')

**Question 11:**  
In which quantum state will the qubit be as a result of the following code?

```python
qc = QuantumCircuit(1)
qc.reset(0)
qc.h(0)
```

A. |−⟩  
B. |+⟩  
C. |0⟩  
D. |1⟩

**Question 12:**  
To which module do the following classes belong?

- `RemoveFinalReset`
- `SabreLayout`
- `BasisTranslator`

○ A. `qiskit.scheduler`  
○ B. `qiskit.circuit.library`  
○ C. `qiskit.transpiler.passes`  
○ D. `qiskit.providers.models`

**Question 13:**  
Which method should be used to retrieve the error message when debugging a failed Qiskit Runtime job?

○ A. `job.get_error()`  
○ B. `job.retrieve_error()`  
○ C. `job.error_message()`  
○ D. `job.error()`

**Question 14:**  
Given the code snippet, which one of the following is a valid way to invoke the `run` method on an instance of `SamplerV2`?

```python
from qiskit_ibm_runtime import SamplerV2
...
sampler = SamplerV2(...)
```

○ A. sampler.run(isa_circuit, observable)  
○ B. sampler.run(isa_circuit, backend, parameter)  
○ C. sampler.run([isa_circuit])  
○ D. sampler.run(backend, isa_circuit)

**Question 15:**  
Given the code fragment, which one of the following correctly connects to the `"ibm_foo"` backend?

```python
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService()
```

○ A. backend = service.get("ibm_foo")  
○ B. backend = "ibm_foo"  
○ C. backend = service.fetch_backend("ibm_foo")  
○ D. backend = service.backend("ibm_foo")

**Question 16:**  
Given a `ParameterVector` as defined below, which one of the following would find the position of `x` within `v`?

```python
from qiskit.circuit import ParameterVector
v = ParameterVector("v", 3)
x = v[1]
```

○ A. v.find(x)  
○ B. v.index(x)  
○ C. x.find_in(v)  
○ D. v.locate(x)

**Question 17:**  
Which one of the following code fragments will generate the given output?
[[0.+0.j 1.+0.j 0.+0.j 0.+0.j]
[ 1.+0.j 0.+0.j 0.+0.j 0.+0.j]
[ 0.+0.j 0.+0.j 0.+0.j -1.+0.j]
[ 0.+0.j 0.+0.j -1.+0.j 0.+0.j]]

○ A. `p = Pauli('ZX')`  
  `print(p.to_matrix())`

○ B. `p = Pauli('-IX')`  
  `print(p.to_matrix())`

○ C. `p = Pauli('-XX')`  
  `print(p.to_matrix())`

○ D. `p = Pauli('-XI')`  
  `print(p.to_matrix())`

**Question 18:**  
Given the following code fragment, which statement describes the `SamplerOptions` parameter `options.default_shots`?

```python
from qiskit_ibm_runtime import Sampler
sampler = Sampler(mode=backend)
sampler.options.default_shots = ...
```

○ A. The number of randomizations we apply to the circuit  
○ B. The number of times that we run the circuit  
○ C. The sum of the number of measurements in each qubit  
○ D. The number of sequences in dynamical decoupling

**Question 19:**  
**(Select 2)**  
Which two of the following Python objects are valid input to `plot_distribution`?

○ A. `[0, 1, 2], [500, 500, 500]`  
○ B. `{ 0: 500, 3: 500 }`  
○ C. `[(0, 500), (3, 500)]`  
○ D. `[{ 0: 500, 3: 500}, { 0: 500, 1: 500 }]`  
○ E. `{ 0: [300, 500], 1: [400, 500] }`

**Question 20:**  
Assuming all necessary imports have been completed, which one of the following is the shape of a `PubResult` named `result`?

```python
parameter_values = np.random.uniform(size=(5, ))
observables = [SparsePauliOp(pauli) for pauli in ["III", "XXX", "YYY", "ZZZ", "XYZ"]]
job = Estimator(mode=session).run([(circuit, observables, parameter_values)])
result = job.result()[0].data.evs
print(result.shape())
```

○ A. (5, 1)  
○ B. (5, 5)  
○ C. (1, 5)  
○ D. (5,)

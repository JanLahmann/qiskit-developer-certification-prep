#### 1. Labeling Pauli operators

Which code fragment constructs the Pauli operator $Z\otimes X$ (-Z on qubit 1, X on qubit 0) for a two-qubit system?

a) `p = Pauli('ZX')`  
b) `p = Pauli('XZ')`  
c) `p = Pauli('IZ')`  
d) `p = Pauli('XI')`  

---

#### 2. Square-root-of-X twice

A qubit is initialised in $|0\rangle$. The following Qiskit program is run:

```python
qc = QuantumCircuit(1)
qc.sx(0)
qc.sx(0)
qc.measure_all()
```

Which final *computational* state does this sequence prepare (ignoring global phase)?

a) $|+\rangle$  
b) $i\,|1\rangle$  
c) $|1\rangle$  
d) $|0\rangle$  

---

#### 3. Phase from an **S** gate

Applying `SGate` (`qc.s(0)`) to a qubit in state $|1\rangle$ introduces which global phase?

a) $+\frac{\pi}{2}$  
b) $-\frac{\pi}{2}$  
c) $+\pi$  
d) $-\pi$  

---

#### 4. Hadamard followed by Z

Consider

```python
qc = QuantumCircuit(1)
qc.h(0)
qc.z(0)
qc.measure_all()
```

What is the probability of measuring the classical bit `1`?

a) 0.25  
b) 0.50  
c) 0.75  
d) 1.00  

---

#### 5. Probabilities after an $R_x$ rotation

```python
qc = QuantumCircuit(1)
qc.rx(np.pi/3, 0)
qc.measure_all()
```

Approximately what is the probability of obtaining outcome `1`?

a) 0.25  
b) 0.50  
c) 0.75  
d) 0.866  

---

#### 6. Generating a Bell state

Which of the following code fragments prepares the Bell state $|\Phi^{+}\rangle = (|00\rangle+|11\rangle)/\sqrt{2}$?

a) `qc.h(0); qc.cx(0,1)`  
b) `qc.h(1); qc.cx(1,0)`  
c) `qc.x(0); qc.h(1); qc.cx(1,0)`  
d) `qc.h(0); qc.cz(0,1)`  

---

#### 7. Commutation of Pauli gates

Which pair of single-qubit Pauli operations **commute** with each other?

a) X and Z  
b) Y and Z  
c) X and X  
d) X and Y  

---

#### 8. Applying a Pauli-Y gate in Qiskit

Which code fragment applies a Pauli-Y operation to qubit 0 of an existing circuit `qc`?

a) `qc.sx(0)`  
b) `qc.y(0)`  
c) `qc.t(0)`  
d) `qc.rz(np.pi, 0)`  

---

#### 9. Draw a circuit with Matplotlib

Which call renders a `QuantumCircuit` named `qc` using Matplotlib?

a) `qc.draw(output="mpl")`  
b) `qc.plot("mpl")`  
c) `plot_circuit(qc, backend="mpl")`  
d) `qc.draw_mpl()`  

---

#### 10. Save a circuit diagram as a PNG

Which snippet correctly saves a Matplotlib circuit diagram to `circuit.png`?

a) `from qiskit.visualization import circuit_drawer; circuit_drawer(qc, output="mpl", filename="circuit.png")`  
b) `qc.draw(filename="circuit.png")`  
c) `qc.save(output="mpl", file="circuit.png")`  
d) `from qiskit.visualization import plot_histogram; plot_histogram(qc, filename="circuit.png")`  

---

#### 11. Visualize measurement outcomes

Given `counts = {"00": 520, "01": 504}`, which function produces a bar chart of these results?

a) `plot_state_city(counts)`  
b) `plot_histogram(counts)`  
c) `plot_bloch_multivector(counts)`  
d) `plot_state_qsphere(counts)`  

---

#### 12. Overlay two histograms

You have `counts_a` and `counts_b` from two circuits. Which call overlays them in one figure with a legend?

a) `plot_histogram(counts_a, counts_b, legend=["A","B"])`  
b) `plot_histogram([counts_a, counts_b], legend=["A","B"])`  
c) `plot_state_city([counts_a, counts_b], labels=["A","B"])`  
d) `plot_bloch_multivector([counts_a, counts_b], legend=["A","B"])`  

---

#### 13. Visualize a single-qubit pure state on the Bloch sphere

You computed `state = Statevector.from_label("0")`. Which call plots the state on a Bloch sphere?

a) `plot_state_qsphere(state)`  
b) `plot_state_city(state)`  
c) `plot_bloch_multivector(state)`  
d) `plot_histogram(state)`  

---

#### 14. Qsphere for equal superposition of two qubits

Which code produces a Qsphere with **four equally sized points of the same color** (equal amplitudes, zero relative phase)?

a)

```python
qc = QuantumCircuit(2); qc.h(0); qc.h(1)
state = Statevector.from_instruction(qc)
plot_state_qsphere(state)
```

b)

```python
qc = QuantumCircuit(2); qc.h(0); qc.z(0); qc.h(1)
state = Statevector.from_instruction(qc)
plot_state_qsphere(state)
```

c)

```python
qc = QuantumCircuit(2); qc.h(0); qc.h(1); qc.z(1)
state = Statevector.from_instruction(qc)
plot_state_qsphere(state)
```

d)

```python
qc = QuantumCircuit(2); qc.x(0); qc.x(1); qc.h(0); qc.h(1)
state = Statevector.from_instruction(qc)
plot_state_qsphere(state)
```

---

#### 15. Classical-control "if"

Which fragment applies an X gate on qubit 0 *only* when classical bit `c0` equals 1?

a)

```python
with qc.if_test((c0, 1)):
    qc.x(0)
```

b)

```python
qc.x(0).c_if(c0, 1)
```

c)

```python
if c0 == 1:
    qc.x(0)
```

d)

```python
qc.if_else(c0 == 1, qc.x(0))
```

---

#### 16. Creating a 3-parameter vector

How do you create three independent symbolic parameters all named θ?

a) `theta = Parameter('theta', 3)`  
b) `theta = ParameterVector('theta', 3)`  
c) `theta = ParameterVector(3, 'theta')`  
d) `theta = ParameterExpression('theta', 3)`  

---

#### 17. Binding a single value to a parameter

Given `theta = Parameter('θ')` and a circuit `qc` containing `rx(theta, 0)`, which call returns a **new** circuit with θ = π/4?

a) `qc.assign_parameters({theta: np.pi/4}, inplace=False)`  
b) `qc.bind_parameters({theta: np.pi/4})`  
c) `qc.assign(theta, np.pi/4)`  
d) `theta.bind(qc, np.pi/4)`  

---

#### 18. Repeating a block five times 

Which construct correctly repeats the enclosed operations five times in a dynamic circuit?

a)

```python
with qc.for_loop(range(5)):
    qc.cx(0, 1)
```

b)

```python
for _ in range(5):
    qc.cx(0, 1)
```

c)

```python
qc.repeat(5):
    qc.cx(0, 1)
```

d)

```python
qc.loop(5).cx(0, 1)
```

---

#### 19. Quick high-level transpilation

What single-line call compiles `qc` for a backend `backend` using the **highest built-in optimisation** level?

a) `transpile(qc, backend, optimization_level=3)`  
b) `qc.transpile(backend, 3)`  
c) `run_transpile(qc, backend, level='max')`  
d) `generate_preset_pass_manager(level=3).run(qc)`  

---

#### 20. Preset pass manager creation

Which function directly returns a pass manager equivalent to transpiler optimisation level 2 for a target backend?

a) `generate_preset_pass_manager(optimization_level=2, target=backend.target)`  
b) `PassManager.preset(backend, level=2)`  
c) `PresetPassManager(backend, 2)`  
d) `transpile(qc, backend, opt_level=2, return_passmanager=True)`  

---

#### 21. Controlling qubit layout manually

While building a circuit for a five-qubit device with coupling map `coupling`, which `transpile` argument lets you **fix physical qubit placement**?

a) `layout_method='trivial'`  
b) `initial_layout=[0,1,2,3,4]`  
c) `routing_method='sabre'`  
d) `backend_properties=coupling`  

---

#### 22. Creating a dynamic while-loop

Which snippet repeats the `foo` sub-circuit until the classical bit `flag` equals 1?

a)

```python
qc.while_loop((flag, 0), foo)
```

b)

```python
while flag == 0:
    qc.append(foo, qc.qubits)
```

c)

```python
with qc.while_loop((flag, 1)):
    qc.append(foo, qc.qubits)
```

d)

```python
qc.do_while(foo, until=(flag,1))
```

---

#### 23. Gate fusion by optimisation

After executing

```python
tqc = transpile(qc, backend, optimization_level=3)
```

you notice the depth is much smaller because consecutive single-qubit rotations were merged. Which **pass family** is mainly responsible?

a) **BasisTranslation** passes  
b) **CXCancellation** passes  
c) **Optimize1qGatesDecomposition** passes  
d) **CommutationAnalysis** passes  

---

#### 24. Identify a valid execution mode

Which option is an official job-execution mode in Qiskit Runtime?

a) *stream*  
b) *batch*  
c) *parallel*  
d) *single-shot*  

---

#### 25. Opening a dedicated session

Choose the call that opens a **dedicated** session on a backend stored in `backend`:

a)

```python
from qiskit_ibm_runtime import Session
session = Session(backend=backend)
```

b)

```python
session = Session(backend, mode="dedicated")
```

c)

```python
session = Session(backend); session.mode = "dedicated"
```

d)

```python
with Session(backend, dedicated=True) as session:
    ...
```

---

#### 26. Limiting how long a **Batch** session stays open

When you construct a `Batch` to run jobs in batch mode, which **keyword argument** lets you set the maximum time before the batch is forcibly closed?

a. `timeout`  
b. `max_time`  
c. `session_time`  
d. `runtime_limit`  

---

#### 27. Batch-mode behaviour

In *batch* mode, how are jobs queued?

a) Each job executes immediately in arrival order.  
b) Jobs wait and execute **only after you close the session or it times out**.  
c) Jobs are distributed across multiple backends simultaneously.  
d) Jobs execute one-by-one but with elevated priority.  

---

#### 28. Running a circuit with the Sampler primitive in a session

Which snippet correctly runs a list `circuits` on real hardware using **Sampler** inside an existing session `session`?

a)

```python
from qiskit_ibm_runtime import Sampler
sampler = Sampler(session=session)
job = sampler.run(circuits)
```

b)

```python
sampler = Sampler()
job = session.run(sampler, circuits)
```

c)

```python
job = Sampler.run(session, circuits)
```

d)

```python
job = session.sampler(circuits)
```

---

#### 29. Broadcasting parameter values

`circuits` contains two parameterised circuits. Which `parameter_values` array will **broadcast correctly** under Runtime rules?

a) shape (2, 3)  
b) shape (1, 3)  
c) shape (3, 2)  
d) shape (3, 3)  

*(Assume each circuit has three Parameters.)*

---

#### 30. Closing a session

What is the recommended way to end a session so that *batch* jobs are released to the queue?

a) `session.stop()`  
b) Exiting the `with Session(...):` context block  
c) `session.end_batch()`  
d) You do not need to do anything; sessions close automatically after 24 h  

---

#### 31. What does the `SamplerOptions` parameter **`options.default_shots`** specify?

a) The sum of measurement results on every qubit  
b) The number of randomisations applied to the circuit  
c) The number of times the circuit is executed (shots)  
d) The number of dynamical-decoupling sequences  

---

#### 32. To change the built-in error-mitigation strategy for every circuit an `Estimator` runs, which option should you set?

a) `options.dynamical_decoupling`  
b) `options.resilience_level`  
c) `options.meas_level`  
d) `options.optimization_level`  

---

#### 33. Which `Sampler` option lets you enable or configure dynamical-decoupling sequences during execution?

a) `options.dynamical_decoupling`  
b) `options.resilience_level`  
c) `options.default_shots`  
d) `options.bias_mitigation`  

---

#### 34. In Qiskit v2, which of the following is a *valid* call to execute sampling with **`Sampler.run()`**?

a) `sampler.run([circuit1, circuit2])` — returns a job object  
b) `sampler.run(distribution, circuit1)`  
c) `sampler.run(circuit1, distribution="gauss")`  
d) `sampler.run(shots=1024)`  

---

#### 35. If you omit the `shots` argument when calling `Sampler.run()`, how is the shot count chosen?

a) It falls back to the backend’s default shots  
b) It is auto-determined from circuit depth  
c) It uses the value of `options.default_shots` set on the `Sampler` instance  
d) It is fixed at 1024 shots

---

#### 36. What does a `Sampler` job **return** to the user?

a) A list of expectation values of observables  
b) Raw state-vector amplitudes  
c) A list of quasi-probability distributions over measured bit-strings  
d) Pulse-level schedules for each circuit  

---

#### 37. Choosing a built-in error-mitigation profile

Which `EstimatorOptions` field lets you pick one of Qiskit’s preset error-mitigation bundles (level 0, 1 or 2)?

a) `dynamical_decoupling`  
b) `default_precision`  
c) `resilience_level`  
d) `seed_estimator`  

---

#### 38. Effect of setting `default_shots`

When you set `estimator.options.default_shots`, what *immediate* consequence does the documentation state?

a) It ignores `resilience_level`  
b) It overrides any `default_precision` value  
c) It disables Pauli-twirling  
d) It forces precision to 1 / √shots  

---

#### 39. Precision-precedence hierarchy

For any Estimator PUB, which source of precision has the **highest** precedence if all four are supplied?

a) `estimator.options.default_precision`  
b) A `precision` keyword in `run()`  
c) The product `num_randomizations × shots_per_randomization` from twirling  
d) A precision value embedded directly in the PUB  

---

#### 40. Valid broadcasting shapes

The Estimator broadcasts observables and parameter sets like NumPy. Which pair below *will* broadcast? (O = observables shape, P = parameter\_values shape.)

a) O (3 × 1), P (100 × 2)  
b) O (3 × 1), P (1 × 100 × 2)  
c) O (5), P (3)  
d) O (2 × 1), P (6 × 5 × 4)  

---

#### 41. Allowed keyword arguments to `Estimator.run()`

Which call is **valid** for Estimator V2 according to the interface?

a) `estimator.run(pubs, precision=0.02)`  
b) `estimator.run(pubs, shots=4096)`  
c) `estimator.run(pubs, mode="priority")`  
d) `estimator.run(pubs, max_execution_time=60)`  

---

#### 42. Accessing expectation values

After the job completes, you write

```python
pub_result = job.result()[0]      # Estimator V2
```

Which attribute gives the array of expectation-value estimates?

a) `pub_result.evs`  
b) `pub_result.values`  
c) `pub_result.data.evs`  
d) `pub_result.data.values`  

---

#### 43. Filter jobs by session

Which one-liner returns **all runtime jobs that belong to a given session** whose ID is stored in the variable `sid`?

a) `service.jobs(session_id=sid)`  
b) `service.job(sid)`  
c) `service.jobs(filter_session=sid)`  
d) `service.jobs().filter(session=sid)`  

---

#### 44. Meaning of a final status

If `job.status()` returns `JobStatus.DONE`, what does this indicate?

a) The job is still queued.  
b) The job has run successfully, and results can be retrieved.  
c) The job was cancelled by the user.  
d) The job failed with an error.  

---

#### 45. Blocking a call that returns results

Which RuntimeJob method **blocks until the job finishes and then returns the result object**?

a) `job.result()`  
b) `job.queue_position()`  
c) `job.metrics()`  
d) `job.backend()`  

---

#### 46. Convert a quasi-distribution to a proper probability distribution

After a `Sampler` run, you have

```python
qpd = result.quasi_dists[0]  # a QuasiDistribution
```

Which call converts `qpd` to the *nearest* valid probability distribution?

a) `qpd.nearest_probability_distribution()`  
b) `qpd.to_counts()`  
c) `qpd.binary_probabilities()`  
d) `qpd.normalize()`  

---

#### 47. Persist results to JSON for later analysis

According to the IBM guide, which import pair should you use with Python’s `json` module when writing a Runtime result to disk?

a) `from qiskit_ibm_runtime import RuntimeEncoder, RuntimeDecoder`  
b) `from qiskit_ibm_runtime import ResultEncoder, ResultDecoder`  
c) `from qiskit.result import ResultEncoder, ResultDecoder`  
d) `import pickle as RuntimeEncoder`  

---

#### 48. Declaring an 8-bit classical register in OpenQASM 3

Which line is **valid** syntax?

a) `bit[8] c;`  
b) `creg c[8];`  
c) `bit c[8];`  
d) `uint8 c;`  

---

#### 49. Exporting a `QuantumCircuit` to an OpenQASM 3 string

Which function does Qiskit 2.x provide for this task?

a) `QuantumCircuit.qasm()`  
b) `qiskit.qasm3.dumps()`  
c) `qiskit.qasm3.export_string()`  
d) `qiskit.qasm2.dumps()`  

---

#### 50. Qiskit IBM Runtime REST API – running a job

According to the official REST spec, which HTTP verb and endpoint starts a new Runtime job?

a) `GET /v1/jobs`  
b) `POST /v1/jobs`  
c) `PUT /v1/job/run`  
d) `PATCH /v1/jobs/{id}`  

---


# Qiskit 2.X Certification Exam | Practice Exam - 1

## Answer Keys:

Question 1: C  
Question 2: A  
Question 3: D  
Question 4: B  
Question 5: A  
Question 6: C and D  
Question 7: D  
Question 8: B  
Question 9: A  
Question 10: A  
Question 11: B  
Question 12: C  
Question 13: C  
Question 14: C  
Question 15: D  
Question 16: B  
Question 17: A  
Question 18: B  
Question 19: B and D  
Question 20: D

## Detailed Solutions

## **Question 1: EstimatorV2 Resilience Levels**

**Question:** Given an instance of `qiskit_ibm_runtime.EstimatorV2` called `estimator`, which resilience level enables Zero Noise Extrapolation (ZNE) and gate twirling as an error mitigation method?

### Options Analysis:

#### **Option A: `resilience_level = 1`**

- Enables **Measurement Error Mitigation** only
- Uses readout error correction based on calibration data
- Does NOT include ZNE or gate twirling
- ❌ **Incorrect**

#### **Option B: `resilience_level = 0`**

- **No error mitigation** applied
- Raw results from quantum hardware
- ❌ **Incorrect**

#### **Option C: `resilience_level = 2`** ✓

- Enables **ZNE (Zero Noise Extrapolation)** AND **gate twirling**
- ZNE: Extrapolates to zero-noise limit by running circuits at different noise levels
- Gate twirling: Randomizes coherent errors into stochastic noise
- Includes measurement error mitigation from level 1
- ✅ **CORRECT ANSWER**

#### **Option D: `resilience_level = 3`**

- This level does NOT exist in Qiskit Runtime
- Valid levels are only 0, 1, and 2
- ❌ **Incorrect**

### **Answer: C**

---

## **Question 2: Array Broadcasting Pattern**

**Question:** Which one of the following patterns, expressed in terms of array broadcasting primitives, is represented by the given image?

### Options Analysis:

#### **Option A: Standard nd generalization** ✓

- General N-dimensional broadcasting following NumPy conventions
- Extends arrays along missing dimensions automatically
- Most flexible pattern for arbitrary dimensional operations
- ✅ **CORRECT ANSWER**

#### **Option B: Outer/Product**

- Creates outer product: every element of array A with every element of array B
- Results in higher-dimensional output
- Pattern: expand both arrays to create Cartesian product
- ❌ **Incorrect**

#### **Option C: Broadcast single observable**

- Specific to quantum computing: one observable broadcast across multiple **parameters**
- Pattern: (1 observable) → (N parameter sets with same observable)
- Used when computing expectation values for same observable with different circuit parameters
- ❌ **Incorrect**

#### **Option D: Zip**

- Element-wise pairing: combines corresponding elements from multiple arrays
- Pattern: arrays must have same length, no dimension expansion
- Example: `zip([a,b,c], [x,y,z])` → `[(a,x), (b,y), (c,z)]`
- ❌ **Incorrect**

### **Answer: A**

---

## **Question 3: SdgGate Phase on |1⟩**

**Question:** Applying the Qiskit `SdgGate` to a qubit in state `|1⟩` introduces which global phase?

### Mathematical Background:

**S Gate matrix:**

```
S = |0⟩⟨0| + i|1⟩⟨1| = [[1, 0 ]
                         [0, i ]]
```

**Sdg (S†) Gate matrix:**

```
Sdg = |0⟩⟨0| - i|1⟩⟨1| = [[1,  0 ]
                            [0, -i]]
```

### Applying Sdg to |1⟩:

```
Sdg|1⟩ = [[1,  0 ]   [[0]     [[0 ]
          [0, -i]] ×  [1]]  =  [-i]]

       = -i|1⟩
       = e^(-iπ/2)|1⟩
```

### Options Analysis:

#### **Option A: π/2 phase**

- Would give: `e^(iπ/2)|1⟩ = i|1⟩`
- This is the **S gate**, not Sdg
- ❌ **Incorrect**

#### **Option B: π/4 phase**

- Would give: `e^(iπ/4)|1⟩`
- This is the **T gate**
- ❌ **Incorrect**

#### **Option C: -π/4 phase**

- Would give: `e^(-iπ/4)|1⟩`
- This is the **Tdg gate**
- ❌ **Incorrect**

#### **Option D: -π/2 phase** ✓

- Gives: `e^(-iπ/2)|1⟩ = -i|1⟩` ✓
- Matches our calculation exactly
- ✅ **CORRECT ANSWER**

### **Answer: D**

---

## **Question 4: OpenQASM 3 File Output**

**Question:** Which one of the following code fragments will convert a `QuantumCircuit` object, named `circuit`, into an OpenQASM 3 **file output** in Qiskit?

### Options Analysis:

#### **Option A: `qiskit.qasm3.dumps(circuit)`**

- `dumps()` → "dump **string**"
- Returns OpenQASM 3 as a **string** in memory (not a file)
- Follows Python convention (like `json.dumps()`)
- ❌ **Incorrect** (creates string, not file)

#### **Option B: `qiskit.qasm3.dump(circuit, file)`** ✓

- `dump()` → "dump to **file**"
- Writes OpenQASM 3 directly to a file object
- Follows standard Python convention (like `json.dump()`)
- ✅ **CORRECT ANSWER**

**Usage Example:**

```python
from qiskit import qasm3

with open('circuit.qasm', 'w') as f:
    qasm3.dump(circuit, f)  # Writes to file
```

#### **Option C: `qiskit.qasm3.to_qasm(circuit)`**

- This function does NOT exist in `qiskit.qasm3` module
- ❌ **Incorrect** (not a valid function)

#### **Option D: `qiskit.qasm3.export(circuit)`**

- This function does NOT exist in `qiskit.qasm3` module
- ❌ **Incorrect** (not a valid function)

### Memory Aid:

- `dumps()` = dump **s**tring (returns string)
- `dump()` = dump to file (requires file object)

### **Answer: B**

---

## **Question 5: Probability After RX Rotation**

**Question:** Given the following code fragment, what is the approximate probability that a measurement would result in a bit value of `0`?

```python
from qiskit import QuantumCircuit
import numpy as np

qc = QuantumCircuit(1)
qc.reset(0)
qc.rx(3 * np.pi / 4, 0)
qc.measure_all()
```

### Method 1: Bloch Sphere Visualization (Easier Mental Calculation)

**Initial State:** `|0⟩` is at **North Pole** of Bloch sphere

**RX Rotation:** Rotates around **X-axis** by angle `θ = 3π/4 = 135°`

**Visualization:**

```
Starting point: North Pole (|0⟩)
Rotation axis:  X-axis (horizontal)
Rotation angle: 135° (more than 90°, less than 180°)

After rotation:
- Qubit is rotated 135° around X-axis
- Ends up closer to South Pole (|1⟩) than North Pole (|0⟩)
- More than halfway toward |1⟩
```

<img src="../Images/blosch_rotation.png" alt="Blosch sphere rotation" width="500">

**Table 2: RX Rotation from |1⟩ → Probability of measuring |1⟩**

Same table, but P(0) and P(1) are swapped!

- If starting from |1⟩: Use the same angle, but P(1) = value from P(0) column above
- Example: RX(135°) on |1⟩ gives P(1) = 0.15, P(0) = 0.85

### **For Question 5:**

**Quick Mental Calculation:**

1. **Angle**: 3π/4 = **135°** around X-axis from |0⟩
2. **Lookup**: From table, **135°** → **P(0) ≈ 0.15**
3. **Exact formula**: P(0) = cos²(θ/2) = cos²(67.5°) = **0.1464**

**Why this works:**

- The formula is P(0) = cos²(θ/2)
- For θ = 135°, we calculate cos²(135°/2) = cos²(67.5°)
- cos(67.5°) ≈ 0.3827
- (0.3827)² ≈ 0.1464 ✓

This matches **Option A: 0.1464**

---

### Method 2: Mathematical Derivation

**RX Gate Matrix Formula:**

```
RX(θ) = [[cos(θ/2),    -i·sin(θ/2)]
         [-i·sin(θ/2),  cos(θ/2)  ]]
```

**For θ = 3π/4:**

```
RX(3π/4) = [[cos(3π/8),    -i·sin(3π/8)]
            [-i·sin(3π/8),  cos(3π/8)  ]]
```

**Calculate Trigonometric Values:**

- `3π/8 = 67.5°`
- `cos(3π/8) ≈ 0.3827`
- `sin(3π/8) ≈ 0.9239`

**Apply to |0⟩ = [1, 0]ᵀ:**

```
RX(3π/4)|0⟩ = [[0.3827   ]   = 0.3827|0⟩ + 0.9239e^(-iπ/2)|1⟩
               [-i·0.9239]]
```

**Calculate Probabilities:**

```
P(0) = |0.3827|² = 0.1465 ≈ 0.1464
P(1) = |0.9239|² = 0.8536
```

**Verification:** P(0) + P(1) = 0.1464 + 0.8536 = 1.000 ✓

---

### Options Analysis:

#### **Option A: 0.1464** ✓

- Matches `P(0) = cos²(3π/8)`
- Correct calculation from both methods
- ✅ **CORRECT ANSWER**

#### **Option B: 0.5**

- Would require `RX(π/2)` rotation (90°)
- Equal superposition state
- ❌ **Incorrect**

#### **Option C: 0.8536**

- This is `P(1)`, not `P(0)`
- Common mistake: confusing measurement outcomes
- ❌ **Incorrect**

#### **Option D: 1.0**

- Would mean no rotation or `RX(0)`
- Qubit stays at North Pole
- ❌ **Incorrect**

### Quick Mental Check Strategy:

1. **Identify rotation**: 3π/4 = 135° around X-axis
2. **Reference points**:
   - 0° → P(0)=1.0
   - 90° → P(0)=0.5
   - 180° → P(0)=0.0
3. **Position**: 135° is 3/4 of the way, so P(0) should be small
4. **Exact formula**: P(0) = cos²(67.5°) ≈ 0.15

### **Answer: A**

---

## **Question 6: QuantumCircuit Initialization**

**Question:** Which two of the following code fragments create a `QuantumCircuit` with 2 classical bits and 3 qubits?

### QuantumCircuit Constructor Patterns:

The `QuantumCircuit` constructor accepts arguments in the following order:

- **Pattern 1:** `QuantumCircuit(num_qubits, num_clbits)`
- **Pattern 2:** `QuantumCircuit(QuantumRegister, ClassicalRegister)`
- **Pattern 3:** `QuantumCircuit(Register1, Register2, ...)`

### Options Analysis:

#### **Option A: `QuantumCircuit(2,3)`**

- Uses the positional argument pattern: `(num_qubits, num_clbits)`
- Creates: **2 qubits** and **3 classical bits**
- We need: **3 qubits** and **2 classical bits**
- ❌ **Incorrect** (reversed order)

#### **Option B: `QuantumCircuit(QuantumRegister(3, 'qr0'), QuantumRegister(2, 'qr1'))`**

- Creates two quantum registers: `qr0` with 3 qubits and `qr1` with 2 qubits
- Total: **5 qubits**, **0 classical bits**
- We need: **3 qubits** and **2 classical bits**
- ❌ **Incorrect** (no classical bits, too many qubits)

#### **Option C: `QuantumCircuit(QuantumRegister(3), ClassicalRegister(2))`** ✓

- Creates one quantum register with 3 qubits
- Creates one classical register with 2 classical bits
- Total: **3 qubits**, **2 classical bits** ✓
- ✅ **CORRECT ANSWER**

#### **Option D: `QuantumCircuit(3,2)`** ✓

- Uses the positional argument pattern: `(num_qubits, num_clbits)`
- Creates: **3 qubits** and **2 classical bits** ✓
- ✅ **CORRECT ANSWER**

#### **Option E: `QuantumCircuit(QuantumRegister(2, 'qr0'), QuantumRegister(3, 'qr1'))`**

- Creates two quantum registers: `qr0` with 2 qubits and `qr1` with 3 qubits
- Total: **5 qubits**, **0 classical bits**
- We need: **3 qubits** and **2 classical bits**
- ❌ **Incorrect** (no classical bits, too many qubits)

### **Answers: C and D**

### Key Takeaway:

Remember the order: `QuantumCircuit(qubits_first, clbits_second)`

---

## **Question 7: Q-Sphere State Visualization**

**Question:** Looking at the Q-sphere visualization showing `|01⟩` and `|10⟩` states, which code would produce this quantum state?

### Understanding the Q-Sphere Image:

The Q-sphere shows:

- **Two states present:** `|01⟩` (yellow/gold sphere on left) and `|10⟩` (blue sphere on right)
- **Equal size spheres:** Indicates equal probabilities for both states
- **Phase indicator:** Shows the relative phase between the states
- The connecting line suggests these states have a **phase relationship**

**Important:** Qiskit uses **little-endian** (right-to-left) ordering:

- `|01⟩` in display means: q₀=|1⟩, q₁=|0⟩ (rightmost bit is qubit 0)
- `|10⟩` in display means: q₀=|0⟩, q₁=|1⟩

### Key Observation from the Image:

The two states appear to have a **relative phase difference** (notice the phase color wheel). This suggests we need a state with phase:

```
|ψ⟩ = (1/√2)(|01⟩ - |10⟩)
```

### Options Analysis:

#### **Option A:**

```python
qc = QuantumCircuit(2)
qc.x(1)              # q₁: |0⟩ → |1⟩
qc.h(0)              # q₀: |0⟩ → |+⟩ = (|0⟩+|1⟩)/√2
qc.cx(0, 1)          # CNOT with q₀ as control, q₁ as target
```

**State Evolution:**

1. After `x(1)`: `|01⟩` (in Qiskit notation: q₀=|0⟩, q₁=|1⟩)
2. After `h(0)`: `(|0⟩+|1⟩)/√2 ⊗ |1⟩ = (|01⟩+|11⟩)/√2`
3. After `cx(0,1)`:
   - When q₀=|0⟩: q₁ stays |1⟩ → |01⟩
   - When q₀=|1⟩: q₁ flips |1⟩→|0⟩ → |10⟩
   - Result: `(|01⟩+|10⟩)/√2` (both components have **same positive phase**)

This creates states with **no relative phase difference**.

- ❌ **Incorrect**

#### **Option B:**

```python
qc = QuantumCircuit(2)
qc.h(0)              # q₀: |0⟩ → |+⟩
qc.cx(0, 1)          # CNOT
```

**State Evolution:**

1. After `h(0)`: `(|00⟩+|10⟩)/√2`
2. After `cx(0,1)`: `(|00⟩+|11⟩)/√2` (standard Bell state Φ⁺)

This produces `|00⟩` and `|11⟩`, not `|01⟩` and `|10⟩`

- ❌ **Incorrect**

#### **Option C:**

```python
qc = QuantumCircuit(2)
qc.h(0)              # q₀: |0⟩ → |+⟩
qc.z(0)              # Applies phase: |+⟩ → |-⟩ = (|0⟩-|1⟩)/√2
qc.cx(0, 1)          # CNOT
```

**State Evolution:**

1. After `h(0)`: `(|00⟩+|10⟩)/√2`
2. After `z(0)`: `(|00⟩-|10⟩)/√2` (Z gate adds π phase to |1⟩ component)
3. After `cx(0,1)`:
   - When q₀=|0⟩: q₁ stays |0⟩ → |00⟩
   - When q₀=|1⟩: q₁ flips |0⟩→|1⟩ → |11⟩
   - Result: `(|00⟩-|11⟩)/√2` (Bell state Φ⁻)

This produces `|00⟩` and `|11⟩`, not `|01⟩` and `|10⟩`

- ❌ **Incorrect**

#### **Option D:** ✓

```python
qc = QuantumCircuit(2)
qc.x(0)              # q₀: |0⟩ → |1⟩
qc.x(1)              # q₁: |0⟩ → |1⟩
qc.h(0)              # q₀: |1⟩ → |-⟩ = (|0⟩-|1⟩)/√2
qc.cx(0, 1)          # CNOT
```

**State Evolution:**

1. After `x(0)` and `x(1)`: `|11⟩` (both qubits in |1⟩)
2. After `h(0)`:
   - H|1⟩ = (|0⟩-|1⟩)/√2 = |-⟩
   - State becomes: `(|0⟩-|1⟩)/√2 ⊗ |1⟩ = (|01⟩-|11⟩)/√2`
3. After `cx(0,1)`: (control=q₀, target=q₁)
   - When q₀=|0⟩: q₁ stays |1⟩ → |01⟩
   - When q₀=|1⟩: q₁ flips |1⟩→|0⟩ → |10⟩
   - Result: `(|01⟩-|10⟩)/√2` = `(1/√2)|01⟩ - (1/√2)|10⟩`

This creates the **Bell state Ψ⁻** with:

- Both `|01⟩` and `|10⟩` present ✓
- **Relative phase of π** between them ✓
- Equal amplitudes ✓

✅ **CORRECT ANSWER**

### **Answer: D**

### Visual Understanding:

The circuit in Option D creates the **Bell state Ψ⁻**:

```
|Ψ⁻⟩ = (1/√2)(|01⟩ - |10⟩)
```

This is one of the four **maximally entangled Bell states**:

- **Φ⁺** = (|00⟩+|11⟩)/√2
- **Φ⁻** = (|00⟩-|11⟩)/√2
- **Ψ⁺** = (|01⟩+|10⟩)/√2
- **Ψ⁻** = (|01⟩-|10⟩)/√2 ← **This one!**

The **minus sign** creates the phase difference visible in the Q-sphere visualization, where the two states are shown with a phase relationship indicated by the connecting line and phase color wheel.

---

## **Question 8: QiskitRuntimeService.jobs Method**

**Question:** Which statement describes the expected behavior of the `QiskitRuntimeService.jobs` method?

### Understanding the `jobs()` Method:

The `QiskitRuntimeService.jobs()` method is used to retrieve job information from IBM Quantum services.

### Options Analysis:

#### **Option A: It returns no jobs unless filtered by a specific criteria**

- This would make the method useless for general queries
- No API would have such restrictive default behavior
- ❌ **Incorrect**

#### **Option B: It retrieves all runtime jobs, subject to optional filtering** ✓

- **Default behavior:** Returns jobs without requiring filters
- **Flexible:** Accepts optional filters like:
  - `backend_name`: Filter by specific backend
  - `limit`: Limit number of results
  - `pending`: Show only pending jobs
  - `created_after`/`created_before`: Time-based filtering
  - `program_id`: Filter by program type

**Example Usage:**

```python
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()

# Get all jobs (default)
all_jobs = service.jobs()

# With optional filters
filtered_jobs = service.jobs(
    backend_name='ibm_kyoto',
    limit=10,
    pending=True
)
```

✅ **CORRECT ANSWER**

#### **Option C: It always retrieves all jobs submitted in the last 30 days (720 hours)**

- While there may be a **default time window**, this is not the defining behavior
- The method's purpose is broader than just 30-day retrieval
- The key feature is **optional filtering**, not a fixed time window
- ❌ **Incorrect** (too specific, not the primary characteristic)

#### **Option D: It only returns all jobs submitted to the `ibm_foo` backend**

- `ibm_foo` is not a real backend name
- The method is not limited to a single backend
- It retrieves jobs from **all backends** by default
- ❌ **Incorrect**

### **Answer: B**

### Key Takeaway:

The `jobs()` method is **flexible and retrieves all jobs by default**, with optional filtering parameters for refined queries.

---

## **Question 9: OpenQASM 3 Type Declaration**

**Question:** Which statement describes what the following line of OpenQASM 3 code does?

```qasm
uint[8] my_int;
```

### OpenQASM 3 Type Declaration Syntax:

The general syntax for type declarations in OpenQASM 3:

```qasm
type[size] variable_name;
```

Where:

- `type`: Data type (uint, int, float, bit, etc.)
- `[size]`: Bit-width or array size
- `variable_name`: Identifier for the variable

### Options Analysis:

#### **Option A: Declare an unsigned 8-bit integer named my_int** ✓

**Breakdown:**

- `uint`: **Unsigned integer** type (non-negative integers only)
- `[8]`: **8-bit width** (can store values 0 to 2⁸-1 = 255)
- `my_int`: Variable name

**Range:** 0 to 255

This is a **type declaration** without initialization (no value assigned yet)

✅ **CORRECT ANSWER**

#### **Option B: Declare a signed 8-bit integer named my_int**

- A **signed** integer would use `int[8]`, not `uint[8]`
- `uint` specifically means **unsigned**
- ❌ **Incorrect**

**Comparison:**

```qasm
int[8] signed_int;      // Signed: -128 to 127
uint[8] unsigned_int;   // Unsigned: 0 to 255
```

#### **Option C: Assign the 8th value of the list int to variable my_int**

- This would require an **assignment operator** `=`
- Array indexing syntax would be different: `my_int = int[7];` (0-indexed)
- This is a **declaration**, not an assignment
- ❌ **Incorrect**

#### **Option D: Declare an integer named my_int with value 8**

- This would require initialization syntax: `uint[8] my_int = 8;`
- The `[8]` specifies **bit-width**, not a value
- Value 8 is assigned in this declaration
- ❌ **Incorrect**

### **Answer: A**

### OpenQASM 3 Integer Types Quick Reference:

| Declaration   | Type            | Range         |
| ------------- | --------------- | ------------- |
| `uint[8] x;`  | 8-bit unsigned  | 0 to 255      |
| `int[8] x;`   | 8-bit signed    | -128 to 127   |
| `uint[16] x;` | 16-bit unsigned | 0 to 65,535   |
| `int[32] x;`  | 32-bit signed   | -2³¹ to 2³¹-1 |

**With initialization:**

```qasm
uint[8] my_int = 42;        // Declare and initialize
int[16] signed_val = -100;   // Signed with negative value
```

---

## **Question 10: Bloch Vector Visualization**

**Question:** A quantum circuit `qc` is initialized as follows:

```python
vector = np.sqrt([1/2, 1/2])
qc.initialize(vector, 0)
```

Which `plot_bloch_vector` command correctly visualizes this state?

### Understanding the Initialized State:

**Given vector:**

```python
vector = np.sqrt([1/2, 1/2]) = [√(1/2), √(1/2)] = [1/√2, 1/√2]
```

**Quantum state:**

```
|ψ⟩ = (1/√2)|0⟩ + (1/√2)|1⟩ = |+⟩
```

This is the **|+⟩ state** (eigenstate of X operator, also called the Hadamard state)

### Bloch Sphere Position of |+⟩:

The **|+⟩ state** is an **equal superposition** of |0⟩ and |1⟩, located on the **positive X-axis** of the Bloch sphere.

**Key Reference States on Bloch Sphere:**

- **|0⟩**: North pole → Cartesian: (0, 0, 1) | Spherical: (1, 0, 0)
- **|1⟩**: South pole → Cartesian: (0, 0, -1) | Spherical: (1, π, 0)
- **|+⟩**: +X axis → Cartesian: (1, 0, 0) | Spherical: (1, π/2, 0)
- **|−⟩**: -X axis → Cartesian: (-1, 0, 0) | Spherical: (1, π/2, π)
- **|+i⟩**: +Y axis → Cartesian: (0, 1, 0) | Spherical: (1, π/2, π/2)
- **|−i⟩**: -Y axis → Cartesian: (0, -1, 0) | Spherical: (1, π/2, 3π/2)

### Bloch Vector Calculation for |+⟩:

For the general state `|ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩`:

**Bloch vector (Cartesian):**

```
[x, y, z] = [sin(θ)cos(φ), sin(θ)sin(φ), cos(θ)]
```

**For |+⟩ = (1/√2)|0⟩ + (1/√2)|1⟩:**

- cos(θ/2) = 1/√2 → θ/2 = π/4 → **θ = π/2**
- No imaginary component → **φ = 0**

**Bloch vector:**

```
x = sin(π/2)cos(0) = 1 × 1 = 1
y = sin(π/2)sin(0) = 1 × 0 = 0
z = cos(π/2) = 0
```

**Cartesian:** (1, 0, 0)
**Spherical:** (r=1, θ=π/2, φ=0)

### Options Analysis:

#### **Option A: `plot_bloch_vector([1, np.pi/2, 0], coord_type='spherical')`** ✓

- Uses **spherical coordinates**
- Format: `[r, theta, phi]`

**For |+⟩ state:**

- r = 1 (unit vector for pure state)
- θ = π/2 (equator of Bloch sphere)
- φ = 0 (on positive X-axis)

Looking at Option A: `[1, np.pi/2, 0]`

✅ **CORRECT ANSWER**

#### **Option B: `plot_bloch_vector([0, 1, 0])`**

- Uses **Cartesian coordinates** (default, no coord_type specified)
- Format: `[x, y, z]`
- Values: x=0, y=1, z=0
- This represents the **+Y axis** → **|+i⟩ state**
- Our state |+⟩ is on the X-axis, not Y-axis
- ❌ **Incorrect**

#### **Option C: `plot_bloch_vector([0, 0, 1])`**

- Cartesian coordinates: (x=0, y=0, z=1)
- Represents **+Z axis** → **|0⟩ state** (North pole)
- Our state is |+⟩, not |0⟩
- ❌ **Incorrect**

#### **Option D: `plot_bloch_vector([1, 0, np.pi/2], coord_type='spherical')`**

- Spherical coordinates with coord_type specified
- If format is `[phi, theta, r]`: φ=0, θ=0, additional=π/2
- θ=0 would point to the **North pole** (|0⟩), not the equator
- Does not represent |+⟩ state
- ❌ **Incorrect**

### **Answer: A**

## **Question 11: Quantum State After H Gate**

**Question:** In which quantum state will the qubit be as a result of the following code?

```python
qc = QuantumCircuit(1)
qc.reset(0)
qc.h(0)
```

### Understanding the Operations:

**Step-by-step state evolution:**

1. **`qc.reset(0)`**: Resets qubit to |0⟩ state (regardless of previous state)

   - Initial state: `|0⟩`

2. **`qc.h(0)`**: Applies Hadamard gate to qubit 0
   - Hadamard gate creates equal superposition

### Hadamard Gate Action:

The **Hadamard (H) gate** is defined as:

```
H = (1/√2) [[1,  1]
            [1, -1]]
```

**Action on basis states:**

```
H|0⟩ = (1/√2)(|0⟩ + |1⟩) = |+⟩
H|1⟩ = (1/√2)(|0⟩ - |1⟩) = |−⟩
```

### Applying H to |0⟩:

```
H|0⟩ = (1/√2) [[1,  1]   [[1]     (1/√2) [[1]     |0⟩ + |1⟩
               [1, -1]] ×  [0]]  =         [1]]  =  -------
                                                       √2
```

**Result:** `|+⟩ = (1/√2)(|0⟩ + |1⟩)`

### Options Analysis:

#### **Option A: |−⟩**

- The |−⟩ state is: `(1/√2)(|0⟩ - |1⟩)`
- This would result from applying H to |1⟩, not |0⟩
- Has a **negative** sign between components
- ❌ **Incorrect**

#### **Option B: |+⟩** ✓

- The |+⟩ state is: `(1/√2)(|0⟩ + |1⟩)`
- This is exactly what H|0⟩ produces
- **Equal superposition** with positive coefficients
- **Eigenstate** of the X operator with eigenvalue +1
- ✅ **CORRECT ANSWER**

#### **Option C: |0⟩**

- This would require no H gate or H applied twice (H² = I)
- The H gate transforms |0⟩ to a superposition, not keeping it as |0⟩
- ❌ **Incorrect**

#### **Option D: |1⟩**

- This would require an X gate (bit-flip), not H gate
- H gate creates superposition, not a basis state flip
- ❌ **Incorrect**

### **Answer: B**

### Key Insights:

**Hadamard Gate Properties:**

- Creates **equal superposition** from basis states
- **Self-inverse:** H² = I (applying H twice returns to original state)
- Maps computational basis to Hadamard basis:
  - |0⟩ ↔ |+⟩
  - |1⟩ ↔ |−⟩

**Bloch Sphere Visualization:**

- |0⟩ is at the **North Pole** (z-axis: +Z)
- |+⟩ is on the **equator** at +X axis
- H gate rotates |0⟩ by 90° around the X-Z diagonal

---

## **Question 12: Transpiler Pass Classes**

**Question:** To which module do the following classes belong?

- `RemoveFinalReset`
- `SabreLayout`
- `BasisTranslator`

### Understanding Qiskit Module Structure:

Qiskit is organized into several key modules, each with specific responsibilities:

1. **`qiskit.transpiler.passes`**: Transformation passes for circuit optimization
2. **`qiskit.circuit.library`**: Pre-built quantum circuits and gates
3. **`qiskit.scheduler`**: Pulse scheduling functionality
4. **`qiskit.providers.models`**: Backend and device models

### Analyzing the Classes:

#### **RemoveFinalReset**

- **Purpose:** Removes reset operations at the end of a circuit
- **Type:** Optimization pass
- **Reasoning:** Final resets don't affect measurement outcomes, so they can be safely removed
- **Category:** Transpiler transformation pass

#### **SabreLayout**

- **Purpose:** Heuristic layout algorithm for qubit mapping
- **SABRE:** "Swap-based Bidirectional heuristic search" algorithm
- **Function:** Maps virtual qubits to physical qubits on hardware topology
- **Category:** Transpiler layout pass

#### **BasisTranslator**

- **Purpose:** Translates gates to a target basis gate set
- **Function:** Converts circuit gates to those natively supported by hardware
- **Example:** Decomposing Toffoli gates into CNOT + single-qubit gates
- **Category:** Transpiler translation pass

### Options Analysis:

#### **Option A: `qiskit.scheduler`**

- This module handles **pulse-level scheduling**
- Deals with timing and orchestration of microwave pulses
- Not related to circuit-level transformations
- ❌ **Incorrect**

#### **Option B: `qiskit.circuit.library`**

- Contains **pre-built circuits** like:
  - Standard gates (XGate, HGate, CNOTGate)
  - Circuit templates (QFT, Grover circuits)
  - N-local circuits (EfficientSU2, RealAmplitudes)
- These are **circuits**, not **transpiler passes**
- ❌ **Incorrect**

#### **Option C: `qiskit.transpiler.passes`** ✓

- Contains **all transpiler transformation passes**
- Organized into categories:
  - **Layout passes:** SabreLayout, TrivialLayout, DenseLayout
  - **Routing passes:** SabreSwap, StochasticSwap
  - **Translation passes:** BasisTranslator, Unroller
  - **Optimization passes:** RemoveFinalReset, Optimize1qGates, CommutativeCancellation
  - **Scheduling passes:** ALAPSchedule, ASAPSchedule

All three classes are transpiler passes that transform quantum circuits.

✅ **CORRECT ANSWER**

#### **Option D: `qiskit.providers.models`**

- Contains **backend information models**:
  - BackendConfiguration
  - BackendProperties
  - PulseDefaults
- Describes hardware characteristics, not circuit transformations
- ❌ **Incorrect**

### **Answer: C**

### Transpiler Pass Categories:

**Common Pass Types:**

| Category         | Purpose                            | Examples                          |
| ---------------- | ---------------------------------- | --------------------------------- |
| **Analysis**     | Gather circuit information         | Depth, Width, CountOps            |
| **Layout**       | Map virtual to physical qubits     | SabreLayout, DenseLayout          |
| **Routing**      | Insert SWAP gates for connectivity | SabreSwap, BasicSwap              |
| **Translation**  | Convert to basis gates             | BasisTranslator, Unroller         |
| **Optimization** | Reduce circuit depth/gates         | Optimize1qGates, RemoveFinalReset |
| **Scheduling**   | Add timing information             | ALAPSchedule, TimeUnitConversion  |

**Usage Example:**

```python
from qiskit.transpiler.passes import RemoveFinalReset, SabreLayout, BasisTranslator
from qiskit.transpiler import PassManager

pm = PassManager([
    SabreLayout(coupling_map),
    BasisTranslator(target_basis),
    RemoveFinalReset()
])
```

---

## **Question 13: Debugging Failed Runtime Jobs**

**Question:** Which method should be used to retrieve the error message when debugging a failed Qiskit Runtime job?

### Understanding Job Error Handling:

When a Qiskit Runtime job fails, you need to retrieve error information to understand what went wrong. The job object provides methods to access error details.

### Typical Job Lifecycle:

```
Queued → Running → {Completed, Failed, Cancelled}
```

For failed jobs, we need to retrieve the error message to debug.

### Options Analysis:

#### **Option A: `job.get_error()`**

- This method name follows a common pattern (get_X)
- However, this is **not** the actual method name in Qiskit Runtime
- ❌ **Incorrect**

#### **Option B: `job.retrieve_error()`**

- Sounds plausible (retrieve pattern)
- However, this is **not** the actual method name in Qiskit Runtime
- ❌ **Incorrect**

#### **Option C: `job.error_message()`** ✓

- This is the **correct method** in Qiskit Runtime
- Returns a string containing the error message
- Available when job status is 'ERROR' or 'CANCELLED'

**Usage Example:**

```python
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
job = service.job('job_id')

# Check job status
if job.status() == 'ERROR':
    # Retrieve error message
    error = job.error_message()
    print(f"Job failed with error: {error}")
```

✅ **CORRECT ANSWER**

#### **Option D: `job.error()`**

- Close to the correct answer, but missing `_message`
- This method **does not exist** in the Qiskit Runtime API
- ❌ **Incorrect**

### **Answer: C**

### Job Debugging Methods:

**Useful Job Methods for Debugging:**

| Method                | Returns   | Purpose                                                     |
| --------------------- | --------- | ----------------------------------------------------------- |
| `job.status()`        | JobStatus | Current job state (QUEUED, RUNNING, DONE, ERROR, CANCELLED) |
| `job.error_message()` | str       | Error message if job failed                                 |
| `job.job_id()`        | str       | Unique job identifier                                       |
| `job.backend()`       | Backend   | Backend where job was run                                   |
| `job.metrics()`       | dict      | Job execution metrics                                       |
| `job.logs()`          | str       | Job execution logs (if available)                           |

**Complete Debugging Example:**

```python
from qiskit_ibm_runtime import QiskitRuntimeService, RuntimeJob

service = QiskitRuntimeService()
job = service.job('job_id')

print(f"Job ID: {job.job_id()}")
print(f"Status: {job.status()}")
print(f"Backend: {job.backend().name}")

if job.status() == 'ERROR':
    print(f"Error Message: {job.error_message()}")
    print(f"Metrics: {job.metrics()}")
elif job.status() == 'DONE':
    result = job.result()
    print(f"Result: {result}")
```

**Common Error Scenarios:**

- **Queue timeout:** Job waited too long in queue
- **Execution timeout:** Job exceeded maximum execution time
- **Invalid circuit:** Circuit not compatible with backend
- **Backend error:** Hardware or service issues

---

## **Question 14: SamplerV2 Run Method Invocation**

**Question:** Given the code snippet, which one of the following is a valid way to invoke the `run` method on an instance of `SamplerV2`?

```python
from qiskit_ibm_runtime import SamplerV2
...
sampler = SamplerV2(...)
```

### Understanding SamplerV2:

**SamplerV2** is a Qiskit Runtime primitive for:

- Sampling from quantum circuits (getting measurement outcomes)
- Executing ISA (Instruction Set Architecture) circuits
- Returns bit string arrays

**Key Design Principle:**

- The backend is specified when **creating** the sampler instance
- The `run()` method only needs **circuits** (and optional parameters)

### SamplerV2 Initialization:

```python
from qiskit_ibm_runtime import SamplerV2, QiskitRuntimeService

service = QiskitRuntimeService()
backend = service.backend('ibm_kyoto')

# Backend specified at initialization
sampler = SamplerV2(backend=backend)
```

### Run Method Signature:

```python
sampler.run(pubs, shots=None)
```

Where:

- **pubs**: List of PUBs (Primitive Unified Blocks) - typically ISA circuits
- **shots**: Optional number of shots (defaults to backend default)

**PUB (Primitive Unified Block):** Can be:

1. A circuit: `[circuit]`
2. A tuple: `(circuit,)` or `(circuit, parameter_values)` or `(circuit, parameter_values, shots)`

### Options Analysis:

#### **Option A: `sampler.run(isa_circuit, observable)`**

- SamplerV2 does **not** take observables as arguments
- **Observables** are used with **EstimatorV2**, not SamplerV2
- SamplerV2 returns results in bitstring array for each run of the circuit
- ❌ **Incorrect**

**Confusion Point:** EstimatorV2 uses observables:

```python
# EstimatorV2 (not SamplerV2)
estimator.run([(isa_circuit, observable)])
```

#### **Option B: `sampler.run(isa_circuit, backend, parameter)`**

- Backend is **already specified** during SamplerV2 initialization
- Cannot specify backend in the `run()` method
- Wrong signature - doesn't match the API
- ❌ **Incorrect**

#### **Option C: `sampler.run([isa_circuit])`** ✓

- **Correct format:** Passes a list of PUBs
- Each circuit in the list is a PUB
- Follows the V2 primitive pattern
- Backend was already specified during initialization

**Valid variations:**

```python
# Single circuit
sampler.run([isa_circuit])

# Multiple circuits
sampler.run([circuit1, circuit2, circuit3])

# With parameter values
sampler.run([(circuit, param_values)])

# With shots override
sampler.run([(circuit, param_values, 2048)])
```

✅ **CORRECT ANSWER**

#### **Option D: `sampler.run(backend, isa_circuit)`**

- Backend is specified at **initialization**, not in `run()`
- Wrong argument order
- Doesn't match API signature
- ❌ **Incorrect**

### **Answer: C**

### SamplerV2 Complete Example:

```python
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import SamplerV2, QiskitRuntimeService

# Setup
service = QiskitRuntimeService()
backend = service.backend('ibm_kyoto')

# Create circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Transpile to ISA circuit
isa_circuit = transpile(qc, backend=backend, optimization_level=3)

# Initialize sampler with backend
sampler = SamplerV2(backend=backend)

# Run - backend already known, just pass circuit(s)
job = sampler.run([isa_circuit])
result = job.result()

# Access results
pub_result = result[0]
counts = pub_result.data.meas.get_counts()
print(f"Counts: {counts}")
```

---

## **Question 15: Connecting to IBM Backend**

**Question:** Given the code fragment, which one of the following correctly connects to the `"ibm_foo"` backend?

```python
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService()
```

### Understanding QiskitRuntimeService:

**QiskitRuntimeService** is the main interface for:

- Authenticating with IBM Quantum services
- Accessing available backends
- Submitting and managing jobs

### Backend Retrieval in Qiskit Runtime:

After initializing the service, you need to retrieve a specific backend to use it.

### Options Analysis:

#### **Option A: `backend = service.get("ibm_foo")`**

- The `get()` method is **not used** for backends in Qiskit Runtime
- `get()` might exist for other purposes but not for backend retrieval
- ❌ **Incorrect**

#### **Option B: `backend = "ibm_foo"`**

- This just assigns a **string** to the variable
- Does not actually connect to or retrieve the backend object
- No API call is made
- Cannot use a string where a Backend object is required
- ❌ **Incorrect**

**This would fail:**

```python
backend = "ibm_foo"
sampler = SamplerV2(backend=backend)  # Error! Expects Backend object
```

#### **Option C: `backend = service.fetch_backend("ibm_foo")`**

- `fetch_backend()` is **not** the correct method name
- This method does not exist in QiskitRuntimeService
- ❌ **Incorrect**

#### **Option D: `backend = service.backend("ibm_foo")`** ✓

- **Correct method:** `backend()` retrieves a backend by name
- Returns a Backend object that can be used with primitives
- Standard method in Qiskit Runtime

**Usage:**

```python
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
backend = service.backend("ibm_kyoto")  # Real backend name

print(f"Backend: {backend.name}")
print(f"Number of qubits: {backend.num_qubits}")
```

✅ **CORRECT ANSWER**

### **Answer: D**

### QiskitRuntimeService Backend Methods:

**Key Methods for Working with Backends:**

| Method                  | Purpose                      | Returns        |
| ----------------------- | ---------------------------- | -------------- |
| `service.backend(name)` | Get specific backend by name | Backend object |
| `service.backends()`    | List all available backends  | List[Backend]  |
| `service.least_busy()`  | Get least busy backend       | Backend object |

**Complete Example:**

```python
from qiskit_ibm_runtime import QiskitRuntimeService

# Initialize service (loads credentials)
service = QiskitRuntimeService()

# Method 1: Get specific backend by name
backend = service.backend("ibm_kyoto")

# Method 2: List all backends and filter
backends = service.backends(simulator=False, operational=True)
print(f"Available backends: {[b.name for b in backends]}")

# Method 3: Get least busy backend
backend = service.least_busy(operational=True, simulator=False)
print(f"Using backend: {backend.name}")

# Check backend properties
print(f"Qubits: {backend.num_qubits}")
print(f"Max shots: {backend.max_shots}")
print(f"Max circuits: {backend.max_circuits}")
```

### Backend Filtering Options:

**Common filter parameters for `service.backends()`:**

- `simulator=False`: Exclude simulators, get real hardware only
- `operational=True`: Only currently operational backends
- `min_num_qubits=5`: Minimum number of qubits required
- `filters=lambda b: b.max_shots >= 10000`: Custom filter function

**Example with filtering:**

```python
# Get all operational hardware backends with at least 27 qubits
backends = service.backends(
    simulator=False,
    operational=True,
    min_num_qubits=27
)

for b in backends:
    print(f"{b.name}: {b.num_qubits} qubits, "
          f"pending jobs: {b.status().pending_jobs}")
```

### Authentication Setup:

**First-time setup (one-time):**

```python
from qiskit_ibm_runtime import QiskitRuntimeService

# Save credentials
QiskitRuntimeService.save_account(
    channel='ibm_quantum_platform',
    token='YOUR_IBM_QUANTUM_TOKEN',
    instance = 'YOUR_IBM_INSTANCE starting with crn:v1:....::'
    overwrite=True,
    set_as_default=True
)
```

**Subsequent usage:**

```python
# Automatically loads saved credentials
service = QiskitRuntimeService()
```

---

## **Question 16: ParameterVector Index Finding**

**Question:** Given a `ParameterVector` as defined below, which one of the following would find the position of `x` within `v`?

```python
from qiskit.circuit import ParameterVector
v = ParameterVector("v", 3)
x = v[1]
```

### Understanding ParameterVector:

**ParameterVector** is a Qiskit class for creating a vector of parameters that can be used in parameterized quantum circuits.

**In this example:**

```python
v = ParameterVector("v", 3)
# Creates: v[0], v[1], v[2]
x = v[1]  # x is the parameter at index 1
```

We want to find which index `x` occupies in the vector `v`.

### Options Analysis:

#### **Option A: `v.find(x)`**

- `find()` is a **string method** in Python, not a sequence method
- Works for strings: `"hello".find("e")` returns 1
- **Does not exist** for list-like objects or ParameterVector
- ❌ **Incorrect**

**Why the confusion?**

- Strings have `find()` method
- Lists/tuples/ParameterVector use `index()` method instead

#### **Option B: `v.index(x)`** ✓

- `index()` is the **standard Python sequence method** to find position
- Works for lists, tuples, and ParameterVector
- Returns the integer index where the item is found
- Raises `ValueError` if item not found

**Usage:**

```python
from qiskit.circuit import ParameterVector

v = ParameterVector("v", 3)
x = v[1]

position = v.index(x)
print(position)  # Output: 1
```

**Verification:**

```python
# x is v[1], so index should return 1
assert v.index(x) == 1  # True

# Try with different elements
assert v.index(v[0]) == 0  # True
assert v.index(v[2]) == 2  # True
```

✅ **CORRECT ANSWER**

#### **Option C: `x.find_in(v)`**

- This method **does not exist** on Parameter objects
- Wrong pattern - we search **in** the container, not from the element
- ❌ **Incorrect**

#### **Option D: `v.locate(x)`**

- `locate()` is **not a standard Python method** for sequences
- Does not exist in ParameterVector API
- ❌ **Incorrect**

### **Answer: B**

### ParameterVector Usage Examples:

**Creating parameterized circuits:**

```python
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector

# Create parameter vector
theta = ParameterVector("θ", 3)

# Build parameterized circuit
qc = QuantumCircuit(3)
qc.rx(theta[0], 0)
qc.ry(theta[1], 1)
qc.rz(theta[2], 2)

# Finding parameter positions
print(theta.index(theta[1]))  # Output: 1

# Binding parameters
parameter_values = [0.5, 1.2, 2.1]
bound_circuit = qc.assign_parameters({theta: parameter_values})
```

**Useful ParameterVector Methods:**

- `len(v)`: Get the length of the vector
- `v[i]`: Access parameter at index i
- `v.index(param)`: Find position of parameter
- `v.name`: Get the vector name
- `v.params`: Get list of all parameters

---

## **Question 17: Pauli Matrix Generation**

**Question:** Which one of the following code fragments will generate the given output?

```
[[0.+0.j  1.+0.j  0.+0.j  0.+0.j]
 [1.+0.j  0.+0.j  0.+0.j  0.+0.j]
 [0.+0.j  0.+0.j  0.+0.j -1.+0.j]
 [0.+0.j  0.+0.j -1.+0.j  0.+0.j]]
```

### Understanding Pauli Operators:

**Single-qubit Pauli matrices:**

```
I = [[1, 0],     X = [[0, 1],     Y = [[0, -i],    Z = [[1,  0],
     [0, 1]]         [1, 0]]          [i,  0]]         [0, -1]]
```

**Multi-qubit Pauli operators** are formed by **tensor products** (⊗):

- Notation: `"ZX"` means Z ⊗ X (Z on qubit 1, X on qubit 0)
- **Right-to-left** convention: Rightmost acts on qubit 0

### Analyzing the Target Matrix:

The target is a **4×4 matrix** (2-qubit system):

```
[[0,  1,  0,  0]
 [1,  0,  0,  0]
 [0,  0,  0, -1]
 [0,  0, -1,  0]]
```

**Structure analysis:**

- Top-left 2×2 block: `[[0, 1], [1, 0]]` = X matrix
- Bottom-right 2×2 block: `[[0, -1], [-1, 0]]` = -X matrix
- This pattern suggests: **X on one qubit, Z on another**

### Tensor Product Review:

For a 2-qubit operator `AB` (A on qubit 1, B on qubit 0):

- If A = Z and B = X, the result is Z ⊗ X
- Basis ordering: |00⟩, |01⟩, |10⟩, |11⟩

**Computing Z ⊗ X:**

```
Z ⊗ X = [[1, 0],  ⊗  [[0, 1],
         [0,-1]]      [1, 0]]

     = [[1·X,  0·X ],     [[X,   0 ],     [[0, 1, 0, 0],
        [0·X, -1·X]]   =   [0,  -X]]   =   [1, 0, 0, 0],
                                            [0, 0, 0,-1],
                                            [0, 0,-1, 0]]
```

This matches our target matrix! ✓

### Options Analysis:

#### **Option A: `Pauli('ZX')`** ✓

**Pauli string:** `'ZX'`

- **Right-to-left convention:** X on qubit 0, Z on qubit 1
- Operator: Z ⊗ X

**Matrix calculation:**

```python
from qiskit.quantum_info import Pauli

p = Pauli('ZX')
print(p.to_matrix())
```

**Result:** Z ⊗ X matrix (exactly matches target)

✅ **CORRECT ANSWER**

#### **Option B: `Pauli('-IX')`**

**Pauli string:** `'-IX'`

- Phase coefficient: **-1**
- Operator: -1 × (I ⊗ X)

**Matrix calculation:**

```
I ⊗ X = [[1, 0],  ⊗  [[0, 1],     [[0, 1, 0, 0],
         [0, 1]]      [1, 0]]   =   [1, 0, 0, 0],
                                     [0, 0, 0, 1],
                                     [0, 0, 1, 0]]

-I ⊗ X = [[0, -1, 0,  0],
          [-1, 0, 0,  0],
          [0,  0, 0, -1],
          [0,  0,-1,  0]]
```

This has **all negative** entries in non-zero positions, different from target.

- ❌ **Incorrect**

#### **Option C: `Pauli('-XX')`**

**Pauli string:** `'-XX'`

- Phase coefficient: **-1**
- Operator: -1 × (X ⊗ X)

**Matrix calculation:**

```
X ⊗ X = [[0, 1],  ⊗  [[0, 1],     [[0, 0, 0, 1],
         [1, 0]]      [1, 0]]   =   [0, 0, 1, 0],
                                     [0, 1, 0, 0],
                                     [1, 0, 0, 0]]

-X ⊗ X has all negative non-zero entries
```

Different structure from target.

- ❌ **Incorrect**

#### **Option D: `Pauli('-XI')`**

**Pauli string:** `'-XI'`

- Phase coefficient: **-1**
- Operator: -1 × (X ⊗ I)

**Matrix calculation:**

```
X ⊗ I = [[0, 1],  ⊗  [[1, 0],     [[0, 0, 1, 0],
         [1, 0]]      [0, 1]]   =   [0, 0, 0, 1],
                                     [1, 0, 0, 0],
                                     [0, 1, 0, 0]]
```

Different structure from target (X acts on qubit 1 instead of 0).

- ❌ **Incorrect**

### **Answer: A**

### Pauli String Format:

**Convention in Qiskit:**

- **String format:** `"[phase][P1][P2]...[Pn]"`
- **Phase prefix:** `''` (none), `'-'` (-1), `'i'` (i), `'-i'` (-i)
- **Operator order:** Right-to-left (rightmost = qubit 0)

**Examples:**

```python
from qiskit.quantum_info import Pauli

# Identity on both qubits
Pauli('II')  # I ⊗ I

# X on qubit 0, I on qubit 1
Pauli('IX')  # I ⊗ X

# X on qubit 1, I on qubit 0
Pauli('XI')  # X ⊗ I

# With phase
Pauli('-ZX')  # -(Z ⊗ X)
Pauli('iYY')  # i(Y ⊗ Y)
```

**Useful Pauli Methods:**

```python
p = Pauli('ZX')
p.to_matrix()      # Get matrix representation
p.to_label()       # Get string label
p.phase            # Get phase (0, 1, 2, 3 for 1, -i, -1, i)
p.evolve(other)    # Compose with another Pauli
```

---

## **Question 18: SamplerOptions default_shots Parameter**

**Question:** Given the following code fragment, which statement describes the `SamplerOptions` parameter `options.default_shots`?

```python
from qiskit_ibm_runtime import Sampler
sampler = Sampler(mode=backend)
sampler.options.default_shots = ...
```

### Understanding the Sampler Primitive:

**Sampler** is a primitive for:

- Executing quantum circuits
- Collecting measurement outcomes

**Key concept:** A "shot" is one execution of the circuit from start to finish, including measurement.

### What is default_shots?

**`default_shots`**: The number of times the circuit is executed on the quantum hardware to collect statistics.

**Why multiple shots?**

- Quantum measurements are **probabilistic**
- Need multiple executions to estimate probability distributions
- More shots → better statistical accuracy

### Options Analysis:

#### **Option A: The number of randomizations we apply to the circuit**

- This describes **gate twirling** or **randomized compiling**, not shots
- Randomization techniques are part of error mitigation (resilience levels)
- Separate from the number of circuit executions
- ❌ **Incorrect**

**Confusion point:** Error mitigation might involve randomization, but that's controlled by different options.

#### **Option B: The number of times that we run the circuit** ✓

- **Exactly correct definition** of shots
- Each shot = one complete execution of the circuit
- Results are aggregated to form probability distribution
- Higher shots → more accurate probability estimates

**Example:**

```python
from qiskit_ibm_runtime import Sampler, QiskitRuntimeService

service = QiskitRuntimeService()
backend = service.backend('ibm_kyoto')

sampler = Sampler(backend=backend)
sampler.options.default_shots = 4096  # Run circuit 4096 times

# When job executes, circuit runs 4096 times
job = sampler.run([circuit])
result = job.result()
```

**Typical shot counts:**

- **Low:** 1024 shots (faster, less accurate)
- **Medium:** 4096 shots (default on many systems)
- **High:** 10000+ shots (slower, more accurate)

✅ **CORRECT ANSWER**

#### **Option C: The sum of the number of measurements in each qubit**

- This would describe the total number of measurement operations
- Not related to shots (execution repetitions)
- A single circuit might measure 1 qubit or 100 qubits - still one shot
- ❌ **Incorrect**

**Clarification:**

- **One shot** = one execution, regardless of number of measured qubits
- Measuring 5 qubits with 1000 shots = 1000 circuit runs (5000 total measurements)

#### **Option D: The number of sequences in dynamical decoupling**

- **Dynamical decoupling** is an error mitigation technique
- Inserts pulse sequences during idle times to reduce decoherence
- Controlled by different options (e.g., `dynamical_decoupling`)
- Completely separate concept from shots
- ❌ **Incorrect**

### **Answer: B**

---

## **Question 19: plot_distribution Valid Inputs**

**Question (Select 2):** Which two of the following Python objects are valid input to `plot_distribution`?

### Understanding plot_distribution:

**`plot_distribution`** from `qiskit.visualization` plots measurement outcome distributions.

**Typical usage:**

```python
from qiskit.visualization import plot_distribution

counts = {'00': 500, '11': 500}
plot_distribution(counts)
```

### Valid Input Formats:

The function accepts:

1. **Single dictionary:** `{outcome: count}`
2. **List of dictionaries:** `[{outcome: count}, ...]` for multiple distributions
3. Each dictionary maps measurement outcomes to their counts

### Options Analysis:

#### **Option A: `[0, 1, 2], [500, 500, 500]`**

- This is **two separate lists**
- Not a dictionary or list of dictionaries
- Would require separate `data=` and `labels=` arguments in old versions
- **Not valid** as a single argument to `plot_distribution`
- ❌ **Incorrect**

**Confusion point:** Some plotting functions accept separate data/labels, but `plot_distribution` expects dict format.

#### **Option B: `{ 0: 500, 3: 500 }`** ✓

- **Valid dictionary format**
- Keys are measurement outcomes (can be integers or strings)
- Values are counts
- Standard single distribution input

**Example:**

```python
from qiskit.visualization import plot_distribution

# Using integer keys
counts = {0: 500, 3: 500}
plot_distribution(counts)

# Equivalent with string keys
counts_str = {'00': 500, '11': 500}
plot_distribution(counts_str)
```

✅ **CORRECT ANSWER**

#### **Option C: `[(0, 500), (3, 500)]`**

- This is a **list of tuples**
- Not a dictionary format
- Would need conversion: `dict([(0, 500), (3, 500)])`
- **Not directly valid** input
- ❌ **Incorrect**

**Note:** While `dict()` can convert this to valid format, the raw list of tuples is not accepted.

#### **Option D: `[{ 0: 500, 3: 500}, { 0: 500, 1: 500 }]`** ✓

- **Valid list of dictionaries format**
- Used to plot **multiple distributions** for comparison
- Each dictionary represents one distribution
- Commonly used to compare different circuits or backends

**Example:**

```python
from qiskit.visualization import plot_distribution

# Comparing two different runs
dist1 = {0: 500, 3: 500}  # First circuit
dist2 = {0: 500, 1: 500}  # Second circuit

plot_distribution([dist1, dist2],
                 legend=['Circuit 1', 'Circuit 2'])
```

✅ **CORRECT ANSWER**

#### **Option E: `{ 0: [300, 500], 1: [400, 500] }`**

- Dictionary with **lists as values** instead of integers
- Not the expected format (values should be counts, not lists)
- Would cause an error
- ❌ **Incorrect**

### **Answers: B and D**

### plot_distribution Complete Guide:

**Basic usage:**

```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_distribution

# Create and run circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

simulator = AerSimulator()
job = simulator.run(qc, shots=1000)
counts = job.result().get_counts()

# Plot single distribution
plot_distribution(counts)
```

**Comparing multiple distributions:**

```python
# Different backends or circuits
counts_sim = {'00': 485, '11': 515}
counts_hardware = {'00': 467, '01': 23, '10': 31, '11': 479}

plot_distribution(
    [counts_sim, counts_hardware],
    legend=['Simulator', 'Hardware'],
    title='Comparison of Results'
)
```

**Valid input formats summary:**

```python
# Format 1: Single dictionary (integer keys)
plot_distribution({0: 500, 3: 500})

# Format 2: Single dictionary (string keys)
plot_distribution({'00': 500, '11': 500})

# Format 3: List of dictionaries
plot_distribution([
    {'00': 500, '11': 500},
    {'00': 480, '01': 20, '11': 500}
])
```

**Common use cases:**

- Visualizing measurement results from quantum circuits
- Comparing simulator vs hardware results
- Comparing different error mitigation techniques
- Analyzing the effect of optimization levels

---

## **Question 20: PubResult Shape in EstimatorV2**

**Question:** Assuming all necessary imports have been completed, which one of the following is the shape of a `PubResult` named `result`?

```python
parameter_values = np.random.uniform(size=(5, ))
observables = [SparsePauliOp(pauli) for pauli in ["III", "XXX", "YYY", "ZZZ", "XYZ"]]
job = Estimator(mode=session).run([(circuit, observables, parameter_values)])
result = job.result()[0].data.evs
print(result.shape())
```

---

## **Understanding the Setup**

**Circuit:** Has 1 parameter (let's call it `theta`)

**Parameter values:** `(5,)` shape = 5 different values for theta

- `[θ₀, θ₁, θ₂, θ₃, θ₄]` - five different parameter values

**Observables:** List of 5 observables

- `["III", "XXX", "YYY", "ZZZ", "XYZ"]` - five different observables

---

## **Key Insight: The "Zip" Pattern**

When you provide:

- **List of observables:** `[obs1, obs2, obs3, obs4, obs5]`
- **1D array of parameters:** `[θ₀, θ₁, θ₂, θ₃, θ₄]`

EstimatorV2 uses the **"Zip" pattern** - it pairs them element-by-element:

1. obs1 with θ₀
2. obs2 with θ₁
3. obs3 with θ₂
4. obs4 with θ₃
5. obs5 with θ₄

**Result:** 5 expectation values = **shape (5,)**

---

## **Visual Representation**

```
Observables:     [III, XXX, YYY, ZZZ, XYZ]
                   ↓    ↓    ↓    ↓    ↓
Parameters:      [θ₀,  θ₁,  θ₂,  θ₃,  θ₄]
                   ↓    ↓    ↓    ↓    ↓
Results:         [ev₀, ev₁, ev₂, ev₃, ev₄]  ← Shape (5,)
```

Each observable is evaluated with its corresponding parameter value.

---

## **Broadcasting: What Changes the Shape?**

### **Pattern 1: Zip (Question 20) - Shape (5,)**

```python
observables = [SparsePauliOp(p) for p in ["III", "XXX", "YYY", "ZZZ", "XYZ"]]
parameter_values = np.random.uniform(size=(5,))  # 5 values

# Result shape: (5,)
# Pairs: (obs[0], param[0]), (obs[1], param[1]), ..., (obs[4], param[4])
```

### **Pattern 2: Broadcast - Shape (5, 5)**

```python
observables = [[SparsePauliOp(p)] for p in ["III", "XXX", "YYY", "ZZZ", "XYZ"]]
#              ↑ Note the double brackets - list of lists
parameter_values = np.random.uniform(size=(5,))  # 5 values

# Result shape: (5, 5)
# Every observable with every parameter value (25 expectation values)
```

**The difference:**

- Single list `[obs1, obs2, ...]` → **Zip pattern** → (5,)
- List of lists `[[obs1], [obs2], ...]` → **Broadcast pattern** → (5, 5)

---

## **Options Analysis**

#### **Option A: (5, 1)**

- Would need special setup with 2D parameter array
- Not matching this case
- ❌ **Incorrect**

#### **Option B: (5, 5)**

- This is the **broadcast pattern** (every obs with every param)
- Requires `observables = [[obs1], [obs2], ...]` (list of lists)
- NOT the case in this question
- ❌ **Incorrect**

#### **Option C: (1, 5)**

- Wrong dimensionality
- Doesn't match the input structure
- ❌ **Incorrect**

#### **Option D: (5,)** ✓

- **Zip pattern:** Pairs corresponding elements
- 5 observables + 5 parameters → 5 expectation values
- 1D array with 5 elements
- ✅ **CORRECT ANSWER**

---

## **Quick Rule for Shape Prediction**

```python
# Check your observables structure:

# Pattern 1: Single list → ZIP
observables = [obs1, obs2, obs3, obs4, obs5]
params = np.array([θ₀, θ₁, θ₂, θ₃, θ₄])
# Result: (5,) - pairs them up

# Pattern 2: List of lists → BROADCAST
observables = [[obs1], [obs2], [obs3], [obs4], [obs5]]
params = np.array([θ₀, θ₁, θ₂, θ₃, θ₄])
# Result: (5, 5) - every combination
```

---

## **Answer: D - Shape (5,)**

**Why?** The question uses a single list of observables `[obs1, obs2, ...]`, which triggers the **Zip pattern**:

- 5 observables zip with 5 parameter values
- Results in 5 expectation values
- Shape: **(5,)** ✓

---

# Idle_Adiabatic

## Hamiltonian Module Manual

This module provides an object-oriented framework for constructing and manipulating quantum Hamiltonians, with a focus on Pauli operators and their unitary conjugations. It is designed for use in quantum simulation and adiabatic state preparation.

### Requirements
- Python 3.7+
- numpy

Install numpy if needed:
```
pip install numpy
```

---

## Classes

### 1. Hamiltonian (Abstract Base Class)
- Abstract class for all Hamiltonians.
- Defines the interface for `matrix()` and pretty-printing.
- Addition and scalar multiplication are not implemented by default.

### 2. PauliHamiltonian
- Represents a sum of Pauli strings with coefficients.
- **Initialization:**
  - `pauli_terms`: List of strings, each string is a Pauli string (e.g., 'XIZ', 'YYY').
  - `coefficients`: List of numbers (float or complex), same length as `pauli_terms`.
- **Supports:**
  - Multi-qubit systems (length of Pauli string = number of qubits)
  - Addition with another `PauliHamiltonian` (same number of qubits)
  - Scalar multiplication
  - Pretty-printing
- **Methods:**
  - `matrix()`: Returns the full matrix representation as a numpy array.

### 3. UnitaryConjugatedHamiltonian
- Represents a Hamiltonian of the form \( U H U^\dagger \), where \( H \) is a `PauliHamiltonian` and \( U \) is a unitary operator (or a list of unitaries, one per qubit).
- **Initialization:**
  - `pauli_hamiltonian`: A `PauliHamiltonian` object
  - `unitary_ops`: Either a list of unitary matrices (numpy arrays, one per qubit) or a single unitary matrix for the whole system
- **Methods:**
  - `matrix()`: Returns the conjugated matrix as a numpy array

---

## Example Usage

```
import numpy as np
from hamiltonian import PauliHamiltonian, UnitaryConjugatedHamiltonian, PAULI_MATRICES

# 3-qubit example: H1 = 0.5 * XIZ + 1.0 * IIZ
H1 = PauliHamiltonian(['XIZ', 'IIZ'], [0.5, 1.0])
# H2 = 0.2 * YYY
H2 = PauliHamiltonian(['YYY'], [0.2])

# Add two PauliHamiltonians (must have same number of qubits)
H_sum = H1 + H2

# Scalar multiplication
H_scaled = 2.5 * H_sum

# Pretty-printing
print("Sum Hamiltonian:", H_sum)
print("Scaled Hamiltonian:", H_scaled)

# Unitary: Hadamard on first qubit, Identity on others
HADAMARD = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
unitaries = [HADAMARD, PAULI_MATRICES['I'], PAULI_MATRICES['I']]
U_H = UnitaryConjugatedHamiltonian(H_scaled, unitaries)

print("Unitary conjugated Hamiltonian:", U_H)

# Get matrix representations
mat = H_scaled.matrix()
mat_conj = U_H.matrix()
print("Matrix shape:", mat.shape)
```

---

## Notes
- All Pauli strings in a `PauliHamiltonian` must have the same length (number of qubits).
- Addition and scalar multiplication are only supported for `PauliHamiltonian` objects.
- For custom unitaries, provide numpy arrays of appropriate dimension (2x2 for single qubit, 2^n x 2^n for n qubits).
- Pretty-printing displays the Hamiltonian in a human-readable sum-of-terms format.

---

## License
MIT

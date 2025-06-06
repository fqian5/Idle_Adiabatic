from abc import ABC, abstractmethod
import numpy as np

PAULI_MATRICES = {
    'I': np.array([[1, 0], [0, 1]], dtype=complex),
    'X': np.array([[0, 1], [1, 0]], dtype=complex),
    'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
    'Z': np.array([[1, 0], [0, -1]], dtype=complex),
}

class Hamiltonian(ABC):
    @abstractmethod
    def matrix(self):
        pass

    def __add__(self, other):
        raise NotImplementedError("Addition is not implemented for this Hamiltonian type.")

    def __mul__(self, scalar):
        raise NotImplementedError("Scalar multiplication is not implemented for this Hamiltonian type.")

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __str__(self):
        return self.__repr__()

class PauliHamiltonian(Hamiltonian):
    def __init__(self, pauli_terms, coefficients):
        n_qubits = len(pauli_terms[0])
        assert all(len(term) == n_qubits for term in pauli_terms), "All Pauli terms must have the same length"
        self.pauli_terms = pauli_terms
        self.coefficients = coefficients
        self.n_qubits = n_qubits

    def matrix(self):
        dim = 2 ** self.n_qubits
        H = np.zeros((dim, dim), dtype=complex)
        for term, coeff in zip(self.pauli_terms, self.coefficients):
            op = PAULI_MATRICES[term[0]]
            for p in term[1:]:
                op = np.kron(op, PAULI_MATRICES[p])
            H += coeff * op
        return H

    def __add__(self, other):
        if isinstance(other, PauliHamiltonian) and self.n_qubits == other.n_qubits:
            new_terms = self.pauli_terms + other.pauli_terms
            new_coeffs = self.coefficients + other.coefficients
            return PauliHamiltonian(new_terms, new_coeffs)
        else:
            raise ValueError("Can only add another PauliHamiltonian with the same number of qubits.")

    def __mul__(self, scalar):
        if not isinstance(scalar, (int, float, complex)):
            raise ValueError("Can only multiply by a scalar.")
        return PauliHamiltonian(self.pauli_terms, [scalar * c for c in self.coefficients])

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __repr__(self):
        terms = []
        for coeff, term in zip(self.coefficients, self.pauli_terms):
            terms.append(f"({coeff})*{term}")
        return " + ".join(terms) if terms else "0"

class UnitaryConjugatedHamiltonian(Hamiltonian):
    def __init__(self, pauli_hamiltonian, unitary_ops):
        assert isinstance(pauli_hamiltonian, PauliHamiltonian)
        self.pauli_hamiltonian = pauli_hamiltonian
        self.n_qubits = pauli_hamiltonian.n_qubits
        if isinstance(unitary_ops, list):
            assert len(unitary_ops) == self.n_qubits
        self.unitary_ops = unitary_ops

    def matrix(self):
        H = self.pauli_hamiltonian.matrix()
        if isinstance(self.unitary_ops, list):
            U = self.unitary_ops[0]
            for u in self.unitary_ops[1:]:
                U = np.kron(U, u)
        else:
            U = self.unitary_ops
        return U @ H @ U.conj().T

    def __repr__(self):
        return f"U * ({repr(self.pauli_hamiltonian)}) * U†" 
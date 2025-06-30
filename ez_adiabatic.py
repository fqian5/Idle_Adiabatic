import numpy as np
def single_operator_embedding(operators, n,location):
    op = np.array([1])
    for i in range(n):
        if i == location:
            op = np.kron(op, operators)
        else:
            op = np.kron(op, np.eye(2))
    return op # checked 

def sum_of_z(n):
    """
    Output the sum of  single -Z pauli operator on n qubits. make sure |0000>is gs
    The Z operator is defined as:
    Z = [[1, 0],
         [0, -1]]
    input:
    n: int, number of qubits
    output:
    sum_z: np.ndarray, shape (2**n, 2**n)
    """
    z = np.array([[1, 0], [0, -1]])
    sum_z = np.zeros((2**n, 2**n), dtype=np.complex128)
    for i in range(n):
        sum_z += single_operator_embedding(-z, n, i)
    return sum_z# checked 

def dummy_state_prep(state):
    """
    Using householder matrix to construct a unitary that prepares a given state.
    input:
    state: np.ndarray, shape (2**n,), the target state to prepare
    output:
    unitary: np.ndarray, shape (2**n, 2**n), the unitary matrix that prepares the state
    """
    eye = np.eye(len(state), dtype=np.complex128)
    k = np.zeros(len(state), dtype=np.complex128)
    
    k[0] = 1
    overlap = k.conj().T@ state/np.abs(k.conj().T@ state)
    print(overlap)
    w = overlap*k - state
    w = w / np.linalg.norm(w)  # Normalize w
    u = eye - 2 * np.outer(w,w.conj()) # Householder reflection
    print(np.allclose(u@u.conj().T,np.eye(len(state), dtype=np.complex128)))
    u = overlap * u
    print(np.allclose(u@u.conj().T,np.eye(len(state), dtype=np.complex128)))
    return u # problem
def random_state(n):
    """
    Generate a random quantum state of n qubits.
    input:
    n: int, number of qubits
    output:
    state: np.ndarray, shape (2**n,), the random quantum state
    """
    state = np.random.rand(2**n) + 1j * np.random.rand(2**n)
    state = state/np.linalg.norm(state)  # Normalize the state
    return state# checked 
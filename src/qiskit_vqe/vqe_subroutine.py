import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator
from qiskit_algorithms import VQE, VQEResult
from qiskit_algorithms.optimizers import SLSQP

SEED = 156


def _build_1qubit_local_ansatz() -> QuantumCircuit:
    """Build a 1-qubit local ansatz.

    Returns:
        QuantumCircuit: Single-qubit variational circuit with ``rx`` and ``rz`` rotations.
    """
    ansatz = QuantumCircuit(1)
    ansatz.rx(Parameter("theta"), 0)
    ansatz.rz(Parameter("phi"), 0)

    return ansatz


def _x0_parameters(n_qubits) -> np.ndarray:
    """Generate deterministic initial parameters for the optimizer.

    Args:
        n_qubits: Number of parameters to generate.

    Returns:
        np.ndarray: Seeded random initial parameter vector.
    """
    params = np.random.RandomState(seed=SEED).random(n_qubits)
    return params


def vqe_subroutine(input_hamiltonian: SparsePauliOp) -> VQEResult:
    """Run the Qiskit VQE algorithm for a supplied Hamiltonian using the ``qiskit_algorithms`` module.

    Args:
        input_hamiltonian: Hamiltonian operator to optimize against.

    Note:
        ``qiskit_algorithms`` is no longer officially supported.

    Returns:
        VQEResult: The computed minimum-eigenvalue result.

    Example:
        >>> from hamiltonian import Hamiltonian
        >>> result = vqe_subroutine(Hamiltonian.H2_STO6G_REDUX.value)
    """
    hamiltonian = input_hamiltonian
    ansatz = _build_1qubit_local_ansatz()
    optimizer = SLSQP(maxiter=1000)
    estimator = StatevectorEstimator(seed=SEED)

    vqe_circuit = VQE(
        estimator=estimator,
        ansatz=ansatz,
        optimizer=optimizer,
        initial_point=_x0_parameters(ansatz.num_parameters),
    )

    return vqe_circuit.compute_minimum_eigenvalue(hamiltonian)

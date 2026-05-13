import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP

SEED = 156


def _h2_1qubit_hamiltonian_stog6g_redux() -> list[tuple[str, float]]:
    """Return the 1-qubit H2 Hamiltonian in the STO-6G basis.

    Returns:
        list[tuple[str, float]]: Pauli operators and coefficients for the reduced Hamiltonian.
    """

    return [
        ("I", -1.04886087),
        ("Z", -0.7967368),
        ("X", 0.18121804),
    ]


def _build_hamiltonian_from_op_list(name="h2") -> SparsePauliOp:
    """Build a molecular Hamiltonian from a hard-coded operator list.

    Args:
        name (str, optional): Molecule identifier to build. Defaults to "h2".

    Returns:
        SparsePauliOp: The Hamiltonian for the requested molecule.

    Raises:
        ValueError: If the requested molecule is not implemented.
    """

    if name == "h2":
        return SparsePauliOp.from_list(_h2_1qubit_hamiltonian_stog6g_redux())

    else:
        raise ValueError(f"Hamiltonian for molecule {name} not implemented.")


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


def vqe_subroutine():
    """Run the Qiskit VQE algorithm for the built-in H2 Hamiltonian using the ``qiskit_algorithms`` module.

    Note:
        ``qiskit_algorithms`` is no longer officially supported.

    Returns:
        VQEResult: The computed minimum-eigenvalue result.

    Example:
        >>> result = vqe_subroutine()
    """
    hamiltonian = _build_hamiltonian_from_op_list("h2")
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

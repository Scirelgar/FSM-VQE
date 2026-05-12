import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import QuantumRegister, ClassicalRegister, Parameter
from qiskit.circuit.library import n_local, hamiltonian_variational_ansatz
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator
from qiskit.visualization import circuit_drawer
from matplotlib import pyplot as plt
from scipy.optimize import minimize



SEED = 156

def _h2_1qubit_hamiltonian_stog6g_redux()->list[tuple[str, float]]:
    """Return the 1-qubit H2 Hamiltonian in the STO-6G basis.

    Returns:
        list[tuple[str, float]]: Pauli operators and coefficients for the reduced Hamiltonian.
    """

    return [("I", -1.04886087), ("Z", -0.7967368), ("X", 0.18121804),]



def _build_hamiltonian_from_op_list(name="h2")->SparsePauliOp:
    """Build a molecular Hamiltonian from a hard-coded operator list.

    Args:
        name (str, optional): Molecule identifier to build. Defaults to "h2".

    Returns:
        SparsePauliOp: The Hamiltonian for the requested molecule.

    Raises:
        ValueError: If the requested molecule is not implemented.
    """

    if name == "h2":
        return SparsePauliOp.from_list(
            _h2_1qubit_hamiltonian_stog6g_redux()
            )
    
    else:
        raise ValueError(f"Hamiltonian for molecule {name} not implemented.")

def _cost_function(params, ansatz, hamiltonian, estimator)->float:
    """Evaluate the estimated energy for a parameter vector.

    Args:
        params: Ansatz parameters supplied to the estimator.
        ansatz: Quantum circuit representing the variational form.
        hamiltonian: Operator whose expectation value is minimized.
        estimator: Qiskit estimator used to evaluate the energy.

    Returns:
        float: Estimated energy for the supplied parameters.
    """

    pub_estimate = (ansatz, [hamiltonian], [params],)
    result = estimator.run(pubs=[pub_estimate],).result()
    energy = result[0].data.evs[0]

    return energy

def _build_n_local_ansatz(n_qubits)->QuantumCircuit:
    """Build an ``n_local`` ansatz for the requested number of qubits.

    Args:
        n_qubits: Number of qubits in the ansatz.

    Returns:
        QuantumCircuit: Parameterized ansatz circuit.
    """

    return n_local(
        num_qubits=n_qubits,
        rotation_blocks=["rx", "rz",],
        entanglement_blocks="cx",
        entanglement="linear",
        reps=1,
    )

def _build_1qubit_local_ansatz()->QuantumCircuit:
    """Build a 1-qubit local ansatz.

    Returns:
        QuantumCircuit: Single-qubit variational circuit with ``rx`` and ``rz`` rotations.
    """
    ansatz = QuantumCircuit(1)
    ansatz.rx(Parameter("theta"), 0)
    ansatz.rz(Parameter("phi"), 0)

    return ansatz


def _build_hamiltonian_variational_ansatz(hamiltonian: SparsePauliOp)->QuantumCircuit:
    """Build a Hamiltonian variational ansatz.

    Args:
        hamiltonian: Operator used to generate the variational circuit.

    Returns:
        QuantumCircuit: Hamiltonian variational ansatz circuit.
    """

    return hamiltonian_variational_ansatz(
        hamiltonian=hamiltonian,
    )

def _x0_parameters(n_qubits)->np.ndarray:
    """Generate deterministic initial parameters for the optimizer.

    Args:
        n_qubits: Number of parameters to generate.

    Returns:
        np.ndarray: Seeded random initial parameter vector.
    """
    params = np.random.RandomState(seed=SEED).random(n_qubits)
    return params


def vqe_circuit_builder() -> QuantumCircuit:
    """Run a classical optimization loop over a VQE cost function.

    Returns:
        scipy.optimize.OptimizeResult: Optimization result from ``minimize``.

    Example:
        >>> result = vqe_circuit_builder()
    """

    hamiltonian = _build_hamiltonian_from_op_list()
    ansatz = _build_1qubit_local_ansatz()
    estimator = StatevectorEstimator()

    x0 = _x0_parameters(ansatz.num_parameters)

    result = minimize(
        _cost_function,
        x0=x0,
        args=(ansatz, hamiltonian, estimator,),
        method="SLSQP",
        options={"maxiter": 1000},
    )

    return result

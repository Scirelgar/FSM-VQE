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
    """Build a hamiltonian for the H2 molecule in the STO-6G basis set, reduced to 1 qubit.

    Returns:
        list[tuple[str, float]]: A list of tuples, where each tuple contains a Pauli string and its corresponding coefficient.
    """

    return [("I", -1.04886087), ("Z", -0.7967368), ("X", 0.18121804),]



def _build_hamiltonian_from_op_list(name="h2")->SparsePauliOp:
    """Build a hamiltonian for a molecule.

    Args:
        name (str, optional): The name of the molecule. Defaults to "h2".

    Returns:
        SparsePauliOp: The hamiltonian for the specified molecule.
    """

    if name == "h2":
        return SparsePauliOp.from_list(
            _h2_1qubit_hamiltonian_stog6g_redux()
            )
    
    else:
        raise ValueError(f"Hamiltonian for molecule {name} not implemented.")
    
def _cost_function(params, ansatz, hamiltonian, estimator)->float:
    """Calculate the estimate energy for a given set of parameters."""

    published_estimate = (ansatz, [hamiltonian], [params],)
    result = estimator.run(pubs=[published_estimate],).result()
    energy = result[0].data.evs[0]

    return energy

def _build_n_local_ansatz(n_qubits)->QuantumCircuit:
    """Build a n-local ansatz for a given number of qubits."""

    return n_local(
        num_qubits=n_qubits,
        rotation_blocks=["rx", "rz",],
        entanglement_blocks="cx",
        entanglement="linear",
        reps=1,
    )

def _build_1qubit_local_ansatz()->QuantumCircuit:
    """Build a 1-local ansatz for a given number of qubits."""
    ansatz = QuantumCircuit(1)
    ansatz.rx(Parameter("theta"), 0)
    ansatz.rz(Parameter("phi"), 0)

    return ansatz


def _build_hamiltonian_variational_ansatz(hamiltonian: SparsePauliOp)->QuantumCircuit:
    """Build a hamiltonian variational ansatz for a given number of qubits."""

    return hamiltonian_variational_ansatz(
        hamiltonian=hamiltonian,
    )

def _x0_parameters(n_qubits)->np.ndarray:
    """Build a list of parameters for the initial state of the ansatz."""
    params = np.random.RandomState(seed=SEED).random(n_qubits)
    return params


def vqe_circuit_builder() -> QuantumCircuit:

    hamiltonian = _build_hamiltonian_from_op_list()
    ansatz = _build_1qubit_local_ansatz()
    estimator = StatevectorEstimator()

    x0 = _x0_parameters(ansatz.num_parameters)

    result = minimize(
        _cost_function,
        x0=x0,
        args=(ansatz, hamiltonian, estimator,),
        method="SLSQP",
    )

    return result

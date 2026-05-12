import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import QuantumRegister, ClassicalRegister, Parameter
from qiskit.circuit.library import n_local
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


def vqe_bare():
    """Run a VQE optimization using only the most basic Qiskit components.

    Example:
        >>> vqe_bare()
    """

    qc = QuantumCircuit(1)

    params = [Parameter("theta"), Parameter("phi"),]
    
    # Build the ansatz
    qc.rx(params[0], 0)
    qc.rz(params[1], 0)

    # Build the Hamiltonian
    hamiltonian = _build_hamiltonian_from_op_list()

    # Set up the estimator
    estimator = StatevectorEstimator(seed=SEED)

    # Define the cost function for optimization
    def cost_function(params, ansatz=qc, hamiltonian=hamiltonian, estimator=estimator)->float:
        pub_estimate = (qc, [hamiltonian], [params],)
        result = estimator.run(pubs=[pub_estimate],).result()
        energy = result[0].data.evs[0]
        return energy
    
    # Run the optimization
    initial_params = np.random.RandomState(seed=SEED).rand(len(params))

    optimization_result = minimize(
        cost_function,
        x0=initial_params,
        args=(qc),
        method="SLSQP",
        options={"maxiter": 1000},
    )

    return optimization_result


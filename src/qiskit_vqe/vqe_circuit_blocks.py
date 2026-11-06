import numpy as np
from qiskit.circuit.library import hamiltonian_variational_ansatz
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator
from scipy.optimize import minimize, OptimizeResult


SEED = 156


def _cost_function(params, ansatz, hamiltonian, estimator) -> float:
    """Evaluate the estimated energy for a parameter vector.

    Args:
        params: Ansatz parameters supplied to the estimator.
        ansatz: Quantum circuit representing the variational form.
        hamiltonian: Operator whose expectation value is minimized.
        estimator: Qiskit estimator used to evaluate the energy.

    Returns:
        float: Estimated energy for the supplied parameters.
    """

    pub_estimate = (
        ansatz,
        [hamiltonian],
        [params],
    )
    result = estimator.run(
        pubs=[pub_estimate],
    ).result()
    energy = result[0].data.evs[0]

    return energy


def vqe(input_hamiltonian: SparsePauliOp) -> OptimizeResult:
    """Run a classical optimization loop over a VQE cost function for a supplied Hamiltonian.

    Args:
        input_hamiltonian: Hamiltonian operator to minimize.

    Returns:
        scipy.optimize.OptimizeResult: Optimization result returned by ``minimize``.

    Example:
        >>> from hamiltonian import Hamiltonian
        >>> result = vqe(Hamiltonian.H2_STO6G_REDUX.value)
    """

    ansatz = hamiltonian_variational_ansatz(input_hamiltonian)
    estimator = StatevectorEstimator()

    x0 = np.random.RandomState(seed=SEED).random(ansatz.num_parameters)

    result = minimize(
        _cost_function,
        x0=x0,
        args=(
            ansatz,
            input_hamiltonian,
            estimator,
        ),
        method="SLSQP",
        options={"maxiter": 1000},
    )

    return result

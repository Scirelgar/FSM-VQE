import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator
from scipy.optimize import minimize

SEED = 156


def vqe_bare():
    """Run a VQE optimization using only the most basic Qiskit components.

    Example:
        >>> vqe_bare()
    """
    # Define circuit and parameters objects
    qc = QuantumCircuit(1)

    params = [
        Parameter("theta"),
        Parameter("phi"),
    ]

    # Build the ansatz
    qc.rx(params[0], 0)
    qc.rz(params[1], 0)

    # Build the Hamiltonian
    hamiltonian = SparsePauliOp.from_list(
        [
            ("I", -1.04886087),
            ("Z", -0.7967368),
            ("X", 0.18121804),
        ]
    )

    # Set up the estimator
    estimator = StatevectorEstimator(seed=SEED)

    # Define the cost function for optimization
    def cost_function(
        params, ansatz=qc, hamiltonian=hamiltonian, estimator=estimator
    ) -> float:
        pub_estimate = (
            qc,
            [hamiltonian],
            [params],
        )
        result = estimator.run(
            pubs=[pub_estimate],
        ).result()
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

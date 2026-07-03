import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator
from scipy.optimize import minimize, OptimizeResult

SEED = 156


def vqe_bare(input_hamiltonian: SparsePauliOp) -> OptimizeResult:
    """Run a VQE optimization using only the most basic Qiskit components.

    Args:
        input_hamiltonian: Hamiltonian operator to minimize.

    Returns:
        scipy.optimize.OptimizeResult: Optimization result returned by ``minimize``.

    Example:
        >>> from hamiltonian import Hamiltonian
        >>> result = vqe_bare(Hamiltonian.H2_STO6G_REDUX.value)
    """
    # Define circuit and parameters objects
    qc = QuantumCircuit(1)  # 1 EXIT __init__() + 1 EXIT for arg

    params = [
        Parameter("theta"),
        Parameter("phi"),
    ]

    # Build the ansatz
    qc.rx(params[0], 0)
    qc.rz(params[1], 0)

    qc.draw("mpl")  # PIN

    # Build the Hamiltonian
    hamiltonian = input_hamiltonian

    # Set up the estimator
    estimator = StatevectorEstimator(seed=SEED)  # 1 EXIT __init__() + 1 EXIT arg

    # Define the cost function for optimization
    def cost_function(  # 1 Trig ENTRY + 4 ENTRIES for arg
        params, ansatz=qc, hamiltonian=hamiltonian, estimator=estimator
    ) -> float:

        pub_estimate = (
            ansatz,
            [hamiltonian],
            [params],
        )

        # This is where quantum execution happens (could be extracted)
        result = estimator.run(  # 1 EXIT method call QC
            pubs=[pub_estimate],  # 1 EXIT tuple arg CL or QC?
        ).result()  # 1 EXIT CL
        energy = result[0].data.evs[0]  # PIN (HOW MANY ENTRIES)
        return energy  # 1 EXIT to whoever called

    # Run the optimization
    initial_params = np.random.RandomState(seed=SEED).rand(len(params))
    # 1 EXIT RandomState __init__(1 EXIT arg)
    # 1 EXIT len( 1 EXIT arg)
    # 1 EXIT rand()

    optimization_result = minimize(  # 1 EXIT
        cost_function,  # 1 EXIT
        x0=initial_params,  # 1 EXIT
        args=(qc),  # 1 EXIT
        method="SLSQP",  # 1 EXIT
        options={"maxiter": 1000},  # 1 EXIT
    )

    return optimization_result  # 1 EXIT of vqe_bare()

from numpy.random import RandomState
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator
from scipy.optimize import minimize, OptimizeResult

SEED = 156


def vqe(
    input_hamiltonian: SparsePauliOp,
) -> OptimizeResult:  # +1 Triggering Entry, +1 Entry for the argument
    """Run a VQE optimization using only the most basic Qiskit components.

    Args:
        input_hamiltonian: Hamiltonian operator to minimize.

    Returns:
        scipy.optimize.OptimizeResult: Optimization result returned by ``minimize``.

    Example:
        >>> from hamiltonian import Hamiltonian
        >>> result = vqe(Hamiltonian.H2_STO6G_REDUX.value)
    """
    # Define circuit and parameters objects
    qc = QuantumCircuit(1)
    """
    FU vqe (classical)
    FP Quantum Circuit (quantum) : +1 Triggering Entry, +1 Entry for the argument, +1 Exit for the object QuantumCircuit
    
    """

    params = [
        Parameter("theta"),
        Parameter("phi"),
    ]
    """
    FU vqe (classical)
    FP params (quantum) : +1 Triggering Entry coming from vqe, +1 Entry for arguments, +1 Exits going back to vqe 
    """

    # Build the ansatz
    qc.rx(params[0], 0)
    qc.rz(params[1], 0)

    """
    FU vqe (classical)
    FU QuantumCircuit (quantum) : +2 Entries (one for each gates)
    FP RX (quantum) : +2 Entries for arguments, +1 Triggering Entry, +1 Exit towards qc

    FP RZ (quantum) : +2 Entries for argument, +1 Triggering Entry, +1 Exit towards qc

    """

    # Build the Hamiltonian
    hamiltonian = input_hamiltonian

    # Set up the estimator
    estimator = StatevectorEstimator(seed=SEED)  # __init__()

    """
    FU vqe (classical)
    FP StatevectorEstimator (quantum) : +1 triggering Entry, +1 Exit (object)
    """

    # Define the cost function for optimization
    def cost_function(
        params, ansatz=qc, hamiltonian=hamiltonian, estimator=estimator
    ) -> float:

        pub_estimate = (
            ansatz,
            [hamiltonian],
            [params],
        )

        # This is where quantum execution happens (could be extracted)
        result = estimator.run(
            pubs=[pub_estimate],
        ).result()
        """
        FU cost_function (classical)
        FP statevector_estimator.run() (quantum) : +1 Triggering Entry, +1 Entry for argument, +1 Exit for PrimitiveJob

        --------------------------------------------------------
        
        FU cost_function (classical)
        FP PrimitiveJob.result() (quantum) : +1 Triggering Entry, +1 Exit for PrimitiveResult        
        """

        energy = result[0].data.evs[0]
        return energy

    # Run the optimization
    initial_params = RandomState(seed=SEED).rand(len(params))
    """
    FU vqe

    FP RandomState.rand() (quantum) : +1 Triggering Entry, +2 Entries for arguments, +2 Exits for values of parameters

    Total : 5
    """

    optimization_result = minimize(
        cost_function,
        x0=initial_params,
        args=(qc),
        method="SLSQP",
        options={"maxiter": 1000},
    )
    """
    FU vqe (classical)
    FP minimize (classical) : + 1 Triggering Entry, +5 Entries for arguments, +1 Exit for OptimizeResult
    """

    return optimization_result  # 1 EXIT of vqe()

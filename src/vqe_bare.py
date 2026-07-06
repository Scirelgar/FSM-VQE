import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator
from scipy.optimize import minimize, OptimizeResult

SEED = 156

"""
FP vqe_bare

"""
def vqe_bare(input_hamiltonian: SparsePauliOp) -> OptimizeResult: # +1 Triggering Entry, +1 Entry for the argument
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
    qc = QuantumCircuit(1)
    """
    FP vqe_bare (classical) : +1 Exit, +1 Exit for the parameter, +1 Entry for the object QuantumCircuit


    FP Quantum Circuit (quantum) : +1 Triggering Entry, +1 Entry for the argument, +1 Exit for the object QuantumCircuit
    
    """

    params = [
        Parameter("theta"),
        Parameter("phi"),
    ]
    """
    FP vqe_bare (classical) : +2 Exit  Parameter (trigger+argument), +1 Entry  Parameter coming back

    FP params (quantum) : +1 Triggering Entry coming from vqe_bare , +1 Entry for arguments , +1 Exits going back to vqe_bare 
    
    Total of exchange : 6
    """

    # Build the ansatz
    qc.rx(params[0], 0)
    qc.rz(params[1], 0)
   
    """
    FP vqe_bare (classical) : +2 Exits trig. each gates, +4 Exits for arguments

    FP RX (quantum) : +2 Entries for arguments, +1 Triggering Entry, +1 Exit towards qc

    FP RZ (quantum) : +2 Entries for argument, +1 Triggering Entry, +1 Exit towards qc

    FP QuantumCircuit (quantum) : +2 Entries (one for each gates)
    
    """

    qc.draw("mpl")  # PIN

    # Build the Hamiltonian
    hamiltonian = input_hamiltonian

    # Set up the estimator
    estimator = StatevectorEstimator(seed=SEED) #__init__()

    """
    FP vqe_bare (classical) : +1 Exit (trigger), +1 Entry (object)

    FP StatevectorEstimator (quantum) : +1 triggering Entry, +1 Exit (object)
    """

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
    """
    FP vqe_bare : +1 Exit (trigger), +2 Exit for arguments, +2 Entries for values of parameters

    FP np.rand() (quantum) : +1 Triggering Entry, +2 Entries for arguments, +2 Exits for values of parameters

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
    FP vqe_bare (classical) : +1 Exit (trigger), +5 Exits for arguments, +1 Entry for OptimizeResult

    FP minimize (classical) : 
    
    """

    return optimization_result  # 1 EXIT of vqe_bare()

"""Demonstrate a VQE functional process from an external user's perspective.

For functional size measurement, this module impersonates a domain user that
supplies a Hamiltonian and consumes the VQE result. The module, including its
orchestration and output, is outside the measured VQE software boundary.
"""

from hamiltonian import Hamiltonian
from qiskit_vqe import vqe_circuit_blocks as vqe


def main(hamiltonian: Hamiltonian = Hamiltonian.H2_STO6G_REDUX):
    """Run the configured VQE variant as an external user and print its result.

    Args:
        hamiltonian: Hamiltonian enum value supplied to the VQE functional process.

    Returns:
        None: This function prints the optimization result and does not return a value.

    Example:
        >>> main()
    """

    vqe_result = vqe.vqe(
        hamiltonian.value
    )  # Data movement with vqe(): +1 Entry for OptimizeResult, +1 Exit Hamiltonian, +1 Exit triggering vqe()
    print(vqe_result)


if __name__ == "__main__":
    main()  # Data movement with System (launch of main.py): +1 Triggering Entry


# Total for FU main() = 4 CFPs

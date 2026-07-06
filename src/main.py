from hamiltonian import Hamiltonian
from vqe_bare import vqe_bare
from vqe_circuit_blocks import vqe_circuit_builder
from vqe_subroutine import vqe_subroutine


def main(hamiltonian: Hamiltonian = Hamiltonian.H2_STO6G_REDUX):
    """Run all VQE implementations for a given Hamiltonian and print the results.

    Args:
        hamiltonian: Hamiltonian enum value to pass to the implementations that consume it.

    Returns:
        None: This function prints each optimization result and does not return a value.

    Example:
        >>> main()
    """

    vqe_result = vqe_subroutine(hamiltonian.value)
    print(vqe_result)
    vqe_result = vqe_circuit_builder(hamiltonian.value)
    print(vqe_result)
    vqe_result = vqe_bare(hamiltonian.value) # Data movement with vqe_bare(): +1 Entry for OptimizeResult, +1 Exit Hamiltonian, +1 Exit triggering vqe_bare()
    print(vqe_result)


if __name__ == "__main__":
    main() # Data movement with System (launch of main.py): +1 Triggering Entry


# Total for FU main() = 4 CFPs

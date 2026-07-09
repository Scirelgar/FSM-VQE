from hamiltonian import Hamiltonian
import vqe_bare


def main(hamiltonian: Hamiltonian = Hamiltonian.H2_STO6G_REDUX):
    """Run all VQE implementations for a given Hamiltonian and print the results.

    Args:
        hamiltonian: Hamiltonian enum value to pass to the implementations that consume it.

    Returns:
        None: This function prints each optimization result and does not return a value.

    Example:
        >>> main()
    """

    vqe_result = vqe_bare.vqe(
        hamiltonian.value
    )  # Data movement with vqe(): +1 Entry for OptimizeResult, +1 Exit Hamiltonian, +1 Exit triggering vqe()
    print(vqe_result)


if __name__ == "__main__":
    main()  # Data movement with System (launch of main.py): +1 Triggering Entry


# Total for FU main() = 4 CFPs

from vqe_bare import vqe_bare
from vqe_circuit_blocks import vqe_circuit_builder
from vqe_subroutine import vqe_subroutine


def main():
    """Run both VQE entry points and print their results.

    Example:
        >>> main()
    """

    vqe_result = vqe_subroutine()
    print(vqe_result)
    vqe_result = vqe_circuit_builder()
    print(vqe_result)
    vqe_result = vqe_bare()
    print(vqe_result)


if __name__ == "__main__":
    main()

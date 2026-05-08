from vqe_circuit_builder import vqe_circuit_builder
from vqe_subroutine import vqe_subroutine


def main():

    vqe_result = vqe_subroutine()
    print(vqe_result)
    vqe_result = vqe_circuit_builder()
    print(vqe_result)


if __name__ == "__main__":
    main()

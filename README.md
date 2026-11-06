# VQE-FSM

VQE-FSM is an experimental Python codebase for studying functional size measurement (FSM) in hybrid quantum-classical software. It deliberately focuses on one subcategory of hybrid application—the Variational Quantum Eigensolver (VQE)—so that manual and automated measurements can be compared against a small, controlled source base.

## Project vision

The project treats a VQE implementation as a functional process with a simple domain-facing responsibility:

1. A functional user, such as a chemist, supplies a Hamiltonian representation of a molecule or other quantum system.
2. A selected VQE variant constructs and optimizes an ansatz against that Hamiltonian using quantum and classical components.
3. The process provides the estimated ground-state energy to the functional user.

The research goal is to maintain comparable implementations of that responsibility at different levels of abstraction, then measure their functional size both manually and with automated techniques. The project is not intended to represent every kind of hybrid quantum-classical application; conclusions drawn from it are scoped specifically to VQE workflows.

The first iteration established the workflow from scratch: it manually constructed the required ansatz for a single, known Hamiltonian and recorded data-movement annotations for manual measurement. Later variants retain the same functional intent while delegating more of the workflow to library abstractions. This makes the codebase useful for examining how implementation structure and abstraction affect a measurement while the user-recognizable function remains stable.

## Functional measurement boundary

The measured software is the selected VQE functional process. Its input is a supplied Hamiltonian, and its output of interest is the estimated ground-state energy.

`src/main.py` is outside this measurement boundary. It is a demonstration client that impersonates the external functional user: it selects a Hamiltonian, hands it to a VQE variant, and displays the result. Its orchestration and printing are not part of the VQE functional size. Existing data-movement annotations are retained as historical measurement material, but annotations concerning `main.py` should not be included in measurements made under the current boundary.

The current VQE callables return library result containers (`OptimizeResult` or `VQEResult`) that contain the estimated energy. Normalizing those callables so that they return only the ground-state energy is part of the target interface, not a claim about the present implementation.

## Implementations

The repository currently contains three VQE variants:

| Variant | Role in the comparison |
| --- | --- |
| `src/legacy/vqe_bare.py` | Original baseline that manually assembles the ansatz and optimization workflow in one VQE function. |
| `src/qiskit_vqe/vqe_circuit_blocks.py` | Explicit cost function and classical optimization loop with a library-provided Hamiltonian variational ansatz. |
| `src/qiskit_vqe/vqe_subroutine.py` | Higher-level implementation delegated to the `qiskit-algorithms` VQE subroutine. |

The supplied `H2_STO6G_REDUX` Hamiltonian keeps the reference scenario reproducible. It is an example input, not a restriction on the conceptual VQE interface, which accepts a Hamiltonian supplied by the functional user.

## Installation

The project targets Python 3.14 or newer. `uv` is the recommended way to create the environment and install dependencies from `pyproject.toml`.

If you do not already have `uv`, install it first from <https://docs.astral.sh/uv/>.

```bash
uv sync
```

## Usage

Run the demonstration client to execute the currently selected VQE variant with the reference Hamiltonian and print its result:

```bash
uv run python src/main.py
```

The client is useful for exercising the workflow, but it remains outside the functional measurement boundary described above.

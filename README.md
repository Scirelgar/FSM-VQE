# VQE-FSM

VQE-FSM is a Python project implementing different Variational Quantum Eigensolver (VQE) workflows to apply functional software measurement techniques. It includes three implementations of the same H2 example: one built directly using a Qiskit VQE subroutine from the `qiskit.algorithms` module, one that uses helper functions to construct the optimization component by blocks, and one that builds the entire optimization workflow in just one method.

## Installation

The project targets Python 3.14 or newer. `uv` is the recommended way to create the environment and install dependencies from `pyproject.toml`.

If you do not already have `uv`, install it first from <https://docs.astral.sh/uv/>.

```bash
uv sync
```

You can also run the project without activating the environment explicitly:

```bash
uv run python src/main.py
```

## Usage

Run the main entry point to execute all three VQE variants and print their results:

```bash
uv run python src/main.py
```

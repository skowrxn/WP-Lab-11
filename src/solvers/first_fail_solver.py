from __future__ import annotations
from dataclasses import dataclass
from typing import NewType
from src.solvers.solver import SudokuSolver
from src.model.grid import SudokuGrid
from src.utils.recursion_limit import recursion_limit_set_to  # noqa


Variable = NewType("Variable", tuple[int, int, int])
"""Type representing a single variable identifier, it's a tuple with
   the variable's coordinates(row index, col index, block index)"""

Domain = NewType("Domain", set[int])
"""Type representing set of of available values"""


@dataclass(frozen=True, slots=True)
class State:
    """
    Represent the current state of the backtracking solver.

    Attributes:
    -----------
    grid: SudokuGrid
        a current state of the grid
    free_variables: set[Variable]
        set of the variables without assigned values
    row_domains: list[Domain]
        set of values available in the given row, e.g.
            row_domains[5] = {1,2,3,4}
        means the {1,2,3,4} can be assigned in row 5
    col_domains: list[Domain]
        set of values available in the given column
    block_domains: list[Domain]
        set of values available in the given block
    """

    grid: SudokuGrid
    free_variables: set[Variable]
    row_domains: list[Domain]
    col_domains: list[Domain]
    block_domains: list[Domain]

    def domain(self, variable: Variable) -> Domain:
        """
        Return domain (available values) for the given variable.

        Parameters
        -----------
        variable: Variable
            a variable whose domain we want to get


        Returns
        --------
        domain: Domain
            values available for the given domain
        """
        raise NotImplementedError("copy from the previous lab")

    def assign(self, variable: Variable, value: int) -> None:
        """
        Assigns a given value to a given variable.

        Parameters
        -----------
        variable: Variable
            variable to be assigned to
        value: int
            what value should we assign
        """
        raise NotImplementedError("copy from the previous lab")

    def remove_assignment(self, variable: Variable) -> None:
        """
        Removes a value assignment.

        Parameters
        -----------
        variable: Variable
            an already assigned variable
        """
        raise NotImplementedError("copy from the previous lab")

    @staticmethod
    def from_grid(grid: SudokuGrid) -> State:
        """
        Creates an initial state for a given grid.

        Parameters
        -----------
        grid: SudokuGrid
            an initial state of the sudoku grid

        Returns
        --------
        state: State
            a state matching the grid
        """
        default_domain = set(range(1, grid.size+1))
        free_variables = set()
        row_domains = [Domain(default_domain.copy()) for _ in range(grid.size)]
        col_domains = [Domain(default_domain.copy()) for _ in range(grid.size)]
        block_domains = [Domain(default_domain.copy()) for _ in range(grid.size)]

        for (row, col), val in grid.enumerate():
            block = grid.block_index(row, col)
            if val != 0:
                row_domains[row].remove(val)
                col_domains[col].remove(val)
                block_domains[block].remove(val)
            else:
                free_variables.add(Variable((row, col, block)))

        return State(grid, free_variables, row_domains, col_domains, block_domains)

class FirstFailSudokuSolver(SudokuSolver):
    """
    A first-fail backtracking sudoku solver.
    It first tries to fill cells with smallest number of available values.
    """

    state: State

    def __init__(self, puzzle, time_limit):
        super().__init__(puzzle, time_limit)
        self.state = State.from_grid(puzzle)

    def run_algorithm(self) -> SudokuGrid | None:
        with recursion_limit_set_to(self._puzzle.size**3):
            if self._dfs():
                return self.state.grid
            return None

    def _dfs(self) -> bool:
        """
        Performs a first-fail depth-first-search to solve the sudoku puzzle.
        It always chooses a variable with the smallest domain and tries it first.

        Returns
        --------
        solved: bool
            `True` - if method found the solution
            `False` - otherwise
        """
        raise NotImplementedError("copy from the previous lab")

    def _choose_variable(self) -> tuple[Variable, Domain] | None:
        """
        Finds a free variable with the smallest domain.

        Returns
        --------
        var_dom: tuple[Variable, Domain] | None:
            if there are no free variables left,returns `None`
            otherwise returns a variable with the smallest domain (together with its domain)
        """
        raise NotImplementedError("copy from the previous lab")

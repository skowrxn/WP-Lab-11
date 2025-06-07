from __future__ import annotations
from dataclasses import dataclass
import itertools
from threading import Timer
from typing import Iterable
from src.solvers.solver import SudokuSolver
from src.model.grid import SudokuGrid
from pysat.formula import CNF  # type: ignore[import-untyped]
from pysat.solvers import Solver  # type: ignore[import-untyped]
from src.utils.group_by import group_by


@dataclass(frozen=True)
class Coordinates:
    """
    Represent coordinates of a sudoku variable (empty cell).
    """

    row: int
    col: int
    block: int


@dataclass(frozen=True)
class Proposition:
    """
    A single proposition:
    "Sudoku cell at coordinates: `coords` has value `val`"
    """

    coords: Coordinates
    val: int
    id: int


@dataclass
class SudokuCNF:
    """
    Represents a sudoku puzzle using a `Conjunctive Normal Form`:
    - https://en.wikipedia.org/wiki/Conjunctive_normal_form
    - https://equaeghe.github.io/ecyglpki/cnfsat.html

    Usage
    -----
    Given a sudoku `grid: SudokuGrid` one should use static method `encode`
    to create a CNF representation:

        `sudoku_cnf = SudokuCNF.encode(grid)`

    To pass the representation into a SAT solver, one should use the `cnf` property:

        `with Solver(bootstrap_with=sudoku_cnf.cnf) as solver`

    Given a solution from a SAT solver (e.g. `solution = solver.get_model()`)
    one can translate it to a SudokuGrid via the `decode` method:

        `solution_grid =  sudoku_cnf.decode()`

    """

    cnf: CNF
    """a `Conjunctive Normal Form` encoding as used by a SAT solver"""
    propositions: dict[int, Proposition]
    """mapping from propositions identifiers (as used in the CNF)
       to the propositions themselves"""
    puzzle: SudokuGrid
    """a puzzle encoded in the CNF"""

    def __post_init__(self) -> None:
        self._every_cell_has_a_single_value()
        self._every_row_contains_unique_values() 
        self._every_col_contains_unique_values()
        self._every_block_contains_unique_values()

    def _at_least_one(self, propositions: Iterable[Proposition]) -> None:
        self.cnf.append([p.id for p in propositions])

    def _at_most_one(self, propositions: Iterable[Proposition]) -> None:
        for p, q in itertools.combinations(propositions, 2):
            self.cnf.append([-p.id, -q.id])

    def _exactly_one(self, propositions: Iterable[Proposition]) -> None:
        self._at_most_one(propositions)
        self._at_least_one(propositions)

    def _every_cell_has_a_single_value(self):
        for cell_propositions in group_by(
            self.propositions.values(), lambda p: p.coords
        ).values():
            self._exactly_one(cell_propositions)

    def _every_row_contains_unique_values(self):
        for row_val_proposition in group_by(
                self.propositions.values(),
                lambda p: (p.coords.row, p.val)
        ).values():
            self._at_most_one(row_val_proposition)

    def _every_col_contains_unique_values(self):
        for col_val_proposition in group_by(self.propositions.values(),
                                            lambda p: (p.coords.col, p.val)).values():
            self._at_most_one(col_val_proposition)

    def _every_block_contains_unique_values(self):
        for block_val_proposition in group_by(self.propositions.values(),
                                              lambda p: (self.puzzle.block_index(p.coords.row, p.coords.col), p.val)).values():
            self._at_most_one(block_val_proposition)

    @staticmethod
    def encode(puzzle: SudokuGrid) -> SudokuCNF:
        """
        Encodes a given sudoku puzzle into its Conjunctive Normal Form
        suitable for SAT solvers.

        Parameters
        ----------
        puzzle: SudokuGrid
            a sudoku puzzle to be encoded

        Returns
        -------
        encoding: SudokuCNF
            Conjunctive Normal Form encoding of the specified puzzle
        """
        cnf = CNF()
        propositions = SudokuCNF._possible_propositions(puzzle)
        return SudokuCNF(cnf, propositions, puzzle)

    def decode(self, results: list[int]) -> SudokuGrid:
        """
        Decodes a SAT solution into a filled sudoku grid.

        Parameters
        ----------
        results: list[int]
            list of true propositions (their identifiers, to be exact)
            [1,-2,3,-4,5] would mean, that propositions 1,3,5 are true
            and 2 and 5 are false.

        Returns
        -------
        solution: SudokuGrid
            a sudoku grid filled according the SAT results
        """

        valid_ids = [prop_id for prop_id in results if prop_id >= 0]
        valid_propositions = [self.propositions[valid_prop_id] for valid_prop_id in valid_ids]
        solved_puzzle = self.puzzle.copy()

        for valid_proposition in valid_propositions:
            solved_puzzle.__setitem__(valid_proposition.coords, valid_proposition.val)

        return solved_puzzle

        # TODO:
        # Implement the method according to the docstring.
        # 1. remember to copy `self.puzzle`
        # 2. for every **true** proposition in the results
        #    assign a corresponding value at the corresponding coordinates
        #    in the puzzle copy
        # 3. return the filled grid
        #raise NotImplementedError("not implemented yet")

    @staticmethod
    def _possible_propositions(puzzle: SudokuGrid) -> dict[int, Proposition]:
        size = puzzle.size
        id_counter = 1
        result = {}
        default_domain = set(range(1, size + 1))
        row_taken = {i: set() for i in range(size)}
        col_taken = {i: set() for i in range(size)}
        block_taken = {i: set() for i in range(size)}
        
        for (row, col), val in puzzle.enumerate():
            if val != 0:
                block = puzzle.block_index(row, col)
                row_taken[row].add(val)
                col_taken[col].add(val) 
                block_taken[block].add(val)
        
        for (row, col), val in puzzle.enumerate():
            if val != 0:
                continue
            block = puzzle.block_index(row, col)
            valid = default_domain - (row_taken[row] | col_taken[col] | block_taken[block])
            for val in valid:
                result[id_counter] = Proposition(Coordinates(row, col, block), val, id_counter)
                id_counter += 1
        
        return result


class SatSudokuSolver(SudokuSolver):
    """
    A SAT-based sudoku solver using the python-sat library:
    - what is a SAT-solver: https://en.wikipedia.org/wiki/SAT_solver

    - python-sat basic usage: https://pysathq.github.io/usage/\n
      look especially at an example starting with `formula = CNF()`

    - python-sat docs: https://pysathq.github.io/docs/html/index.html#supplementary-examples-package
    """

    def __init__(self, puzzle, time_limit):
        super().__init__(puzzle, time_limit)

    def run_algorithm(self) -> SudokuGrid | None:



        # TODO:
        # Use python-sat to solve to sudoku!
        #
        # General tip: read SudokuCNF documentation at the top of this file
        #
        # 1. encode `self._puzzle` into a CNF
        #    via `SudokuCNF.encode`
        # 2. build solver via context manager
        #    - a basic example is shown here:
        #       https://pysathq.github.io/docs/html/api/solvers.html#pysat.solvers.Solver.accum_stats
        #    - `cnf` is a property of the SudokuCNF you have already built
        #    - we don't need the `accum_stats()`
        # 3. handle timeout as stated here:
        #    - https://pysathq.github.io/docs/html/api/solvers.html#pysat.solvers.Solver.interrupt
        #    - in other words:
        #       * use solve_limited expecting an interrupt
        #       * run Timer with self._timelimit to interrupt the solver
        #       * the example on the page is missing a single line.
        #         After solver finds a solution one should cancel the timer via `timer.cancel()`.
        #         Otherwise the timer will interrupt the already finished solver.
        # 4. `solve_limited` returns status:
        #   - `None` means there was an interruption/timeout
        #      * we should raise a TimeoutError
        #   - `False` means the solver failed to find a solution
        #      * we should also return `None`
        #   - `True` means the solver found a solution
        #      * we should return "decoded" solution.
        #        Use `decode` method of the SudokuCNF object.
        raise NotImplementedError("not implemented yet")

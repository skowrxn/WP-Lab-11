from abc import ABC, abstractmethod
from src.model.grid import SudokuGrid
from timeit import default_timer as timer


class SudokuSolver(ABC):
    """
    An abstract class defining a sudoku solver.
    Every sudoku solver is supposed to inherit from this class
    and implement the `run_algorithm` method.

    Protected Attributes:
    ---------------------
    _puzzle: SudokuGrid
        **copy** of the sudoku puzzle to be solved. Solvers can modify this grid.
    _time_limit: float
        how much time is available for the solver
    _deadline: float
        a deadline used in the built-in _timeout() method

    Methods:
    --------
    _timeout() -> bool:
        checks whether the available time has run out

    Abstract Methods:
    -----------------
    run_algorithm(self) -> SudokuGrid | None:
        implements the specific solving algorithm

    Class Methods:
    --------------
    solve(cls, puzzle: SudokuGrid, time_limit: float, *args, **kwargs) -> SudokuGrid | None:
        an interface method supposed dispatch correct algorithm
    """

    _puzzle: SudokuGrid
    _time_limit: float
    _deadline: float

    def __init__(self, puzzle: SudokuGrid, time_limit: float) -> None:
        self._puzzle = puzzle.copy()
        self._time_limit = time_limit
        self._deadline = timer() + time_limit

    def _timeout(self) -> bool:
        """
        Checks whether the available time has run out.

        Returns
        --------
        timeout: bool
            - `True` if solver has missed the deadline
            - `False` otherwise
        """
        return timer() > self._deadline

    @abstractmethod
    def run_algorithm(self) -> SudokuGrid | None:
        """
        A method implementing the solving algorithm.

        Return:
        --------
        solution: SudokuGrid | None:
            - a sudoku solution if it has been found
            - `None` if the solution has not been found

        Raises:
        -------
        timeout_error: TimeoutError
            when the available time runs out
        """
        pass

    @classmethod
    def solve(
        cls, puzzle: SudokuGrid, time_limit: float, *args, **kwargs
    ) -> SudokuGrid | None:
        """
        Solves the given sudoku puzzle within a specified time limit using
        the solver implement within the class `cls`.

        Returns
        --------
        solution: SudokuGrid | None:
            - a sudoku solution if it has been found
            - `None` if the solution has not been found

        Raises
        -------
        timeout_error: TimeoutError
            when the available time runs out

        Parameters
        -----------
        puzzle: SudokuGrid
            a sudoku puzzle to be solved
        time_limit: float
            amount of time (in seconds) available to the solver
        *args: Any
            extra arguments passed to the solver constructor
        **kwargs: Any
            extra named arguments passed to the solver constructor
        """
        solver = cls(puzzle, time_limit, *args, **kwargs)
        return solver.run_algorithm()

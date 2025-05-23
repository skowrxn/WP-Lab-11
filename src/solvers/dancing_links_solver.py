from ctypes import CDLL, c_int, Array
from multiprocessing import Queue, Process
from pathlib import Path

import numpy as np
from src.solvers.solver import SudokuSolver
from src.model.grid import SudokuGrid


class DancingLinksSudokuSolver(SudokuSolver):
    """
    This solver uses the famous Knuth's Algorithm X.
    We will outsource work to the existing implementation in C:
        https://github.com/nstagman/exact_cover_sudoku
    """

    def run_algorithm(self) -> SudokuGrid | None:
        raise NotImplementedError("copy from the previous lab")

    def _communicate_with_external_solver(self, queue: Queue) -> None:
        """
        Calls the external solver and returns result via the queue.

        Parameters
        -----------
        queue: Queue
            queue used to return the result
        """
        raise NotImplementedError("copy from the previous lab")

    def _get_lib(self) -> CDLL:
        """
        Loads the library containing the solver.

        Returns
        --------
        library: CDLL
            a library containing the algorithm implementation
        """

        # TODO:
        # You don't have to write any code here, but you create the library
        # and put in at the `lib/ss.so` path.
        #
        # How to build the library:
        # - download code from https://github.com/nstagman/exact_cover_sudoku
        # - open the `c` directory
        # - modify the `sudoku_solve.c` file by adding
        #   `import <Python.h>` somewhere at the top
        #   it is required by the file to be easily called from Python
        # - modify the `makefile`:
        #   0. rename EXE to `ss.so`
        #   1. remove two lines starting with `run: $(EXE)`.
        #      we won't run the code directly
        #   2. add `-fPIC -shared` to CFLAGS, so the code would compile to a shared library
        #   3. find location of your python development files,
        #      if you are using `uv`, it should be something like this:
        #      - include_path: /home/user/.local/share/uv/python/cpython-3.13.3-linux-x86_64-gnu/include/python3.13
        #      - lib_path: /home/user/.local/share/uv/python/cpython-3.13.3-linux-x86_64-gnu/lib
        #   4. add `-I<include_path>` to the CFLAGS, e.g.
        #      -I/home/user/.local/share/uv/python/cpython-3.13.3-linux-x86_64-gnu/include/python3.13
        #   5. add `-L<lib_path> to the LFLAGS, e.g.
        #      LFLAGS := -lm -L/home/user/.local/share/uv/python/cpython-3.13.3-linux-x86_64-gnu/lib
        #   6. run `make`
        #   It should create the `ss.so` file you can copy to `lib` directory.
        LIB_PATH = Path("lib").joinpath("ss.so")
        return CDLL(LIB_PATH)

    def _c_args(self) -> tuple[Array[c_int], c_int, Array[c_int]]:
        """
        Translates sudoku puzzle to the arguments used by the solver.

        Returns
        --------
        size: c_int
            a c_int object with size of the puzzle, `9` for the classical one
        puzzle_array: Array[c_int]
            a flat array containing the initial state of the puzzle
        solution_array: Array[c_int]
            a flat array of the same same as puzzle_array, but containing only zeros
        """
        raise NotImplementedError("copy from the previous lab")

    def _grid_from_array(self, solution: Array[c_int]) -> SudokuGrid:
        """
        Translates the C array into a sudoku grid.

        Parameters
        ----------
        solution: Array[c_int]
            an array containing the solution

        Returns
        --------
        grid: SudokuGrid
            a sudoku grid corresponding to the array
        """
        raise NotImplementedError("copy from the previous lab")

    def _run_algorithm(self) -> SudokuGrid | None:
        """
        Runs the algorithm.

        Returns
        --------
        grid: SudokuGrid | None
            `None` if the algorithm failed, otherwise a solution
        """
        dll = self._get_lib()

        puzzle_array, size, solution_array = self._c_args()
        result = dll.solve_puzzle(puzzle_array, size, solution_array)
        if result == 0:
            return None

        return self._grid_from_array(solution_array)

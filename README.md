# Very Satisfying Sudoku Solver

This project aims to produce a solver for the general [sudoku puzzle](https://en.wikipedia.org/wiki/Sudoku). The general variant is basically the sudoku with no specific size. Classically, the sudoku uses `9`x`9` grid, but in general it can any size divisible into equal blocks, e.g., `4`x`4`, `16`x`16`, `25`x`25`, etc.

This time we will use an existing SAT solver to solve the sudoku efficiently. Using existing efficient solvers is probably the best approach to solve computational problems in Python.

Sources:
- [what is a SAT solver](https://en.wikipedia.org/wiki/Solver)
- [webpage of the SAT library we use](https://pysathq.github.io/)
- [quite nice SAT tutorial for programmers](https://sat.inesc-id.pt/~ines/publications/aimath06.pdf)
- [paper this lab is based on](https://sat.inesc-id.pt/~ines/publications/aimath06.pdf)

## TODO: 

There are several tasks to complete:
- [ ] reuse configuration from the previous lab
    - [ ] add (`uv add`) new dependency `python-sat`
- [ ] copy already implemented methods from the previous lab
- [ ] implement:
    - `src/utils/group_by.py` — a utility function to group elements into a dictionary
    - `src/solvers/sat_solver.py` — solver using a SAT solver
- [ ] use `benchmark.py` to compare your solvers
- [ ] keep your code tidy by running `ruff format` and `ruff check` or using vs code `ruff` extension
    - bobot won't give points if your file is not well formatted 


## Grading

* [ ] Make sure, you have a **private** group
  * [how to create a group](https://docs.gitlab.com/ee/user/group/#create-a-group)
* [ ] Fork this project into your private group
  * [how to create a fork](https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html#creating-a-fork)
* [ ] Add @bobot-is-a-bot as the new project's member (role: **maintainer**)
  * [how to add an user](https://docs.gitlab.com/ee/user/project/members/index.html#add-a-user)

## How To Submit Solutions

* [ ] Clone repository: git clone:
    ```bash
    git clone <repository url>
    ```
* [ ] Solve the exercises
    * use WebIDE, whatever
* [ ] Commit your changes
    ```bash
    git add <path to the changed files>
    git commit -m <commit message>
    ```
* [ ] Push changes to the gitlab master branch
    ```bash
    git push 
    ```

The rest will be taken care of automatically. You can check the `GRADE.md` file for your grade / test results. Be aware that it may take some time (up to one hour) till this file appears.

## Project Structure

    .
    ├── puzzles                     # contains puzzles of various sizes
    ├── src                         # source directory
    │   ├── model                   # - directory with the problem model 
    │   │   └── grid.py             # representation of the sudoku grid
    │   ├── solvers                 # TODO: directory with the sudoku solvers
    │   └── utils                   # TODO: various utilities              
    ├── benchmark.py                # you may use this script to compare solvers
    ├── main.py                     # TODO: create this file with `uv init`
    ├── pyproject.toml              # TODO: create this file with `uv init`
    └── README.md                   # the README you are reading now
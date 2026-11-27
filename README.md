# kipro_wi

Course material for modelling and solving combinatorial problems with constraint programming.
Each lecture folder contains small examples, usually first written in
[MiniZinc](https://www.minizinc.org/) and then translated to Python with
[Google OR-Tools](https://developers.google.com/optimization) (CP-SAT solver).

## Contents

### [lecture2](lecture2/): Decision variables and constraints

| File | What it shows |
|---|---|
| [australia.mzn](lecture2/australia.mzn) | Map colouring of Australia in MiniZinc |
| [australia_ortools.py](lecture2/australia_ortools.py) | The same model in OR-Tools, translated line by line |
| [australia_ortools.ipynb](lecture2/australia_ortools.ipynb) | Notebook version: solves the model, draws the map and lists all solutions |
| [australia_viz.py](lecture2/australia_viz.py) | Drawing helpers used by the notebook (`draw_map`, `draw_all`) |
| [decision_variables_ortools.py](lecture2/decision_variables_ortools.py) | How MiniZinc variable declarations (enums, ranges, Booleans, unbounded `int`) look in OR-Tools |
| [parameters_ortools.py](lecture2/parameters_ortools.py) | How MiniZinc parameters (fixed constants) look in Python, and how to use them in a model |
| [boolean_conditions_ortools.py](lecture2/boolean_conditions_ortools.py) | and, or, not, implication, counting and xor in CP-SAT |
| [harbour_ortools.py](lecture2/harbour_ortools.py) | Ship assignment: boats to docks, with restricted domains |
| [harbour_ortools.ipynb](lecture2/harbour_ortools.ipynb) | Notebook version: solves the model, draws the harbour and a selection of all solutions |
| [harbour_viz.py](lecture2/harbour_viz.py) | Drawing helpers used by the harbour notebook (`draw_harbour`, `draw_all`) |
| [arrays_ortools.py](lecture2/arrays_ortools.py) | Arrays of variables and parameters: lists vs. dicts, set-valued arrays as Boolean matrices, channeling |
| [workers_ortools.py](lecture2/workers_ortools.py) | Assignment of robots to tasks: arrays, `all_different` and element constraints |
| [mip_ortools.py](lecture2/mip_ortools.py) | A small mixed-integer program with float, integer and Boolean variables |

**Try the notebooks in your browser, no installation needed:**

- Map colouring: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AImotion-Bavaria/kipro_wi/blob/main/lecture2/australia_ortools.ipynb)
- Harbour: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AImotion-Bavaria/kipro_wi/blob/main/lecture2/harbour_ortools.ipynb)

### [lecture3](lecture3/)

| File | What it shows |
|---|---|
| [send_more_money_ortools.py](lecture3/send_more_money_ortools.py) | The cryptarithmetic puzzle SEND + MORE = MONEY with explicit carries, listing all solutions |

## Running the examples locally

### MiniZinc models (`.mzn`)

Install the [MiniZinc IDE](https://www.minizinc.org/software.html), open the file and press *Run*.

### Python examples (`.py`, `.ipynb`)

Create a conda environment with Python 3.14 and the required packages:

```bash
conda create -n kipro -c conda-forge python=3.14 pip
conda activate kipro
pip install ortools cpmpy matplotlib ipykernel
```

Then run a script from its folder, for example:

```bash
cd lecture2
python australia_ortools.py
```

To use the notebooks, open them in VS Code or Jupyter and select the `kipro` environment as the kernel.

## From MiniZinc to OR-Tools

A few differences to keep in mind when translating models:

| MiniZinc | OR-Tools (CP-SAT) |
|---|---|
| `par int: n = 5;` | A plain Python constant: `n = 5` |
| `enum color = {blue, green, red};` | No enums: use integers `0..n-1` and a list of names |
| `var 1..10: x;` | `x = model.new_int_var(1, 10, "x")` |
| `var bool: b;` | `b = model.new_bool_var("b")` |
| `var int: x;` | Every variable needs finite bounds |
| `constraint x != y;` | `model.add(x != y)` |
| `solve satisfy;` | `solver = cp_model.CpSolver()` and `solver.solve(model)` |

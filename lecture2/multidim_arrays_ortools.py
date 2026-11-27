from ortools.sat.python import cp_model

# multidimensional arrays

# MiniZinc: set of int: Workers = 1..3;
#           set of int: Tasks = 1..3;
Workers = range(1, 4)
Tasks = range(1, 4)

# MiniZinc: array[Workers, Tasks] of 0..90: values;
#           values = [| 10, 20, 30 |
#                       40, 40, 40 |
#                       70, 60, 50 |];
# a list of rows -- note: Python indices start at 0 -> values[w - 1][t - 1]
values = [
    [10, 20, 30],
    [40, 40, 40],
    [70, 60, 50],
]

# ... or a dictionary with (worker, task) keys, to keep the MiniZinc indices
values_d = {(w, t): values[w - 1][t - 1] for w in Workers for t in Tasks}

# MiniZinc checks the element type 0..90 for us, Python does not
assert all(0 <= v <= 90 for v in values_d.values())

# MiniZinc: values[2, 3]
print("values[2, 3] =", values[1][2], "=", values_d[2, 3])


# a 2D array of decision variables works the same way
# MiniZinc: array[Workers, Tasks] of var 0..90: x;
model = cp_model.CpModel()
x = {(w, t): model.new_int_var(0, 90, f"x[{w},{t}]") for w in Workers for t in Tasks}

# MiniZinc: constraint forall(w in Workers, t in Tasks) (x[w, t] >= values[w, t]);
for w in Workers:
    for t in Tasks:
        model.add(x[w, t] >= values_d[w, t])

solver = cp_model.CpSolver()
solver.solve(model)
for w in Workers:
    print(" ".join(f"{solver.value(x[w, t]):3}" for t in Tasks))

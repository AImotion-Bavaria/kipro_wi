from ortools.sat.python import cp_model

# aggregation over arrays: sum, max, min

model = cp_model.CpModel()

# MiniZinc: array[1..5] of var 2..6: values;
Index = range(1, 6)
values = {i: model.new_int_var(2, 6, f"values[{i}]") for i in Index}

# fix the values from the slide: [3, 2, 4, 5, 3]
for i, v in zip(Index, [3, 2, 4, 5, 3]):
    model.add(values[i] == v)


# MiniZinc: sum(i in 1..5) (values[i])
# Python's sum() works directly: it builds a linear expression
total = sum(values[i] for i in Index)

# with an expression of i, e.g. sum(i in 1..5) (i * values[i])
weighted = sum(i * values[i] for i in Index)



# MiniZinc: max(i in 1..5) (values[i])
# Python's max() does NOT work on variables (NotImplementedError)
# -> a new variable plus a max-equality constraint: largest == max(values)
largest = model.new_int_var(2, 6, "largest")
model.add_max_equality(largest, [values[i] for i in Index])

# MiniZinc: min(i in 1..5) (values[i])
smallest = model.new_int_var(2, 6, "smallest")
model.add_min_equality(smallest, [values[i] for i in Index])


solver = cp_model.CpSolver()
solver.solve(model)

print("values   =", [solver.value(values[i]) for i in Index])
print("sum      =", solver.value(total))
print("weighted =", solver.value(weighted))
print("max      =", solver.value(largest))
print("min      =", solver.value(smallest))


# for parameters (plain Python data) the built-in functions work as usual:
fixed = [3, 2, 4, 5, 3]
print("parameters:", sum(fixed), max(fixed), min(fixed))

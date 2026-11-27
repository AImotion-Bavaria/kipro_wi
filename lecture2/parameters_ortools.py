from ortools.sat.python import cp_model

# parameters
# In OR-Tools, parameters are just ordinary Python constants:
# their values are fixed before the model is built, the solver never changes them.

# MiniZinc: par int: number_items;
#           number_items = 5;
# Python has no declaration without a value -> declare and assign in one step
number_items = 5

# MiniZinc: par 1..10: n_workers = 8;
# Python does not check the range for us -> check it explicitly
n_workers = 8
assert 1 <= n_workers <= 10, "n_workers must be in 1..10"

# MiniZinc: int: costs_per_unit = 2;
#           (the keyword "par" is optional in MiniZinc)
# MiniZinc: int: costs_per_unit;
#           costs_per_unit = 2;
# both variants are the same in Python:
costs_per_unit = 2


# --- using parameters in a model ---
model = cp_model.CpModel()

# parameters can be used as bounds of decision variables ...
items_produced = model.new_int_var(0, number_items, "items_produced")
workers_used = model.new_int_var(1, n_workers, "workers_used")
total_costs = model.new_int_var(0, costs_per_unit * number_items, "total_costs")

# ... and as coefficients in constraints
model.add(total_costs == costs_per_unit * items_produced)
model.add(items_produced >= workers_used)  # every worker produces at least one item

solver = cp_model.CpSolver()
status = solver.solve(model)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    for var in [items_produced, workers_used, total_costs]:
        print(f"{var.name} = {solver.value(var)};")
else:
    print("=====UNSATISFIABLE=====")

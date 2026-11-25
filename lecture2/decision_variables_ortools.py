from ortools.sat.python import cp_model

model = cp_model.CpModel()

# decision variables

# MiniZinc: var color: WA;
# CP-SAT has no enums -> encode the enum values as integers 0..n-1
colors = ["blue", "green", "red"]
WA = model.new_int_var(0, len(colors) - 1, "WA")

# MiniZinc: var 1..10: number_cars;
#           var 1..10: number_busses;
number_cars = model.new_int_var(1, 10, "number_cars")
number_busses = model.new_int_var(1, 10, "number_busses")

# MiniZinc: var 0..1: switch_on;
switch_on = model.new_int_var(0, 1, "switch_on")
# ... or, more idiomatic in CP-SAT, a Boolean variable:
# switch_on = model.new_bool_var("switch_on")

# MiniZinc: var int: total_costs;
# CP-SAT requires finite bounds for every integer variable
total_costs = model.new_int_var(cp_model.INT32_MIN, cp_model.INT32_MAX, "total_costs")


# --- just to show the variables get values ---
solver = cp_model.CpSolver()
status = solver.solve(model)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print(f"WA = {colors[solver.value(WA)]};")
    for var in [number_cars, number_busses, switch_on, total_costs]:
        print(f"{var.name} = {solver.value(var)};")
else:
    print("=====UNSATISFIABLE=====")

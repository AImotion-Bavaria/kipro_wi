from ortools.sat.python import cp_model

# models the ship assignment problem for harbour management
# ----------------------------------------------------------

Docks = range(1, 4)
model = cp_model.CpModel()

# variables

# boats 1 and 2 cannot use dock 1 -> smaller domain
boat1 = model.new_int_var(2, 3, "boat1")
boat2 = model.new_int_var(2, 3, "boat2")
boat3 = model.new_int_var(min(Docks), max(Docks), "boat3")
boat4 = model.new_int_var(min(Docks), max(Docks), "boat4")
boat5 = model.new_int_var(min(Docks), max(Docks), "boat5")

solver = cp_model.CpSolver()
status = solver.solve(model)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    for boat in [boat1, boat2, boat3, boat4, boat5]:
        print(f"{boat.name} = {solver.value(boat)};")
else:
    print("=====UNSATISFIABLE=====")

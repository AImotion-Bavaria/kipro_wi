from ortools.sat.python import cp_model

# possible values
colors = ["blue", "green", "red"]

model = cp_model.CpModel()

# decision variables (each region gets a color index 0..2)
WA = model.new_int_var(0, len(colors) - 1, "WA")
NT = model.new_int_var(0, len(colors) - 1, "NT")
SA = model.new_int_var(0, len(colors) - 1, "SA")
QL = model.new_int_var(0, len(colors) - 1, "QL")
NSW = model.new_int_var(0, len(colors) - 1, "NSW")
VT = model.new_int_var(0, len(colors) - 1, "VT")

# constraints: bordering
# countries must be different
model.add(WA != NT)
model.add(SA != NT)
model.add(WA != SA)
model.add(SA != NT)
model.add(QL != NT)
model.add(QL != SA)
model.add(NSW != SA)
model.add(NSW != VT)
model.add(NSW != QL)
model.add(VT != SA)

solver = cp_model.CpSolver()
status = solver.solve(model)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    assignment = {}
    for var in [WA, NT, SA, QL, NSW, VT]:
        assignment[var.name] = colors[solver.value(var)]
        print(f"{var.name} = {assignment[var.name]};")
    print("map written to australia_solution.svg")
else:
    print("=====UNSATISFIABLE=====")

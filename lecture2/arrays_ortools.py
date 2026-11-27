from ortools.sat.python import cp_model

model = cp_model.CpModel()

# arrays of decision variables or parameters

# MiniZinc: array[1..5] of var 2..6: values;
# a Python list of variables; note: Python lists start at index 0 -> values[0] .. values[4]
values = [model.new_int_var(2, 6, f"values[{i + 1}]") for i in range(5)]

# ... or a dictionary, if you want to keep the MiniZinc indices 1..5 -> values_d[1] .. values_d[5]
values_d = {i: model.new_int_var(2, 6, f"values_d[{i}]") for i in range(1, 6)}


# MiniZinc: set of int: Workers = 1..5;
#           set of int: Robots = 1..10;
Workers = range(1, 6)
Robots = range(1, 11)
is_operated_by_worker = {r: model.new_int_var(min(Workers), max(Workers), f"worker_of_robot_{r}")
                         for r in Robots}
operates_robots = {w: {r: model.new_bool_var(f"worker_{w}_operates_robot_{r}") for r in Robots}
                   for w in Workers}
# MiniZinc: array[Robots] of var Workers: is_operated_by_worker;
# index = robot, value = the worker (1..5) who operates it


# MiniZinc: array[Workers] of var set of Robots: operates_robots;
# no set variables in CP-SAT -> one Boolean per (worker, robot):
# operates_robots[w][r] is true <=> robot r is in the set of worker w


# MiniZinc: array[Workers] of par int: hourly_fee;
#           hourly_fee = [20, 25, 18, 30, 22];
# a parameter array is just Python data
hourly_fee = {1: 20, 2: 25, 3: 18, 4: 30, 5: 22}


# --- a few constraints that use the arrays ---

# both views describe the same assignment -> link them ("channeling"):
# robot r is in the set of worker w  <=>  is_operated_by_worker[r] == w
for w in Workers:
    for r in Robots:
        b = operates_robots[w][r]
        model.add(is_operated_by_worker[r] == w).only_enforce_if(b)
        model.add(is_operated_by_worker[r] != w).only_enforce_if(~b)

# card(operates_robots[w]) <= 3: nobody operates more than 3 robots
for w in Workers:
    model.add(sum(operates_robots[w].values()) <= 3)

# MiniZinc: values[1] = 3 (the example from the slide)
model.add(values[0] == 3)

# minimize the total fee: every robot costs the hourly fee of its worker
model.minimize(sum(hourly_fee[w] * operates_robots[w][r] for w in Workers for r in Robots))


# --- solve and print ---
solver = cp_model.CpSolver()
status = solver.solve(model)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print("values =", [solver.value(v) for v in values])
    print("is_operated_by_worker =", {r: solver.value(is_operated_by_worker[r]) for r in Robots})
    print("operates_robots =",
          {w: sorted(r for r in Robots if solver.value(operates_robots[w][r])) for w in Workers})
    print(f"total fee = {solver.objective_value:.0f}")
else:
    print("=====UNSATISFIABLE=====")

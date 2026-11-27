from ortools.sat.python import cp_model

# Assignment problem: every robot gets a different task, maximize the total profit.
# OR-Tools version of workers.mzn

# MiniZinc: int: n = 3;
#           int: m = 3;
n = 3
m = 3

# MiniZinc: set of int: Robots = 1..n;
#           set of int: Tasks = 1..m;
# Python indices start at 0 -> Robots = 0..n-1, Tasks = 0..m-1
Robots = range(n)
Tasks = range(m)

# MiniZinc: array[Robots,Tasks] of int: profits = [| 20, 5, 8 | 15, 20, 15 | 10, 30, 7 |];
# a list of rows: profits[r][t]
profits = [
    [20, 5, 8],
    [15, 20, 15],
    [10, 30, 7],
]

model = cp_model.CpModel()

# decision variables
# MiniZinc: array[Robots] of var Tasks: assign;
assign = [model.new_int_var(0, m - 1, f"assign_{r + 1}") for r in Robots]

# constraints
# MiniZinc: constraint alldifferent(assign);
model.add_all_different(assign)

# objective
# MiniZinc: solve maximize sum(r in Robots) (profits[r, assign[r]]);
# CP-SAT cannot index a list with a variable directly (profits[r][assign[r]]),
# so we use an element constraint: profit[r] == profits[r][assign[r]]
profit = [model.new_int_var(min(profits[r]), max(profits[r]), f"profit_{r + 1}")
          for r in Robots]
for r in Robots:
    model.add_element(assign[r], profits[r], profit[r])

model.maximize(sum(profit))

solver = cp_model.CpSolver()
status = solver.solve(model)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    for r in Robots:
        t = solver.value(assign[r])
        # +1 to print robots and tasks numbered from 1 as in MiniZinc
        print(f"robot {r + 1} -> task {t + 1} (profit {profits[r][t]})")
    print(f"total profit = {solver.objective_value:.0f}")
else:
    print("=====UNSATISFIABLE=====")

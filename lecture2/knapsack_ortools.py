from ortools.sat.python import cp_model

# 0/1 knapsack: choose items with maximal total value without exceeding the capacity

# MiniZinc: set of int: ITEMS = 1..3;
ITEMS = range(1, 4)

# example data
# MiniZinc: array[ITEMS] of int: w;   (weights)
#           int: capacity;
#           array[ITEMS] of int: v;   (values)
w = {1: 4, 2: 3, 3: 2}
v = {1: 10, 2: 7, 3: 5}
capacity = 5

model = cp_model.CpModel()

# MiniZinc: array[ITEMS] of var 0..1: x;
# x[i] = 1 <=> item i is packed  (model.new_bool_var would work as well)
x = {i: model.new_int_var(0, 1, f"x[{i}]") for i in ITEMS}

# MiniZinc: constraint sum(i in ITEMS) (x[i] * w[i]) <= capacity;
model.add(sum(x[i] * w[i] for i in ITEMS) <= capacity)

# MiniZinc: var int: f = sum(i in ITEMS) (x[i] * v[i]);
# here f is simply a linear expression, no extra variable needed
f = sum(x[i] * v[i] for i in ITEMS)

# MiniZinc: solve maximize f;
model.maximize(f)

solver = cp_model.CpSolver()
status = solver.solve(model)

if status == cp_model.OPTIMAL:
    packed = [i for i in ITEMS if solver.value(x[i])]
    print("x =", [solver.value(x[i]) for i in ITEMS])
    print("packed items:", packed)
    print("weight =", sum(w[i] for i in packed), "of", capacity)
    print("f =", solver.value(f))
else:
    print("no optimal solution found")

from ortools.sat.python import cp_model

# Boolean conditions in CP-SAT
# Each example builds its own small model, solves it and prints the solution.


def solve_and_print(title, model, variables):
    solver = cp_model.CpSolver()
    status = solver.solve(model)
    print(f"--- {title} ---")
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("  ".join(f"{v.name} = {solver.value(v)}" for v in variables))
    else:
        print("=====UNSATISFIABLE=====")


# 1) AND
# MiniZinc: constraint x + y > 10 /\ y < 20;
# every constraint in a model must hold anyway -> just add both
model = cp_model.CpModel()
x = model.new_int_var(0, 30, "x")
y = model.new_int_var(0, 30, "y")
model.add(x + y > 10)
model.add(y < 20)
# NOT: model.add((x + y > 10) and (y < 20))  -> NotImplementedError
solve_and_print("and", model, [x, y])


# 2) OR
# MiniZinc: constraint x >= 25 \/ y >= 25;
# introduce one Boolean per condition, then require at least one of them
model = cp_model.CpModel()
x = model.new_int_var(0, 30, "x")
y = model.new_int_var(0, 30, "y")
b1 = model.new_bool_var("b1")  # b1 -> x >= 25
b2 = model.new_bool_var("b2")  # b2 -> y >= 25
model.add(x >= 25).only_enforce_if(b1)
model.add(y >= 25).only_enforce_if(b2)
model.add_bool_or([b1, b2])
model.add_bool_and
model.add(x + y <= 30)
solve_and_print("or", model, [x, y, b1, b2])


# 3) NOT
# MiniZinc: constraint not (x = y);
# a negated comparison is just the opposite comparison
model = cp_model.CpModel()
x = model.new_int_var(0, 3, "x")
y = model.new_int_var(0, 3, "y")
model.add(x != y)
# for Boolean variables: ~b is "not b"
b = model.new_bool_var("b")
model.add_bool_or([~b])  # forces b = false
solve_and_print("not", model, [x, y, b])


# 4) IMPLICATION
# MiniZinc: constraint x > 20 -> y = 0;
# b must be *equivalent* to x > 20, otherwise the solver could set b = false
# and ignore the implication -> enforce both directions
model = cp_model.CpModel()
x = model.new_int_var(0, 30, "x")
y = model.new_int_var(0, 30, "y")
x_big = model.new_bool_var("x_big")         # x_big <-> x > 20
model.add(x > 20).only_enforce_if(x_big)
model.add(x <= 20).only_enforce_if(~x_big)
model.add(y == 0).only_enforce_if(x_big)    # x_big -> y = 0
model.add(x == 25)
solve_and_print("implication", model, [x, y, x_big])

# implication between two Booleans: add_implication(a, b) means a -> b
# MiniZinc: constraint a -> b;
model = cp_model.CpModel()
a = model.new_bool_var("a")
b = model.new_bool_var("b")
model.add_implication(a, b)
model.add(a == 1)
solve_and_print("implication (Booleans)", model, [a, b])


# 5) EQUIVALENCE / REIFICATION and COUNTING
# MiniZinc: constraint sum([x > 10, y > 10, x + y < 15]) >= 2;
# reify every condition into a Boolean (both directions!) and sum them up
model = cp_model.CpModel()
x = model.new_int_var(0, 30, "x")
y = model.new_int_var(0, 30, "y")
c1 = model.new_bool_var("c1")  # c1 <-> x > 10
c2 = model.new_bool_var("c2")  # c2 <-> y > 10
c3 = model.new_bool_var("c3")  # c3 <-> x + y < 15
model.add(x > 10).only_enforce_if(c1)
model.add(x <= 10).only_enforce_if(~c1)
model.add(y > 10).only_enforce_if(c2)
model.add(y <= 10).only_enforce_if(~c2)
model.add(x + y < 15).only_enforce_if(c3)
model.add(x + y >= 15).only_enforce_if(~c3)
model.add(c1 + c2 + c3 >= 2)
model.add(x + y >= 15)  # makes c3 false -> c1 and c2 must both hold
solve_and_print("counting", model, [x, y, c1, c2, c3])


# 6) XOR (exactly one of)
# MiniZinc: constraint a xor b;
model = cp_model.CpModel()
a = model.new_bool_var("a")
b = model.new_bool_var("b")
model.add_bool_xor([a, b])          # odd number of true literals
# for "exactly one" of a longer list: model.add_exactly_one([...])
solve_and_print("xor", model, [a, b])

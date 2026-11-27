from ortools.sat.python import cp_model

# constraints = Boolean expressions that need to hold
# MiniZinc: constraint <Boolean_Expression>;
# OR-Tools: model.add(<Boolean_Expression>)


def solve_and_print(title, model, variables):
    solver = cp_model.CpSolver()
    status = solver.solve(model)
    print(f"--- {title} ---")
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("  ".join(f"{v.name} = {solver.value(v)}" for v in variables))
    else:
        print("=====UNSATISFIABLE=====")


# --- comparisons ---
model = cp_model.CpModel()
num_workers = model.new_int_var(0, 100, "num_workers")
number_users = model.new_int_var(0, 100, "number_users")
in_flows = model.new_int_var(0, 100, "in_flows")
out_flows = model.new_int_var(0, 100, "out_flows")
y = model.new_int_var(0, 10, "y")
z = model.new_int_var(0, 10, "z")

model.add(num_workers < 16)          # MiniZinc: constraint num_workers < 16;       (less than)
model.add(number_users > 5)          # MiniZinc: constraint number_users > 5;       (greater than)
model.add(in_flows == out_flows)     # MiniZinc: constraint in_flows == out_flows;  (equals)
model.add(y != z)                    # MiniZinc: constraint y != z;                 (is not equal)
solve_and_print("comparisons", model,
                [num_workers, number_users, in_flows, out_flows, y, z])


# --- logical AND ---
# MiniZinc: constraint age < 16 /\ height < 150;
model = cp_model.CpModel()
age = model.new_int_var(0, 120, "age")
height = model.new_int_var(0, 250, "height")

# variant 1: all constraints of a model must hold anyway -> two separate constraints
#   model.add(age < 16)
#   model.add(height < 150)

# variant 2: with add_bool_and -- it only accepts Boolean variables, not constraints
# (model.add_bool_and([model.add(...), ...]) raises "Invalid boolean literal")
b1 = model.new_bool_var("b1")  # b1 -> age < 16
b2 = model.new_bool_var("b2")  # b2 -> height < 150
model.add(age < 16).only_enforce_if(b1)
model.add(height < 150).only_enforce_if(b2)
model.add_bool_and([b1, b2])

solve_and_print("AND", model, [age, height])


# --- logical OR ---
# MiniZinc: constraint x in 1..5 \/ x in 10..15;
# variant 1: "x in a set of values" is a domain constraint
model = cp_model.CpModel()
x = model.new_int_var(0, 20, "x")
model.add_linear_expression_in_domain(x, cp_model.Domain.from_intervals([[1, 5], [10, 15]]))
model.add(x > 7)  # just to see that the solver jumps to the second interval
solve_and_print("OR (domain)", model, [x])

# variant 2: the general way for any OR -- one Boolean per alternative
model = cp_model.CpModel()
x = model.new_int_var(0, 20, "x")
b1 = model.new_bool_var("b1")  # b1 -> x in 1..5
b2 = model.new_bool_var("b2")  # b2 -> x in 10..15
model.add(x >= 1).only_enforce_if(b1)
model.add(x <= 5).only_enforce_if(b1)
model.add(x >= 10).only_enforce_if(b2)
model.add(x <= 15).only_enforce_if(b2)
model.add_bool_or([b1, b2])
model.add(x > 7)
solve_and_print("OR (Booleans)", model, [x, b1, b2])


# --- logical NOT ---
# MiniZinc: constraint not (age < 16 /\ height < 150);
# De Morgan: not (A /\ B)  ==  (not A) \/ (not B)  ==  age >= 16 \/ height >= 150
model = cp_model.CpModel()
age = model.new_int_var(0, 120, "age")
height = model.new_int_var(0, 250, "height")
old = model.new_bool_var("old")    # old -> age >= 16
tall = model.new_bool_var("tall")  # tall -> height >= 150
model.add(age >= 16).only_enforce_if(old)
model.add(height >= 150).only_enforce_if(tall)
model.add_bool_or([old, tall])
model.add(age == 10)  # a child -> must be tall
solve_and_print("NOT", model, [age, height, old, tall])

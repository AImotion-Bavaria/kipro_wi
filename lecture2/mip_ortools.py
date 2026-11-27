from ortools.math_opt.python import mathopt

# A small mixed-integer program (MIP) with float, integer and Boolean variables,
# written with MathOpt, the current OR-Tools interface for LP/MIP solvers.
#
# A workshop builds tables and chairs and buys wood for them.
# It may rent an extra machine that gives more working hours.
# Maximize the profit.

# parameters
profit_table = 120.0         # EUR per table
profit_chair = 45.0          # EUR per chair
wood_table = 1.8             # m^2 of wood per table
wood_chair = 0.6             # m^2 of wood per chair
wood_price = 12.5            # EUR per m^2
max_wood = 30.0              # m^2 the supplier can deliver
hours_table = 3.5
hours_chair = 1.2
hours_available = 40.0
machine_rent = 80.0          # EUR, fixed cost if the machine is rented
machine_hours = 15.0         # extra hours with the machine

model = mathopt.Model(name="workshop")

# decision variables
# MiniZinc: var 0..100: tables;   (integer)
tables = model.add_integer_variable(lb=0, ub=100, name="tables")
chairs = model.add_integer_variable(lb=0, ub=100, name="chairs")
# MiniZinc: var 0.0..max_wood: wood;   (float -- not possible in CP-SAT!)
wood = model.add_variable(lb=0.0, ub=max_wood, name="wood")
# MiniZinc: var bool: rent_machine;   (a 0/1 integer variable)
rent_machine = model.add_binary_variable(name="rent_machine")

# constraints (all linear, float coefficients are fine)
# we cannot use more wood than we buy
model.add_linear_constraint(wood_table * tables + wood_chair * chairs <= wood)
# working hours; the Boolean adds hours only if the machine is rented
model.add_linear_constraint(hours_table * tables + hours_chair * chairs
                            <= hours_available + machine_hours * rent_machine)
# at least as many chairs as tables
model.add_linear_constraint(chairs >= tables)

# objective
model.maximize(profit_table * tables + profit_chair * chairs
               - wood_price * wood
               - machine_rent * rent_machine)

# the solver is chosen when solving; alternatives: GSCIP (SCIP), CP_SAT,
# GLOP (LP: continuous variables only)
result = mathopt.solve(model, mathopt.SolverType.HIGHS)

if result.termination.reason == mathopt.TerminationReason.OPTIMAL:
    print(f"profit = {result.objective_value():.2f} EUR")
    print(f"tables = {result.variable_values(tables):.0f}")
    print(f"chairs = {result.variable_values(chairs):.0f}")
    print(f"wood = {result.variable_values(wood):.2f} m^2")
    print(f"rent_machine = {result.variable_values(rent_machine):.0f}")
else:
    print("no optimal solution found:", result.termination.reason)

from ortools.sat.python import cp_model

# Cryptarithmetic puzzle:
#
#       S E N D
#   +   M O R E
#   -----------
#   = M O N E Y
#
# Every letter stands for a different digit, numbers have no leading zeros.

# MiniZinc: enum Letters = {s, e, n, d, m, o, r, y};
# no enums in Python -> a list of names
Letters = ["s", "e", "n", "d", "m", "o", "r", "y"]

model = cp_model.CpModel()

# MiniZinc: set of int: Digits = 0..9;
#           array[Letters] of var Digits: value;
# a dictionary letter -> variable, so we can write value["s"] like value[s]
value = {l: model.new_int_var(0, 9, l) for l in Letters}
s, e, n, d, m, o, r, y = (value[l] for l in Letters)  # short names for the equations

# MiniZinc: array[1..4] of var 0..1: carry;
# carry[i] is the carry out of column i (counted from the right: C1 .. C4)
carry = {i: model.new_int_var(0, 1, f"C{i}") for i in range(1, 5)}

# MiniZinc: constraint value[s] != 0 /\ value[m] != 0;
model.add(s != 0)
model.add(m != 0)

# MiniZinc: constraint alldifferent(value);
model.add_all_different(value.values())

# column by column, from right to left:
# the digits plus the incoming carry give the result digit plus 10 * outgoing carry
model.add(d + e == y + 10 * carry[1])                 # column 1:      D + E = Y
model.add(n + r + carry[1] == e + 10 * carry[2])      # column 2:      N + R = E
model.add(e + o + carry[2] == n + 10 * carry[3])      # column 3:      E + O = N
model.add(s + m + carry[3] == o + 10 * carry[4])      # column 4:      S + M = O
model.add(m == carry[4])                              # column 5: the last carry is M


# --- solve and print all solutions ---
class PrintSolutions(cp_model.CpSolverSolutionCallback):
    def __init__(self):
        super().__init__()
        self.count = 0

    def on_solution_callback(self):
        self.count += 1
        v = {l: self.value(value[l]) for l in Letters}
        print(f"Solution {self.count}: " + ", ".join(f"{l.upper()}={v[l]}" for l in Letters))
        print(f"    {v['s']}{v['e']}{v['n']}{v['d']}")
        print(f"  + {v['m']}{v['o']}{v['r']}{v['e']}")
        print(f"  = {v['m']}{v['o']}{v['n']}{v['e']}{v['y']}")


solver = cp_model.CpSolver()
solver.parameters.enumerate_all_solutions = True
printer = PrintSolutions()
solver.solve(model, printer)
print(f"{printer.count} solution(s) found")

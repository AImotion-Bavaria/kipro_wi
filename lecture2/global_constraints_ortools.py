from ortools.sat.python import cp_model

# "special" constraints: global constraints

model = cp_model.CpModel()

Workers = range(1, 5)   # 4 workers
Tasks = range(1, 5)     # 4 tasks

# shifts as an "enum": no enums in CP-SAT -> integer codes
MORNING, DAY, NIGHT = 0, 1, 2
shift_names = ["morning", "day", "night"]


# MiniZinc: constraint alldifferent(workers_work_on_task);
# every worker gets a different task
workers_work_on_task = {w: model.new_int_var(min(Tasks), max(Tasks), f"task_of_{w}")
                        for w in Workers}
model.add_all_different(workers_work_on_task.values())


# MiniZinc: constraint at_most(2, works_shift, night);
# at most 2 workers work the night shift
# no direct at_most for values in CP-SAT -> one Boolean per worker "works at night", then count
works_shift = {w: model.new_int_var(MORNING, NIGHT, f"shift_of_{w}") for w in Workers}
is_night = {w: model.new_bool_var(f"{w}_is_night") for w in Workers}
for w in Workers:
    model.add(works_shift[w] == NIGHT).only_enforce_if(is_night[w])
    model.add(works_shift[w] != NIGHT).only_enforce_if(~is_night[w])
model.add(sum(is_night.values()) <= 2)


# MiniZinc: constraint increasing(work_load);
# the work load does not decrease from worker to worker
work_load = {w: model.new_int_var(0, 40, f"work_load_{w}") for w in Workers}
for w in Workers:
    if w + 1 in Workers:
        model.add(work_load[w] <= work_load[w + 1])


# just to get an interesting solution: everybody prefers the night shift (bonus)
# and as much work as possible for the first worker
model.maximize(sum(is_night.values()) * 100 + work_load[1])

solver = cp_model.CpSolver()
status = solver.solve(model)

if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print("worker  task  shift    work_load")
    for w in Workers:
        print(f"{w:6}  {solver.value(workers_work_on_task[w]):4}  "
              f"{shift_names[solver.value(works_shift[w])]:7}  {solver.value(work_load[w]):9}")
else:
    print("=====UNSATISFIABLE=====")

# Configuration Files Directory (`results`)

This directory contains the results of the optimization process, either resulting from `solve_problem.py` or from `join_and_local_search`.

---
The files follow the naming convention
```
vars_{script}_{test_name}.txt
```
`{script}`  identifies the source script,
`localsearch` if created by `join_local_search.py` and
`problem` if created by `solve_problem.py`. `identifier` identifies the run of
the test.
These files contain and contain the solution found of the optimized land use for each cell
in the problem. The format for each row is
```
{cell id} {land use}.
```

**Example**:
```
2721492 FDR_N
2723791 FDR_N
1345806 ODR_N
1345807 ODR_N
```
# Parkview Data

## Structure
### Git Data
- in the directory `git_data`
- contains a file called `branches` with the following format:
```
[
  "branch1",
  "branch2",
  "branch3",
  ...
]
```
- each branch has a file with the same name as the branch, for example the *develop*-branch has a file called `develop` containing the commits in the format
```
[
    {
        "sha": "<commit sha>",
        "author": "<author name>",
        "date": "<commit date>",
        "message": "<commit message>"
    },
    {
        "sha": "<other commit sha>",
        "author": "<other author name>",
        "date": "<other commit date>",
        "message": "<other commit message>"
    },
    ...
]
```

### Benchmark Data
- benchmark data is stored under `benchmark_data`
- a benchmark for a specific **commit** on a specific **device** is stored `<commit sha>/<benchmark type>/<device name>` with `<benchmark type>` being being one of `[spmv, solver, conversion, preconditioner, blas]`
- the `index` file keeps track of all benchark results, its format is as follows:
```
{
      "<commit sha>": {
          spmv: [<available devices>],
          blas: [<available devices>],
          solver: [<available devices>],
          preconditioner: [<available devices>],
          conversion: [<available devices>],
      },
      ...
}
```
- `<available devices>` is a list of strings containing the name of the device


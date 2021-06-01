# rocket-cores 

Rocket cores is a simple tool to fetch most reused first stage cores and calculate total carried mass to the orbit for each core.
It leverages spaceX graphQL Api: https://api.spacex.land/graphql/

## Installation & Usage:

Installation via pip:
`rocket-cores` uses poetry as a build tool. To use rocket-core, simply type (inside rocket-cores dir):
``` console
poetry install
poetry build
```

To run `rocket-cores`, just type:
``` console
poetry run rocket-cores
```
Command will fetch the api asynchronously for 5 most reused cores.
You can change number of cores via `--cores` flag:
``` console
poetry run rocket-cores --cores 10
```
Will produce:
``` console
The most reused rocket cores:

_____________________________________
|core id|reuse count|mass total [kg]|
|-------+-----------+---------------|
| B1049 |     6     |     91880     |
| B1051 |     5     |     75274     |
| B1048 |     4     |     49245     |
| B1046 |     3     |     13550     |
| B1059 |     3     |     23977     |
| B1056 |     3     |     26910     |
| B1047 |     2     |     16576     |
| B1060 |     2     |     34680     |
| B1058 |     2     |     24925     |
| B1032 |     1     |     4230      |
=====================================
```
For further guidance, type:
``` console
poetry run rocket-cores --help
```

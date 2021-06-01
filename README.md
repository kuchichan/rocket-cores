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

For further guidance, type:
``` console
poetry run rocket-cores --help
```

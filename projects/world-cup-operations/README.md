# World Cup Operations Scenarios

## Decision questions

This team coursework explores several tournament operations questions using explicit scenario assumptions: how to form balanced groups, model qualifier outcomes, assess sensitivity to spectator-interest assumptions, and assign matches to stadiums. These are analytical exercises, not official tournament forecasts.

## Code map

- `python/world_cup_group_formation.py` — mixed-integer group formation and constraint exploration.
- `python/world_cup_qualifier_monte_carlo.py` — Monte Carlo simulation of qualification paths.
- `python/world_cup_sensitivity_analysis.py` — sensitivity modelling for match-interest scenarios.
- `python/world_cup_stadium_assignment.py` — stadium allocation under capacity and schedule constraints.

## Inputs and scope

The qualifier script contains a dated ranking snapshot and assumptions in code. The optimisation scripts expect the course workbook described in [`../../data/README.md`](../../data/README.md), which is not included. Outputs are not presented as verified real-world results.

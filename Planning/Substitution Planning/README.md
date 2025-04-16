# Basketball Game Planning Scenarios (PDDL)

This folder contains a collection of PDDL domain and problem files that simulate various basketball game situations. The planner used for this simulation is **OPTIC**, available at:  
 https://editor.planning.domains/#

All output discussed in the project was generated using this online OPTIC planner.

---

## Domain File

- **`game_simulation_domain.pddl`**  
  Contains the core domain model for basketball simulation.  
  Includes stamina tracking, fatigue rates, substitutions, and a momentum metric.

---

## Problem Files

Each problem file defines a unique game scenario using the same domain. The goal in all cases is to reduce `time-left` to 0 while maximizing overall `momentum`.

- **`game_situation_problem.pddl`**  
  Standard game with all players active and moderate stamina levels.

- **`game_situation_problem2.pddl`**  
  Alternate lineup and varied player stamina values to demonstrate planner flexibility.

- **`injured_player_problem.pddl`**  
  Simulates a scenario where one player (Curry) is unavailable for the entire game and is not entered into the game. (`max-stamina = 0`).

- **`fast_paced_game_problem.pddl`**  
  Shorter game with increased fatigue rates for all players, leading to frequent substitutions.

- **`back2back_game_problem.pddl`**  
  All players start with full stamina, but their `max-stamina` is reduced to simulate a game played on short rest.

- **`late_game_problem.pddl`**  
  Simulates an end-of-game scenario with low stamina and only a few usable players. Several players cannot be reused (`max-stamina = 0`).

---

## How to Run the Files

To test or explore the scenarios:

1. Go to [https://editor.planning.domains/#](https://editor.planning.domains/#)
2. Upload `game_simulation_domain.pddl` as the **domain file**
3. Upload any `.pddl` file listed above as the **problem file**
4. Click **"Solve"** to run the scenario
5. OPTIC will return the full planned action sequence as output

---

## Notes

- Each scenario is designed to highlight different planning behaviors (e.g., endurance management, injury constraints, lineup flexibility)
- Momentum is always the optimization metric (`:metric maximize (momentum)`)
- Players are only substituted in when the on-court player’s stamina is depleted

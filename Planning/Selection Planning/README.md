This project uses PDDL and the OPTIC solver to simulate building optimal basketball lineups based on different player attributes. Each problem file asks the solver to select a 5-player lineup (PG, SG, SF, PF, C) to maximize a specific overall team stat.

All files are compatible with the OPTIC planner.

How to run:
    1. Go to https://editor.planning.domains/#
    2. Upload selection_domain as the domain file
    3. choose any of the *_selection.pddl files as the problem file
    4. From the dropdown select OPTIC as the solver.
    5. Click "solve". The planner will return some messy output, the set of actions at the bottom is its solution.

File Name | Description
selection_domain.pddl | The domain file with actions for assigning players based on each attribute (composite, shooting, defense, playmaking, offense). OPTIC-compatible.
composite_selection.pddl | Problem file to select the lineup with the highest total composite score (offense + defense + playmaking).
shooting_selection.pddl | Problem file to maximize total shooting in the lineup.
defense_selection.pddl | Problem file to maximize total defense in the lineup.
playmaking_selection.pddl | Problem file to maximize total playmaking in the lineup.
offense_selection.pddl | Problem file to maximize total offense in the lineup.
README.md | This file. Describes the files and how to run them.

Notes:
    each action in the domain adds only to the specific total being optimized
    the problem file includes 10 players, each with attributes and eligible positions
    the planner will assign one player per position, maximizing the target attribute
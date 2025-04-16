🏀 AI Basketball Lineup Optimization – CISC 352 Project
This project is a comprehensive exploration of AI techniques applied to basketball decision-making. It was developed for the CISC 352: Artificial Intelligence course at Queen's University and showcases three core AI methodologies:

Constraint Satisfaction Problems (CSP)

Planning (PDDL)

Deep Learning (PyTorch)

All techniques revolve around the central problem of basketball lineup formation, simulation, and evaluation.

📁 Project Structure

Folder	Description
Planning	Uses PDDL to simulate lineup substitutions and in-game stamina management, as well as selecting optimal 5-man lineups.
CSP	Uses Google OR-Tools to generate feasible 5-man lineups based on statistical constraints and sort them by key metrics.
Deep_Learning	Trains a neural network to predict lineup performance (net impact per 36 minutes), then ranks and compares lineups.
🧠 Techniques Overview
🧩 Constraint Satisfaction (CSP)
Selects the top 5 players from each team using stat-based constraints.

Ensures lineups have minimum rebounding, defense, shooting, and playmaking presence.

Outputs top 5 lineups per team by Points, Rebounds, Assists, and Defense.

📋 Planning (PDDL)
Models in-game substitutions with stamina constraints and momentum mechanics.

Simulates a 3-on-3 basketball game with sub rules and time decay.

Also includes lineup selection planning using position and attribute constraints to optimize different team qualities.

🤖 Deep Learning
Trains a neural network to predict impact per 36 minutes from historical play-by-play data.

Adjusts predictions based on minutes played.

Identifies best/worst starting lineups and highlights high-performing bench lineups.

🔧 How to Run
🧩 CSP
Navigate to CSP/

Run one of:

bash
Copy
Edit
python CSP_one_team.py
python CSP_all_teams.py
View results in lineup_results.txt.

📋 Planning
Visit https://editor.planning.domains/#

Use the OPTIC planner.

Load a .pddl domain file and one of the problem files (e.g., game_situation_problem.pddl, composite_selection.pddl).

Click Plan to generate results.

🤖 Deep Learning
Install dependencies:

bash
Copy
Edit
pip install torch pandas
Navigate to Deep_Learning/

Run:

bash
Copy
Edit
python DL_prediction.py
Outputs are saved to lineup_predictions.txt.

📚 Data Sources
Kaggle Dataset (for Deep Learning)
NBA Play-by-Play Dataset:
https://www.kaggle.com/datasets/xocelyk/nba-pbp

📝 Notes
.csv files over 2GB are excluded from the repo and provided as .zip archives.

The Planning component was tested using the OPTIC planner only, due to other planners not supporting numeric fluents or ADL.

Lineup selection and simulation were constrained to smaller rosters due to solver limitations and complexity.

🙌 Credits
Developed by Avery McLean for CISC 352 (Winter 2024), Queen's University
Instructor: Prof. Christian Muise
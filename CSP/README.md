# CSP – NBA Lineup Generation with Constraint Satisfaction

This directory contains all files related to the Constraint Satisfaction Problem (CSP) portion of the CISC 352 AI project. The goal of this module is to generate valid and effective NBA lineups using real player statistics from the 2021–22 season, based on a set of basketball-relevant constraints.

## 🧠 Overview

Using OR-Tools and constraint programming, we define a series of rules (constraints) that determine what makes a "valid" lineup. These include position requirements, shooting ability, rebounding, playmaking, and defense. For each team:

- A set of eligible players is selected (based on scoring and games played).
- All 5-player combinations are tested for feasibility using CSP.
- Valid lineups are ranked and displayed based on team-level stats like points, assists, rebounds, and defense.

## 📁 File Descriptions

| File | Description |
|------|-------------|
| `CSP_one_team.py` | Allows the user to select a team by abbreviation and generates valid lineups only for that team. It prints top 5 lineups for several metrics. |
| `CSP_all_teams.py` | Generates valid lineups for **all NBA teams**. Outputs top lineups for each and summarizes team lineup depth in `lineup_results.txt`. |
| `2021-2022 NBA Player Stats - Regular.csv` | Raw player stats from the 2021–22 NBA season, including points, assists, rebounds, shooting percentages, etc. |
| `2021-2022 NBA Player Stats - Regular.zip` | Compressed version of the CSV file to help manage GitHub size constraints. |
| `lineup_results.txt` | Output from `CSP_all_teams.py`, listing best lineups for each team across different metrics, along with summary statistics. |

## 🔍 Constraints Modeled

Each valid lineup must satisfy:
- Exactly **5 players**.
- At least **2 wing players** (SG, SF, PF).
- At least **2 competent shooters** (based on 3P%).
- At least **2 rebounders** (based on per-36 rebounding).
- At least **2 playmakers** (based on per-36 assists).
- At least **3 defenders** (based on per-36 steals + blocks).

These rules ensure lineups reflect realistic team-building considerations.

## 🚀 How to Run

To run the one-team version:

```bash
python CSP_one_team.py

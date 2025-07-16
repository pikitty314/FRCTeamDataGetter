import statbotics
import pandas

# Constants
YEAR = 2025
EVENT_CODE = "2025micmp4"
MATCH_CODE = "qm3"

### PULL DATA FROM STATBOTICS ###
sb = statbotics.Statbotics() # Get Statbotics

matchdata = sb.get_match(EVENT_CODE + "_" + MATCH_CODE) # Get match data

redAlliance = matchdata["alliances"]["red"]["team_keys"]
blueAlliance = matchdata["alliances"]["blue"]["team_keys"]
allTeams = redAlliance + blueAlliance

teamData = dict()

for team in allTeams:
    sbdata = sb.get_team_year(int(team), YEAR) # Get team data

    teamData[str(team)] = {} # Initialize team in dict

    teamData[str(team)]["total_epa"] = float(sbdata["epa"]["breakdown"]["total_points"]) # Total EPA
    teamData[str(team)]["auto_epa"] = float(sbdata["epa"]["breakdown"]["auto_points"]) # Auto EPA
    teamData[str(team)]["teleop_epa"] = float(sbdata["epa"]["breakdown"]["teleop_points"]) # Teleop EPA
    teamData[str(team)]["endgame_epa"] = float(sbdata["epa"]["breakdown"]["endgame_points"]) # Endgame EPA


### PULL DATA FROM PRE SCOUTING ###
preScouting = pandas.read_csv("preScoutingData.csv")

indexCounter = 0
for team in preScouting["Team #"]:
    for target in allTeams:
        if (int(team) == int(target)):
            teamData[str(team)]["auto_rating"] = float(preScouting["Auton"].loc[preScouting.index[indexCounter]])
            teamData[str(team)]["coral_intake_rating"] = float(preScouting["Coral Intake"].loc[preScouting.index[indexCounter]])
            teamData[str(team)]["coral_scoring_rating"] = float(preScouting["Coral Scoring on L4/3/2"].loc[preScouting.index[indexCounter]])
            teamData[str(team)]["coral_L1_rating"] = float(preScouting["Coral Scoring  on L1"].loc[preScouting.index[indexCounter]])
            teamData[str(team)]["algae_rating"] = float(preScouting["Algae Intake & Scoring"].loc[preScouting.index[indexCounter]])
            teamData[str(team)]["endgame_rating"] = float(preScouting["Endgame"].loc[preScouting.index[indexCounter]])
            teamData[str(team)]["defense_rating"] = float(preScouting["Defense (N/A if not observed)"].loc[preScouting.index[indexCounter]])
    else:
        indexCounter += 1


### PULL DATA FROM PIT SCOUTING ###

dataframe = pandas.DataFrame(teamData)
print(dataframe)
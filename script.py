import statbotics
import pandas

# Constants
YEAR = 2025
EVENT_CODE = "2025micmp4"
MATCH_CODE = "qm3"

sb = statbotics.Statbotics() # Get Statbotics

matchdata = sb.get_match(EVENT_CODE + "_" + MATCH_CODE) # Get match data

redAlliance = matchdata["alliances"]["red"]["team_keys"]
blueAlliance = matchdata["alliances"]["blue"]["team_keys"]
allTeams = redAlliance + blueAlliance

teamData = dict()

for team in allTeams:
    sbdata = sb.get_team_year(int(team), YEAR) # Get team data

    teamData[str(team)] = {}

    teamData[str(team)]["total_epa"] = float(sbdata["epa"]["breakdown"]["total_points"]) # Total EPA
    teamData[str(team)]["auto_epa"] = float(sbdata["epa"]["breakdown"]["auto_points"]) # Auto EPA
    teamData[str(team)]["teleop_epa"] = float(sbdata["epa"]["breakdown"]["teleop_points"]) # Teleop EPA
    teamData[str(team)]["endgame_epa"] = float(sbdata["epa"]["breakdown"]["endgame_points"]) # Endgame EPA

    #print(str(team) + ": " + str(teamData[str(team)]["total_epa"]))
else:
    dataframe = pandas.DataFrame(teamData)
    print(dataframe)
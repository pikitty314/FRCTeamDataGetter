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

teamEPAs = dict()

for team in allTeams:
    teamdata = sb.get_team_year(int(team), YEAR) # Get team data

    teamEPAs[str(team)] = {}

    teamEPAs[str(team)]["total_epa"] = float(teamdata["epa"]["breakdown"]["total_points"]) # Total EPA
    teamEPAs[str(team)]["auto_epa"] = float(teamdata["epa"]["breakdown"]["auto_points"]) # Auto EPA
    teamEPAs[str(team)]["teleop_epa"] = float(teamdata["epa"]["breakdown"]["teleop_points"]) # Teleop EPA
    teamEPAs[str(team)]["endgame_epa"] = float(teamdata["epa"]["breakdown"]["endgame_points"]) # Endgame EPA

    #print(str(team) + ": " + str(teamEPAs[str(team)]["total_epa"]))
else:
    print(teamEPAs)
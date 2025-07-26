import statbotics
import pandas
import io
import pyperclip

# Constants
YEAR = 2025
EVENT_CODE = "2025micmp4"
MATCH_CODE = "qm3"
PICKLIST_MODE = False

### PULL DATA FROM STATBOTICS ###
sb = statbotics.Statbotics() # Get Statbotics

allTeams = [None] * 6
if (PICKLIST_MODE):
    # NOTE: 7211B entered as 9991. We'll see if that works
    allTeams = ["1076", "27", "33", "51", "201", "226", "302", "1038", "1506", "1596", "2834", "3175", "3357", "3538", "3641", "3655", "3656", "4327", "4381", "4384", "4422", "4776", "5205", "5460", "5641", "5704", "6078", "6517", "7197", "7211", "8424", "8728", "9312", "9991"]
else:
    try:
        matchdata = sb.get_match(EVENT_CODE + "_" + MATCH_CODE) # Get match data

        redAlliance = matchdata["alliances"]["red"]["team_keys"]
        blueAlliance = matchdata["alliances"]["blue"]["team_keys"]
        allTeams = redAlliance + blueAlliance
    except:
        print("It appears that Statbotics is down. Using local Statbotics data instead.\nYou'll need to manually enter the team numbers for the next match (B Roll is 9991).")
        for x in range(1, 7):
            if (x<=3):
                allTeams[x - 1] = input("Enter team number for Red Alliance team #" + str(x) + " ")
            else:
                allTeams[x - 1] = input("Enter team number for Blue Alliance team #" + str(x - 3) + " ")

teamData = dict()

sbDataLocal = pandas.read_csv("statboticsDataLocal.csv") # Just in case

for team in allTeams:
    try:
        sbdata = sb.get_team_year(int(team), YEAR) # Get team data

        teamData[str(team)] = {} # Initialize team in dict

        teamData[str(team)]["total_epa"] = float(sbdata["epa"]["breakdown"]["total_points"]) # Total EPA
        teamData[str(team)]["auto_epa"] = float(sbdata["epa"]["breakdown"]["auto_points"]) # Auto EPA
        teamData[str(team)]["teleop_epa"] = float(sbdata["epa"]["breakdown"]["teleop_points"]) # Teleop EPA
        teamData[str(team)]["endgame_epa"] = float(sbdata["epa"]["breakdown"]["endgame_points"]) # Endgame EPA
    except:
        teamData[str(team)] = {}

        indexCounter = 0

        for target in sbDataLocal["num"]:
            if (int(target) == int(team)):
                if PICKLIST_MODE:
                    pass
                    #teamData[str(team)]["rank"] = float(sbDataLocal["ranking"].loc[sbDataLocal.index[indexCounter]]) # Rank
                teamData[str(team)]["total_epa"] = float(sbDataLocal["total_epa"].loc[sbDataLocal.index[indexCounter]]) # Total EPA
                teamData[str(team)]["auto_epa"] = float(sbDataLocal["auto_epa"].loc[sbDataLocal.index[indexCounter]]) # Auto EPA
                teamData[str(team)]["teleop_epa"] = float(sbDataLocal["teleop_epa"].loc[sbDataLocal.index[indexCounter]]) # Teleop EPA
                teamData[str(team)]["endgame_epa"] = float(sbDataLocal["endgame_epa"].loc[sbDataLocal.index[indexCounter]]) # Endgame EPA

            indexCounter += 1
        
### PULL DATA FROM PRE SCOUTING ###
preScouting = {}
try:
    # Attempt to get online data
    preScouting = pandas.read_csv("https://docs.google.com/spreadsheets/d/1Wmq8-JmdmKnbyP2ugYfs_vGFBbQ_E34Tj_4mVdkYWnA/export?gid=1694826509&format=csv")
    preScouting = preScouting.drop([0,1,2,3,5,6,7])
    preScouting.columns = preScouting.iloc[0]
    preScouting = preScouting[1:].reset_index(drop=True)
    preScouting = pandas.read_csv(io.StringIO(preScouting.to_csv()))
except:
    print("Fell back to local pre-scouting data")
    preScouting = pandas.read_csv("preScoutingData.csv")

indexCounter = 0
for team in preScouting["Team #"]:
    for target in allTeams:
        if (int(team) == int(target)):
            teamData[str(team)]["auto_rating"] = preScouting["Auton"].loc[preScouting.index[indexCounter]]
            teamData[str(team)]["coral_intake_rating"] = preScouting["Coral\n Intake"].loc[preScouting.index[indexCounter]]
            teamData[str(team)]["coral_scoring_rating"] = preScouting["Coral \nScoring\n on L4/3/2"].loc[preScouting.index[indexCounter]]
            teamData[str(team)]["coral_L1_rating"] = preScouting["Coral \nScoring \n on L1"].loc[preScouting.index[indexCounter]]
            teamData[str(team)]["algae_rating"] = preScouting["Algae \nIntake\n & Scoring"].loc[preScouting.index[indexCounter]]
            teamData[str(team)]["endgame_rating"] = preScouting["Endgame"].loc[preScouting.index[indexCounter]]
            teamData[str(team)]["defense_rating"] = preScouting["Defense\n (N/A if not observed)"].loc[preScouting.index[indexCounter]]
    else:
        indexCounter += 1


### PULL DATA FROM PIT SCOUTING ###
pitScouting = {}
try:
    # Try to get online pit scouting data
    pitScouting = pandas.read_csv(io.StringIO(pandas.read_csv("https://docs.google.com/spreadsheets/d/1fdGYdZ9yxb8Jbm_znspI2aFLtc540xTeS0D1ZJOdecU/export?gid=189750286&format=csv").transpose().to_csv()))
except Exception as e:
    print("Fell back to local pit scouting data")
    pitScouting = pandas.read_csv(io.StringIO(pandas.read_csv("pitScoutingData.csv").transpose().to_csv()))

# Set the first row as the heading and drop it
pitScouting.columns = pitScouting.iloc[0]
pitScouting = pitScouting[1:].reset_index(drop=True)

indexCounter = 0
for team in pitScouting["Team Number"]:
    for target in allTeams:
        if (int(team) == int(target)):
            #pass
            teamData[str(team)]["can_score_l4"] = pitScouting["Coral Scoring -- L4"].loc[pitScouting.index[indexCounter]]
            teamData[str(team)]["can_score_l3"] = pitScouting["Coral Scoring -- L3"].loc[pitScouting.index[indexCounter]]
            teamData[str(team)]["can_score_l2"] = pitScouting["Coral Scoring -- L2"].loc[pitScouting.index[indexCounter]]
            teamData[str(team)]["can_score_l1"] = pitScouting["Coral Scoring -- L1"].loc[pitScouting.index[indexCounter]]
            teamData[str(team)]["algae_intake_ability"] = pitScouting["Can you intake Algae from the Reef, the Floor, Both, or Neither?\n* [If they can't intake algae from the reef...] Can you knock algae off the reef? "].loc[pitScouting.index[indexCounter]]
            teamData[str(team)]["algae_scoring_ability"] = pitScouting["Can you score Algae in the Processor, the Barge, Both, or Neither?"].loc[pitScouting.index[indexCounter]]
            teamData[str(team)]["auto_coral_ability"] = pitScouting["In Auto, how many Coral can you score?"].loc[pitScouting.index[indexCounter]]
            teamData[str(team)]["auto_algae_ability"] = pitScouting["In Auto, do you ever handle Algae?"].loc[pitScouting.index[indexCounter]]
    else:
        indexCounter += 1

dataframe = pandas.DataFrame(teamData)

print(dataframe.to_string())
pyperclip.copy(dataframe.to_csv(sep=";", na_rep="N/A"))

# read csv
# get first word

import pandas as pd
import json

data = pd.read_csv("../Data_User/measures.csv")
users = pd.read_csv("../Data_User/users.csv")

def read_json(adress):
    file = open(adress+".json")
    data = json.load(file)
    file.close()
    return data
CRULP_MAPPTING = read_json("mappings/CRULP")
WINDOWS_MAPPING = read_json("mappings/Windows")

# for all incomplete or withdraw, drop from database
users = users[users["status"] == "COMPLETED"]
print(users)
data = data[data["user"].isin(users["uid"])]

# testing milisecond per charachter
stim = data["stimulus"]
wpm = data["wpm"]
time = data["end_time"]-data["start_time"]
for i in range(len(data)):
    words = stim.iloc[i].split(" ")
    calc = (data["end_time"].iloc[i]-data["start_time"].iloc[i])/float(len(words))
    if abs(wpm.iloc[i] - calc)>=0.00000001:
        print("error at line %",i)
        print(wpm.iloc[i])
        print(calc)
        print(len(words))

# test for start time misalignment
# first one for each condition expected to be misaligned because user selects the text and that starts timer but takes a sec to move hands to keyboard. since first two are dummies this dosnt matter
for i in range(len(data)):
    if data["start_time"].iloc[i] != json.loads(data["log"].iloc[i])[0]["timestamp"]:
        print("start time misaligned")
        print(data["user"].iloc[i])
        print(data["condition"].iloc[i])
        # print(data["start_time"].iloc[i]-json.loads(data["log"].iloc[i])[0]["timestamp"])
        # print(data["stimulus"].iloc[i])



# check if entered keystrokes match expected final string
# for i in range(len(data)):
#     target = data["stimulus"][i]
#     string_value = data["log"][i]
#     log_data = json.loads(string_value)
#     target_strokes = ""
#     for char in target:
#         if data["condition"][i] == "crulp":
#             target_strokes+= CRULP_MAPPTING[char]
#         if data["condition"][i] == "windows":
#             target_strokes+= WINDOWS_MAPPING[char]
#         if data["condition"][i] == "baseline":
#             target_strokes+= char

#     logged_strokes = ""
#     for entery in log_data:
#         key = entery["key"]
#         if (key == "Backspace"):
#             logged_strokes = logged_strokes[:-1]
#         elif (len(key)==1):
#             logged_strokes += key
#     if(logged_strokes != target_strokes):
#         print("error at line %",i)
#         break

# #ime target creation
# string_value = data["log"][22]
# parsed_list = json.loads(string_value)
# # print(parsed_list[0])
# target = ""
# for entery in parsed_list:
#     key = entery["key"]
#     if (key == "Backspace"):
#         target = target[:-1]
#     elif (len(key)==1):
#         target += key
# # print(target)
# read csv
# get first word

import pandas as pd
import json

data = pd.read_csv("../Data_User/measures.csv")

def read_json(adress):
    file = open(adress+".json")
    data = json.load(file)
    file.close()
    return data
CRULP_MAPPTING = read_json("mappings/CRULP")
WINDOWS_MAPPING = read_json("mappings/Windows")

# testing milisecond per charachter
stim = data["stimulus"]
wpm = data["wpm"]
time = data["end_time"]-data["start_time"]
for i in range(62,len(data)):
    words = stim[i]
    calc = (data["end_time"][i]-data["start_time"][i])/float(len(words))
    if abs(wpm[i] - calc)>=0.00000000001:
        print("error at line %",i)
        print(wpm[i])
        print(calc)
    break

# test for start time misalignment
for i in range(62,len(data)):
    if data["start_time"][i] != json.loads(data["log"][i])[0]["timestamp"]:
        print("start time misaligned")


# check if entered keystrokes match expected final string
for i in range(62,len(data)):
    target = data["stimulus"][i]
    string_value = data["log"][i]
    log_data = json.loads(string_value)
    target_strokes = ""
    for char in target:
        if data["condition"][i] == "crulp":
            target_strokes+= CRULP_MAPPTING[char]
        if data["condition"][i] == "windows":
            target_strokes+= WINDOWS_MAPPING[char]
        if data["condition"][i] == "baseline":
            target_strokes+= char

    logged_strokes = ""
    for entery in log_data:
        key = entery["key"]
        if (key == "Backspace"):
            logged_strokes = logged_strokes[:-1]
        elif (len(key)==1):
            logged_strokes += key
    if(logged_strokes != target_strokes):
        print("error at line %",i)
        break

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
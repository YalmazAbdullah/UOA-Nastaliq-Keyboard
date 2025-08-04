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

target = data["stimulus"][13]
string_value = data["log"][13]
log_data = json.loads(string_value)

# check if entered keystrokes match expected
target_strokes = ""
for char in target:
    target_strokes+= CRULP_MAPPTING[char]

logged_strokes = ""
for entery in log_data:
    key = entery["key"]
    print(key)
    if (key == "Backspace"):
        logged_strokes = logged_strokes[:-1]
    elif (len(key)==1):
        logged_strokes += key
print(logged_strokes == target_strokes)

#ime target creation
string_value = data["log"][22]
parsed_list = json.loads(string_value)
# print(parsed_list[0])
target = ""
for entery in parsed_list:
    key = entery["key"]
    if (key == "Backspace"):
        target = target[:-1]
    elif (len(key)==1):
        target += key
# print(target)

# testing wpm
stim = data["stimulus"]
wpm = data["wpm"]
time = data["end_time"]-data["start_time"]
for i in range(len(data)):
    words = stim[i].split()
    print(time[i])
    print(words)
    calc = time[i]/float(len(words))
    if (wpm[i] != calc):
        print("error at line %",i)
        print(wpm[i])
        print(calc)
        break
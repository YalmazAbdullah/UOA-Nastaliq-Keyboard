# read csv
# get first word

import pandas as pd
import json

data = pd.read_csv("../Data/UserStudy/measures.csv")

# testing wpm
# stim = data["stimulus"]
# wpm = data["wpm"]
# time = data["end_time"]-data["start_time"]
# for i in range(len(data)):
#     words = stim[i].split()
#     print(time[i])
#     print(words)
#     calc = time[i]/float(len(words))
#     if (wpm[i] != calc):
#         print("error at line %",i)
#         print(wpm[i])
#         print(calc)
#         break

# testing start and end time

# testing error recreation

#ime target creation
string_value = data["log"][22]
parsed_list = json.loads(string_value)
print(parsed_list[0])
target = ""
for entery in parsed_list:
    key = entery["key"]
    if (key == "Backspace"):
        target = target[:-1]
    elif (len(key)==1):
        target += key
print(target)

#ime error analysis
#for each key enterd
    #transpo
    #if it is a char
    #check if this and last are matching with target
    #if not does swapping them match
        #if yes then this is transpo


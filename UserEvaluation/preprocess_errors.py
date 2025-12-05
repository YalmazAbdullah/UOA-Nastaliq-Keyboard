import pandas as pd
import json

data = pd.read_csv("../Data_User/raw/measures.csv")
users = pd.read_csv("../Data_User/raw/users.csv")

def read_json(adress):
    file = open(adress+".json")
    data = json.load(file)
    file.close()
    return data

CRULP_MAPPTING = read_json("assets/CRULP")
WINDOWS_MAPPING = read_json("assets/Windows")

def error_analysis(entered, target):
    # if length same loop over each dyad, 
        # if flipped at any point then transposition, 
        # if not flipped but uses adjacent char then subsitition
    # if length different
        # if length greater then addition, loop over each dyad, if offset then ommision
        # if length shorter then ommision, loop over each dyad, if offset then addition
    return

def ime_processing():
    return

def all_other_processing():
    # get stim
    # for each char entered add to entery
    # if 

    return

# for all incomplete or withdraw, drop from database
users = users[users["status"] == "COMPLETED"]

# drop inclomplete latin square
users = users[users["uid"] != 3]
users = users[users["uid"] != 4]
users = users[users["uid"] != 11]
users = users[users["uid"] != 13]
users = users[users["uid"] != 18]
print(users)

data = data[data["user"].isin(users["uid"])]

#ime target creation
string_value = data["log"][21]
parsed_list = json.loads(string_value)
entered = ""
target = ""
for entery in parsed_list:
    key = entery["key"]
    if (len(target)==0 and key== " "):
        # adding a space, ignore
        continue
    if (key == "Backspace" and len(target)>0):
        # a mistake was identified, removing char
        target = target[:-1]
    if (len(key)==1):
        # adding a char
        entered+=key
        target+=key
    if (len(target)>0 and (key== " " or key=="Enter")):
        # word completed. Begin error analysis
        
        print(entered)
        print(target)
        entered = ""
        target = ""

#error types
# pre entery errors. Everything at the time of enter is correct. any backspaces pressed after word was entered indicates a selection mistake
# when they press enter, the word they had is the target word
# addition, when there is an extra letter

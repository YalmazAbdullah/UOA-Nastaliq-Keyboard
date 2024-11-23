from util import read_tsv
from util import read_json
import pandas as pd
import math

QWERTY_DATA = read_json("keyboards/QWERTY")
KEY_SET = set(QWERTY_DATA["Keys"])
KEY_2_FINGER = QWERTY_DATA["Key_Finger"]
KEY_2_HOME = QWERTY_DATA["Key_Home"]
KEY_COORD = QWERTY_DATA["Key_Coordinate"]
CHAR_2_KEY = QWERTY_DATA["Char_Key_Mapping"]
KEY_2_HAND = QWERTY_DATA["Key_Hand"]
MOD_KEY_DIST = 0

def travel_dist(a,b):
    return math.dist(KEY_COORD[a],KEY_COORD[b])

def calculate_freq(data):
    freq = dict.fromkeys(KEY_SET,0)
    freq["l_shift"] = 0
    freq["r_shift"] = 0
    for line in data:
        for char in line:
            if char == ' ':
                continue
            key = CHAR_2_KEY[char]
            freq[key] = freq.get(key,0)+1
            
            if(key!=char and KEY_2_HAND[key] == "left"):
                freq["r_shift"] = freq.get("r_shift",0)+1
            elif(key!=char and KEY_2_HAND[key] == "right"):
                freq["l_shift"] = freq.get("l_shift",0)+1


    return freq

def score(dataset_name): 

    output = {}

    finger_assign = dict.fromkeys(KEY_SET)
    travel_dist = dict.fromkeys(KEY_SET)
    for key in finger_assign.keys():
        finger_assign[key] = KEY_2_FINGER[key]
        travel_dist[key] = math.dist(KEY_COORD[key],KEY_COORD[KEY_2_HOME[key]])
    finger_assign["l_shift"] = "little"
    finger_assign["r_shift"] = "little"
    travel_dist["l_shift"] = MOD_KEY_DIST
    travel_dist["r_shift"] = MOD_KEY_DIST

    crulp,roman = read_tsv("transformed/keystroke_CRULP/"+dataset_name)
    windows,roman = read_tsv("transformed/keystroke_Windows/"+dataset_name)
    data_sets = {"CRULP":crulp,"WINDOWS":windows,"IME":roman}

    for keyboard in data_sets.keys():
        freq = calculate_freq(data_sets[keyboard])
        df = pd.DataFrame({
            "Finger":finger_assign,
            "Distance":travel_dist,
            "Frequency":freq
        })
        df['Keyboard'] = keyboard
        output[keyboard] = df
    
    output = pd.concat([output["CRULP"],output["WINDOWS"],output["IME"]])
    output.to_csv("./DiscountEvaluation/output/monad/"+dataset_name+".csv", index=True)

def main():
    print("###############################################")
    print("=====================SCORE=====================")
    print("###############################################")
    print()
    score("dakshina_dataset")
    score("roUrParl_dataset")

if __name__ == "__main__":
    main()
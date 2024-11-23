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
PRESS_DEPTH = QWERTY_DATA["Press_Depth"]
SCALE_FACTOR = QWERTY_DATA["Scale_Factor"]

RIGHT_MOD = math.dist(KEY_COORD[KEY_2_HOME["r_shift"]],KEY_COORD["r_shift"]) * SCALE_FACTOR
LEFT_MOD = math.dist(KEY_COORD[KEY_2_HOME["l_shift"]],KEY_COORD["l_shift"]) * SCALE_FACTOR

def calculate_freq(data):
    '''
    Tally frequency of each key within the dataset

    Args:
        data (list): list of setnences transformed inot keystrokes
    Returns:
        freq (dict): frequency table
    '''
    # build a dictionary of all keys
    freq = dict.fromkeys(KEY_SET,0)
    freq["l_shift"] = 0
    freq["r_shift"] = 0

    # for each sentence in data
    for line in data:
        # for each char in sentence
        for char in line:
            # skip spaces
            if char == ' ':
                continue

            # increment frequency of keys
            key = CHAR_2_KEY[char]
            freq[key] = freq.get(key,0)+1
            
            # if uppercase key then add mod distance ie: the distance to move finger to shift key
            if(key!=char and KEY_2_HAND[key] == "left"):
                freq["r_shift"] = freq.get("r_shift",0)+RIGHT_MOD
            elif(key!=char and KEY_2_HAND[key] == "right"):
                freq["l_shift"] = freq.get("l_shift",0)+LEFT_MOD
    return freq

def score(dataset_name): 
    '''
    Calculates finger assignment, finger travel distance, and frequency of each key.
    These results are then saved to csv

    Args:
        dataset_name (string): name of the dataset
    Returns:
        None
    '''
    output = {}

    # finger assignment for all possible key
    finger_assign = dict.fromkeys(KEY_SET)
    # disntace from home for each possible key
    travel_dist = dict.fromkeys(KEY_SET)

    # for each key
    for key in finger_assign.keys():
        # find assigned finger
        finger_assign[key] = KEY_2_FINGER[key]
        # find travel distance from home
        travel_dist[key] = math.dist(KEY_COORD[key],KEY_COORD[KEY_2_HOME[key]]) * SCALE_FACTOR + PRESS_DEPTH

    # consider shift keys
    finger_assign["l_shift"] = "l_little"
    finger_assign["r_shift"] = "r_little"
    travel_dist["l_shift"] = math.dist(KEY_COORD["l_shift"],KEY_COORD[KEY_2_HOME["l_shift"]]) * SCALE_FACTOR + PRESS_DEPTH
    travel_dist["r_shift"] = math.dist(KEY_COORD["r_shift"],KEY_COORD[KEY_2_HOME["r_shift"]]) * SCALE_FACTOR + PRESS_DEPTH

    # read data
    crulp,roman = read_tsv("transformed/keystroke_CRULP/"+dataset_name)
    windows,roman = read_tsv("transformed/keystroke_Windows/"+dataset_name)
    data_sets = {"CRULP":crulp,"WINDOWS":windows,"IME":roman}

    # for each dataset
    for keyboard in data_sets.keys():
        # tally frequency of each key
        freq = calculate_freq(data_sets[keyboard])
        # buid dataframe
        df = pd.DataFrame({
            "Finger":finger_assign,
            "Distance":travel_dist,
            "Frequency":freq
        })
        df['Keyboard'] = keyboard
        output[keyboard] = df
    
    # output results
    output = pd.concat([output["CRULP"],output["WINDOWS"],output["IME"]])
    output.to_csv("./DiscountEvaluation/output/monad/"+dataset_name+".csv", index=True)

##################
##     MAIN     ##
##################
def main():
    score("dakshina_dataset")
    score("roUrParl_dataset")

if __name__ == "__main__":
    main()
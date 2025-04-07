# STL
import pandas as pd
import math
from tqdm import tqdm

# CUSTOM
from util import read_tsv
from util import key_distance
from util import KEY_SET
from util import KEY_2_FINGER,KEY_2_HAND,KEY_2_HOME,CHAR_2_KEY
from util import PRESS_DEPTH,RIGHT_MOD,LEFT_MOD


def calculate_freq(data):
    '''
    Tally frequency of each key within the dataset

    Args:
        data (list): list of setnences transformed inot keystrokes
    Returns:
        freq (dict): frequency table
    '''
    # build a dictionary of all keys
    freq = dict.fromkeys(KEY_SET,int(0))
    freq["l_shift"] = int(0)
    freq["r_shift"] = int(0)

    # for each sentence in data
    for i in tqdm(range(len(data)), desc="Count Frequency"):
        line = data[i]
        # for each char in sentence
        for char in line:
            # skip spaces
            if char == ' ':
                continue

            # increment frequency of keys
            key = CHAR_2_KEY[char]
            freq[key] = freq.get(key,0) + 1
            
            # if modded key then add mod press
            if(key!=char and KEY_2_HAND[key] == "L"):
                freq["r_shift"] += 1
            elif(key!=char and KEY_2_HAND[key] == "R"):
                freq["l_shift"] += 1
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
    for key in tqdm(finger_assign.keys(), desc="Calculating Distance"):
        # find assigned finger
        finger_assign[key] = KEY_2_FINGER[key]
        # find travel distance from home
        travel_dist[key] = key_distance(key,KEY_2_HOME[key]) + PRESS_DEPTH

    # consider shift keys
    finger_assign["l_shift"] = "L_Little"
    finger_assign["r_shift"] = "R_Little"
    travel_dist["l_shift"] = LEFT_MOD + PRESS_DEPTH
    travel_dist["r_shift"] = RIGHT_MOD + PRESS_DEPTH

    # read data
    crulp,roman = read_tsv("interim/transformed/keystroke_CRULP/"+dataset_name)
    windows,roman = read_tsv("interim/transformed/keystroke_Windows/"+dataset_name)
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
    output.to_csv("../data/monad/"+dataset_name+".csv", index=True)

##################
##     MAIN     ##
##################
def main():
    print("Dataset: Dakshina".center(100, "="))
    score("dakshina_dataset")
    print("Dataset: Roman Urdu Parl".center(100, "="))
    score("roUrParl_dataset")
    print("Dataset: Combined Subset".center(100, "="))
    score("combined_subset")

if __name__ == "__main__":
    main()
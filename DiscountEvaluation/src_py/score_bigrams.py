# Finger travel for each bigram (complicated)
# Frequency of bigram
# Is same hand
# Is same finger not same key
# Is hurdle
# Is reach
# SUM(f*variable)
# Hand = 1
# Other two=0.5

from util import read_tsv,write_tsv
from util import read_json
import pandas as pd
from itertools import product
import math

from transform_dyad import transform

QWERTY_DATA = read_json("keyboards/QWERTY")
CHAR_SET = set(QWERTY_DATA["Charachters"])
CHAR_2_KEY = QWERTY_DATA["Char_Key_Mapping"]
KEY_2_HAND = QWERTY_DATA["Key_Hand"]
KEY_2_FINGER = QWERTY_DATA["Key_Finger"]
KEY_2_ROW = QWERTY_DATA["Key_Row"]
KEY_2_HOME = QWERTY_DATA["Key_Home"]
KEY_COORD = QWERTY_DATA["Key_Coordinate"]
MOD_KEY_DIST = 0

def read_dyad_tsv(path):
    data = read_json(path)
    return data["Native"],data["Roman"]

def travel_dist(a,b):
    return math.dist(KEY_COORD[a],KEY_COORD[b])

def dyad_dist(dyad,keys,is_same_finger,is_same_hand):
    distance = 0

    # get keys used in dyad
    first_key = keys[0]
    second_key = keys[1]
    
    # check if shift is used
    is_fist_modified = first_key != dyad[0]
    is__second_modified = second_key != dyad[1]


    if(is_same_finger):
        # add distance from first key to second key
        distance += travel_dist(first_key,second_key)
    else:
        # add distance from first key back to the home row
        distance += travel_dist(first_key,KEY_2_HOME[first_key])
        # add distance from home row to second key
        distance += travel_dist(KEY_2_HOME[second_key],second_key)


    if (is_fist_modified and is__second_modified):
        # if different hand
        if(not is_same_hand):
            # add mod to home distance
            distance += MOD_KEY_DIST
            # add home to mod distance 
            distance += MOD_KEY_DIST
    elif (is_fist_modified or is__second_modified):
        # add mod to home distance
        distance += MOD_KEY_DIST

    return distance

    #########################################################################
    # This wont work because of add_1 smoothing                             #
    #########################################################################
    # if first in sentence:
    # if(i == 0):
    #     # add distance from home row to first key
    #     distance += travel_dist(KEY_2_HOME(first_key),first_key)
    #     if(is_fist_modified):
    #         # add home to mod distance
    #         distance += 0

    # # if last in sentence
    # if(i == len):
    #     # add distance of second to home
    #     distance += travel_dist(second_key,KEY_2_HOME(second_key))
    #     # if second moded:
    #     if(is__second_modified):
    #         # add mod to home distance
    #         distance += 0
    #########################################################################    
          

def score(dataset_name):     
    # Generate dictionary of all possible bigrams
    two_char_permutations = list(product(CHAR_SET, repeat=2))
    permutation_strings = [''.join(p) for p in two_char_permutations]

    dyad_sameHand = {}
    dyad_sameKey = {}
    dyad_sameFinger = {}
    dyad_isReach = {} # if not home
    dyad_isHurdle = {} # if not home and both different
    dyad_distance = {}

    for dyad in permutation_strings:
        keys = (CHAR_2_KEY[dyad[0]],CHAR_2_KEY[dyad[1]])
        dyad_sameKey[dyad]      = (keys[0] == keys[1])
        dyad_sameHand[dyad]     = (KEY_2_HAND[keys[0]] == KEY_2_HAND[keys[1]] )
        dyad_sameFinger[dyad]   = (KEY_2_FINGER[keys[0]] == KEY_2_FINGER[keys[1]])
        # if one or more is not home
        dyad_isReach[dyad]      = (KEY_2_ROW[keys[0]] != 0) or (KEY_2_ROW[keys[1]] != 0)
        # if both are not home and different rows
        dyad_isHurdle[dyad]     = ((KEY_2_ROW[keys[0]] != 0) and (KEY_2_ROW[keys[1]] != 0)) and (KEY_2_ROW[keys[0]] != KEY_2_ROW[keys[1]])
        # distance required to go from one key in bigram to other
        dyad_distance[dyad]     = dyad_dist(dyad,keys,dyad_sameFinger[dyad],dyad_sameHand[dyad])

    # retrive data
    crulp,windows,roman = transform(dataset_name)
    data_sets = {"CRULP":crulp,"WINDOWS":windows,"IME":roman}

    output = {}

    # tally frequency of dyad
    for keyboard in data_sets.keys():
        dyad_freq = {}
        data_set = data_sets[keyboard]
        for sentence in data_set:
            for i in range(len(sentence)):
                dyad = sentence[i]
                dyad_freq[dyad] = dyad_freq.get(dyad,0)+ 1
        
        # build datafram
        df = pd.DataFrame({
            'Distance'      : dyad_distance,
            'SameHand'      : dyad_sameHand,
            'SameKey'       : dyad_sameKey,
            'SameFinger'    : dyad_sameFinger,
            'Reach'         : dyad_isReach,
            'Hurde'         : dyad_isHurdle,
            'Frequency'     : dyad_freq,
        })
        df['Keyboard'] = keyboard
        output[keyboard] = df
        output['Frequency'] = df['Frequency'].fillna(0)

    output = pd.concat([output["CRULP"],output["WINDOWS"],output["IME"]])
    output.to_csv("./DiscountEvaluation/output/dyad/"+dataset_name+".csv", index=True)

def main():
    score("dakshina_dataset")
    score("roUrParl_dataset")

if __name__ == "__main__":
    main()
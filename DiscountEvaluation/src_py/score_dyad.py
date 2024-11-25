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
PRESS_DEPTH = QWERTY_DATA["Press_Depth"]
SCALE_FACTOR = QWERTY_DATA["Scale_Factor"]

def travel_dist(a,b):
    '''
    Euclidian distance between 2 keys using their coordinates

    Args:
        a (char): first key
        b (char): second key
    Returns:
        distance (float): euclidian distance between keys
    '''
    return math.dist(KEY_COORD[a],KEY_COORD[b]) * SCALE_FACTOR

RIGHT_MOD = travel_dist(KEY_2_HOME["r_shift"],"r_shift") * SCALE_FACTOR
LEFT_MOD = travel_dist(KEY_2_HOME["l_shift"],"l_shift") * SCALE_FACTOR

def dyad_dist(dyad,keys,is_same_finger,is_same_hand):
    '''
    Calculate the travel distance for each finger for a particular dyad.

    Args:
        dyad (string): the dyad
        keys (keys): decoded keys
        is_same_finger (bool): true if the same finger is used to enter dyad
        is_same_hand (bool): true if the same hand is used to enter dyad
    Returns:
        finger_distance (dict): the travel distance split up by finger. Keys are finger and value is distance.
    '''
    # get keys used in dyad
    first_key = keys[0]
    second_key = keys[1]
    
    # get fingers used in dyad
    first_finger = KEY_2_FINGER[first_key]
    second_finger = KEY_2_FINGER[second_key]
    finger_distance = {
        "l_little" : 0,   "r_little" : 0,
        "l_ring" : 0,     "r_ring" : 0,
        "l_middle" : 0,   "r_middle" : 0,
        "l_index" : 0,    "r_index" : 0,
    }

    # check if shift is used
    is_first_modified = first_key != dyad[0]
    is__second_modified = second_key != dyad[1]

    if(is_same_finger):
        # add distance from first key to second key
        finger_distance[first_finger] += travel_dist(first_key,second_key) + PRESS_DEPTH
    else:
        # add distance from first key back to the home row
        finger_distance[first_finger] += travel_dist(first_key,KEY_2_HOME[first_key])
        # add distance from home row to second key
        finger_distance[second_finger] += travel_dist(KEY_2_HOME[second_key],second_key) + PRESS_DEPTH

    if (is_first_modified and is__second_modified):
        # if different hand
        if(not is_same_hand):
            finger_distance["l_little"] += LEFT_MOD
            finger_distance["r_little"] += RIGHT_MOD
            if(is__second_modified):
               finger_distance["r_little"] += PRESS_DEPTH
    elif (is_first_modified or is__second_modified):
        # check which side key is modified
        if(is_first_modified):
            # check which side is modified
            if (KEY_2_HAND[first_key] == "left"):
                finger_distance["r_little"] += RIGHT_MOD
            else:
                # has to be right
                finger_distance["l_little"] += LEFT_MOD
        else:
            # has to be second
            if (KEY_2_HAND[second_key] == "left"):
                finger_distance["r_little"] += RIGHT_MOD + PRESS_DEPTH
            else:
                # has to be right
                finger_distance["l_little"] += LEFT_MOD + PRESS_DEPTH
    return finger_distance

def dyad_dist_special(char, key, is_end):
    '''
    Calcuating distances for special case which is start and end of
    sentence dyads.
    '''
    finger_distance = {
        "l_little" : 0,   "r_little" : 0,
        "l_ring" : 0,     "r_ring" : 0,
        "l_middle" : 0,   "r_middle" : 0,
        "l_index" : 0,    "r_index" : 0,
    }

    # get travel distance
    finger = KEY_2_FINGER[key]
    finger_distance[finger] += travel_dist(KEY_2_HOME[key], key) + PRESS_DEPTH

    # check if modified
    if(key != char):
        # add home to mod distance
        if(KEY_2_HAND[key] == "left"):
            finger_distance["r_little"] += RIGHT_MOD if(is_end) else RIGHT_MOD + PRESS_DEPTH
        else:
            finger_distance["l_little"] += LEFT_MOD if(is_end) else LEFT_MOD + PRESS_DEPTH
    return finger_distance
    

def score(dataset_name):
    '''
    Score the dyads for the dataset by caculating travel distance, frequency
    and checking if same finger, same key, same hand, reach, and hurdle. Results
    are saved to output csv.

    Args:
        dataset_name (string): name of dataset
    Returns:
        None
    '''
    output = {}
    two_char_permutations = list(product(CHAR_SET, repeat=2))
    permutation_strings = [''.join(p) for p in two_char_permutations]

    # Columns
    dyad_sameHand   = {}
    dyad_sameKey    = {}
    dyad_sameFinger = {}
    dyad_isReach    = {} # if not home
    dyad_isHurdle   = {} # if not home and both different
    
    # Distance columns:
    finger_distance = {}

    # Calculate dyad distances
    for dyad in permutation_strings:
        keys = (CHAR_2_KEY[dyad[0]],CHAR_2_KEY[dyad[1]])
        dyad_sameKey[dyad]      = (keys[0] == keys[1])
        dyad_sameHand[dyad]     = (KEY_2_HAND[keys[0]] == KEY_2_HAND[keys[1]] )
        dyad_sameFinger[dyad]   = (KEY_2_FINGER[keys[0]] == KEY_2_FINGER[keys[1]])
        # if one or more is not home
        dyad_isReach[dyad]      = (KEY_2_ROW[keys[0]] != 0) or (KEY_2_ROW[keys[1]] != 0)
        # if both are not home and different rows
        dyad_isHurdle[dyad]     =  ((KEY_2_ROW[keys[0]] != 0) and (KEY_2_ROW[keys[1]] != 0)) and dyad_sameHand[dyad]
        # distance required to go from one key in bigram to other
        finger_distance[dyad]   = dyad_dist(dyad,keys,dyad_sameFinger[dyad],dyad_sameHand[dyad])

    # handle special start case:
    for char in CHAR_SET:
        markers = ["<s>","</s>"]
        for i in range(len(markers)):
            mark = markers[i]
            is_end = False
            if(i==0):
                dyad = mark+char
            else:
                dyad = char+mark
                is_end = True
            key = CHAR_2_KEY[char]
            dyad_isReach[dyad]      = (KEY_2_ROW[key] != 0)
            # The following simply cannot be true because this dyad actually consists of just one key
            dyad_sameKey[dyad]      = False
            dyad_sameHand[dyad]     = False
            dyad_sameFinger[dyad]   = False
            dyad_isHurdle[dyad]     = False
            # distance is the same as naive distance
            finger_distance[dyad]   = dyad_dist_special(char,key, is_end)


    # Retrive data for each keyboard diad frequency counting
    crulp,windows,roman = transform(dataset_name)
    data_sets = {"CRULP":crulp,"WINDOWS":windows,"IME":roman}

    # tally frequency of dyad
    for keyboard in data_sets.keys():
        dyad_freq = {key: 0 for key in finger_distance.keys()}
        data_set = data_sets[keyboard]
        for sentence in data_set:
            for i in range(len(sentence)):
                dyad = sentence[i]
                dyad_freq[dyad] = dyad_freq.get(dyad,0)+ 1
        
        # build dataframe
        df = pd.DataFrame({
            'SameHand'              : dyad_sameHand,
            'SameKey'               : dyad_sameKey,
            'SameFinger'            : dyad_sameFinger,
            'Reach'                 : dyad_isReach,
            'Hurdle'                 : dyad_isHurdle,
            'Frequency'             : dyad_freq,
        })
        # add distance col for each finger
        df = pd.concat([df, pd.DataFrame.from_dict(finger_distance, orient="index")], axis=1)
        df['left_total'] = df[['l_little', 'l_ring', 'l_middle', 'l_index']].sum(axis=1)
        df['right_total'] = df[['r_little', 'r_ring', 'r_middle', 'r_index']].sum(axis=1)
        df['total_distance'] = df[['right_total', 'left_total']].sum(axis=1)

        df['Keyboard'] = keyboard
        output[keyboard] = df
    
    # Write the results
    output = pd.concat([output["CRULP"],output["WINDOWS"],output["IME"]])
    output.to_csv("./DiscountEvaluation/output/dyad/"+dataset_name+".csv", index=True)

##################
##     MAIN     ##
##################
def main():
    score("dakshina_dataset")
    score("roUrParl_dataset")

if __name__ == "__main__":
    main()

#STL
from tqdm import tqdm

# VENDOR
import pandas as pd
from nltk import edit_distance

# CUSTOM
from transform_keystroke import transform
from util import key_distance
from util import read_tsv
from util import CRULP_MAPPTING, WINDOWS_MAPPING
from util import KEY_2_HAND,KEY_2_HOME, CHAR_2_KEY
from util import RIGHT_MOD,LEFT_MOD

def keyying_dist(keystrokes):
    keystrokes = keystrokes.replace(" ", "")
    # calculate distance from key to home for first
    key = CHAR_2_KEY[keystrokes[0]]
    dist = key_distance(KEY_2_HOME[key],key)
    if (key != keystrokes[0]):
        if(KEY_2_HAND[key]=="left"):
            # add distance to go from right home to mod
            dist += RIGHT_MOD
        else:
            # add distance to go from left home to home
            dist += LEFT_MOD


    for i in range(1,len(keystrokes)):
        # for all the rest calculate teh dsitance from last to current
        key = CHAR_2_KEY[keystrokes[i]]
        prev_key = CHAR_2_KEY[keystrokes[i-1]]
        dist+=key_distance(prev_key,key)

        is_current_modified = key != keystrokes[0]
        is_prev_modified = prev_key != keystrokes[1]

        # if current is modifed and previous is not
        if (is_current_modified and not is_prev_modified):
            # and modification on left hand
            if(KEY_2_HAND[key]=="left"):
                # add distance to go from right home to mod
                dist += RIGHT_MOD
            else:
                # add distance to go from left home to home
                dist += LEFT_MOD
        
        # prev key not modified and current key is modified
        if (not is_current_modified and is_prev_modified):
            # and modification on left hand
            if(KEY_2_HAND[key]=="left"):
                # add distance to go from right mod to hom
                dist += RIGHT_MOD
            else:
                # add distance to go from left mod to home
                dist += LEFT_MOD

    # calcualte the distance of last key back to home
    key = CHAR_2_KEY[keystrokes[len(keystrokes)-1]]
    dist += key_distance(key, KEY_2_HOME[key])
    if (key != keystrokes[0]):
        if(KEY_2_HAND[key]=="left"):
            # add distance to go from right home to mod
            dist += RIGHT_MOD
        else:
            # add distance to go from left home to home
            dist += LEFT_MOD
    return dist

def score(dataset_name):
    native,roman = read_tsv("transformed/sentences/"+dataset_name)

    keystroke_CRULP = transform(native, CRULP_MAPPTING)
    keystroke_Windows = transform(native, WINDOWS_MAPPING)

    crulp_roman_levin    = []
    windows_roman_levin  = []
    crulp_windows_levin  = []

    crulp_dist    = []
    windows_dist  = []
    ime_dist  = []
    
    # calculate levinsteine distance
    for i in tqdm(range(len(roman))):
        if(i==58):
            # this sentence is bugged. It is too long to reasonabily calculate the distance.
            crulp_roman_levin.append(None)
            windows_roman_levin.append(None)
            crulp_windows_levin.append(None)

            crulp_dist.append(None)
            windows_dist.append(None)
            ime_dist.append(None)
            continue
        crulp_roman_levin.append(edit_distance(keystroke_CRULP[i],roman[i]))
        windows_roman_levin.append(edit_distance(keystroke_Windows[i],roman[i]))
        crulp_windows_levin.append(edit_distance(keystroke_CRULP[i],keystroke_Windows[i]))

        crulp_dist.append(keyying_dist(keystroke_CRULP[i]))
        windows_dist.append(keyying_dist(keystroke_Windows[i]))
        ime_dist.append(keyying_dist(roman[i]))

    # write levinsteine distance to csv
    output = pd.DataFrame({
        "CRULP":keystroke_CRULP,
        "WINDOWS":keystroke_Windows,
        "IME":roman,

        "CRULP_2_IME_DISTANCE": crulp_roman_levin,
        "WINDOWS_2_IME_DISTANCE": windows_roman_levin,
        "CRULP_2_WINDOWS_DISTANCE": crulp_windows_levin,

        "CRULP_DISTANCE": crulp_dist,
        "WINDOWS_DISTANCE": windows_dist,
        "IME_DISTANCE": ime_dist
    })
    output.to_csv("./DiscountEvaluation/output/sentence/"+dataset_name+".csv", index=True)
    pass

##################
##     MAIN     ##
##################
def main():
    score("dakshina_dataset")
    score("roUrParl_dataset")

if __name__ == "__main__":
    main()
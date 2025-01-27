# STL
import csv
import json
import math

'''
Read .tsv file, seperate into native and roman.
'''
def read_tsv(file_name):
    # Read the .tsv file
    with open('./DiscountEvaluation/corpus/'+file_name+'.tsv', 'r', encoding='utf-8') as file:
        native = []
        roman = []

        for line in file:
            # Split the line into two parts based on the tab character
            parts = line.strip().replace('"""', '"').split('\t')
            
            # Check if the line has exactly two parts
            if len(parts) == 2:
                native.append(parts[0])
                roman.append(parts[1])

    # Print the resulting dictionary
    return native,roman

'''
Read .tsv file, seperate into native and roman.
'''
def read_json(adress):
    file = open("./DiscountEvaluation/"+adress+".json")
    data = json.load(file)
    file.close()
    return data

'''
Write the arrays as .tsv file
'''
def write_tsv(native, roman, file_name):
    # write to headless .tsv
    with open('./DiscountEvaluation/corpus/'+ file_name +'.tsv', 'w', newline='', encoding='utf-8') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
    
        for val1, val2 in zip(native, roman):
            writer.writerow([val1, val2])

'''
Simple evaluation function that returns percentage of tokens removed from dataset.
'''
def eval(input_size, output_size):
    ratio = float(output_size)/input_size
    print("Loss:    "+str(round((1-ratio) *100,6))+"%")

'''
Preparing data fro layouts
'''
CRULP_MAPPTING = read_json("keyboards/mappings/CRULP")
WINDOWS_MAPPING = read_json("keyboards/mappings/Windows")
QWERTY_DATA = read_json("keyboards/QWERTY")
KEY_SET = set(QWERTY_DATA["Keys"])
CHAR_SET = set(QWERTY_DATA["Charachters"])
KEY_2_FINGER = QWERTY_DATA["Key_Finger"]
KEY_2_HOME = QWERTY_DATA["Key_Home"]
KEY_2_ROW = QWERTY_DATA["Key_Row"]
KEY_COORD = QWERTY_DATA["Key_Coordinate"]
CHAR_2_KEY = QWERTY_DATA["Char_Key_Mapping"]
KEY_2_HAND = QWERTY_DATA["Key_Hand"]
PRESS_DEPTH = QWERTY_DATA["Press_Depth"]
SCALE_FACTOR = QWERTY_DATA["Scale_Factor"]
RIGHT_MOD = math.dist(KEY_COORD[KEY_2_HOME["r_shift"]],KEY_COORD["r_shift"]) * SCALE_FACTOR
LEFT_MOD = math.dist(KEY_COORD[KEY_2_HOME["l_shift"]],KEY_COORD["l_shift"]) * SCALE_FACTOR

'''
Euclidian distance between 2 keys using their coordinates
'''
def key_distance(a,b):
    if (a==None or b==None):
        return 0
    return math.dist(KEY_COORD[a],KEY_COORD[b]) * SCALE_FACTOR

'''
Caclualte distances and characterize stroke of dyad
'''
def evaluate_dyad(a,b):
    # Get keys for each char in dyad
    f_key = CHAR_2_KEY.get(a,None)
    s_key = CHAR_2_KEY.get(b,None)

    # Get finger assignment
    f_finger = KEY_2_FINGER.get(f_key,None)
    s_finger = KEY_2_FINGER.get(s_key,None)

    # Get hand assignment
    f_hand = KEY_2_HAND.get(f_key,None)
    s_hand = KEY_2_HAND.get(s_key,None)

    # Get row
    f_row = KEY_2_ROW.get(f_key,None)
    s_row = KEY_2_ROW.get(s_key,None)

    # Get home
    f_home = KEY_2_HOME.get(f_key,None)
    s_home = KEY_2_HOME.get(s_key,None)

    # Charachterize the stroke
    same_key = 1 if f_key == s_key else 0
    same_finger = 1 if f_finger == s_finger else 0
    same_hand = 1 if f_hand == s_hand else 0
    is_reach = 1 if s_row!=1 else 0
    is_hurdle = 1 if (same_hand == 1 and
                      f_row!=1 and 
                      s_row!=1 and f_row!=s_row) else 0

    # Prepare output structure
    output = {
        "dyad": a+b,

        "SameHand":same_hand,
        "SameFinger":same_finger,
        "SameKey":same_key,
        "Reach":is_reach,
        "Hurdle":is_hurdle,

        "Press_L_Little":int(0),
        "Press_L_Ring":int(0),
        "Press_L_Middle":int(0),
        "Press_L_Index":int(0),
        "Press_R_Little":int(0),
        "Press_R_Ring":int(0),
        "Press_R_Middle":int(0),
        "Press_R_Index":int(0),

        "Dist_L_Little":0,
        "Dist_L_Ring":0,
        "Dist_L_Middle":0,
        "Dist_L_Index":0,
        "Dist_R_Little":0,
        "Dist_R_Ring":0,
        "Dist_R_Middle":0,
        "Dist_R_Index":0,
    }

    # Calculate distances
    if same_finger:
        # distance + release + press
        f2s = key_distance(f_key, s_key) + PRESS_DEPTH + PRESS_DEPTH
        output["Dist_"+s_finger] += f2s
        output["Press_"+s_finger] += 1
    else:
        # distance of first->home + Press Depth because releasing still requires motion
        f2home = key_distance(f_key, f_home) + PRESS_DEPTH
        # distance of home->second + Press Depth
        home2s = key_distance(s_home, s_key) + PRESS_DEPTH
        if(f_finger!=None):
            output["Dist_"+f_finger] += f2home
        if(s_finger!=None):
            output["Dist_"+s_finger] += home2s

        # key press not considered for lifting, therefore we only care
        # about second key.
        if(s_finger!=None):
            output["Press_"+s_finger] += 1

    # Consider distance of mod keys
    is_f_mod = f_key != a
    is_s_mod = s_key != b
    
    # when same hand both moded then key will just be help
    if (is_f_mod and is_s_mod and same_hand):
        return output
    # when both moded but different hands, we switch mod keys
    elif (is_f_mod and is_s_mod):
        # Mod -> home + press or release
        output["Dist_L_Little"] += LEFT_MOD + PRESS_DEPTH
        # Home -> mod + press or release
        output["Dist_R_Little"] += RIGHT_MOD + PRESS_DEPTH
        # We only consider second key as press
        if (s_hand == "R"):
            output["Press_L_Little"] += 1
        else:
            output["Press_R_Little"] += 1
    elif (is_f_mod == True):
        # Distance of mod -> home + lift so pressing is not counted 
        if (f_hand == "R"):
            output["Dist_L_Little"] += LEFT_MOD + PRESS_DEPTH
        else:
            output["Dist_R_Little"] += RIGHT_MOD + PRESS_DEPTH
    elif (is_s_mod == True):
        # Distance of home -> mod + press so pressing is counted 
        if (s_hand == "R"):
            output["Dist_L_Little"] += LEFT_MOD + PRESS_DEPTH
            output["Press_L_Little"] += 1
        else:
            output["Dist_R_Little"] += RIGHT_MOD + PRESS_DEPTH
            output["Press_R_Little"] += 1
    return output

from pprint import pprint
def main():
    pprint(evaluate_dyad("a","A"))

if __name__ == "__main__":
    main()
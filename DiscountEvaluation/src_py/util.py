# STL
import csv
import json
import math

'''
Simple evaluation function that returns percentage of tokens removed from dataset.
'''
def eval(input_size, output_size):
    ratio = float(output_size)/input_size
    print("Loss:    "+str(round((1-ratio) *100,6))+"%")

'''
Read .tsv file, seperate into native and roman.
'''
def read_tsv(file_name):
    # Read the .tsv file
    with open('./DiscountEvaluation/data/'+file_name+'.tsv', 'r', encoding='utf-8') as file:
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
    with open('./DiscountEvaluation/data/'+ file_name +'.tsv', 'w', newline='', encoding='utf-8') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
    
        for val1, val2 in zip(native, roman):
            writer.writerow([val1, val2])


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
    return math.dist(KEY_COORD[a],KEY_COORD[b]) * SCALE_FACTOR
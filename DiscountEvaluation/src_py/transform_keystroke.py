#STL
from tqdm import tqdm

# Vendor
import pandas as pd
from nltk import edit_distance

# Custom
from util import read_tsv, write_tsv
from util import read_json

CRULP_MAPPTING = read_json("keyboards/mappings/CRULP")
WINDOWS_MAPPING = read_json("keyboards/mappings/Windows")
def transform(native, mapping):
    '''
    Transforms the content of the text into keystrokes. For example مش becomes "ab" for the 
    Windows layout.

    Args:
        native (list): list of sentences in dataset
        mapping (dictionary): dictionary that maps chars to their keys
    Returns:
        transformed (list): list of senteces transformed into keystrokes
    '''
    transformed = []
    for i in range(len(native)):
        transformed_line = ''
        for char in native[i]:
            transformed_line = transformed_line + mapping[char]
        transformed.append(transformed_line)
    return transformed


def transform_keystrokes(dataset_name, calculate_distance = False):
    '''
    This function is used to transform and write the transformation results. Levinsteine
    distance is also calculated for each sentence and written to csv

    Args:
        dataset_name (string): name of the dataset.
        calculate_distance: specfies if levinsteine distance should be calculated.
    Returns:
        None
    '''
    # read data
    native,roman = read_tsv("transformed/sentences/"+dataset_name)
    # transform for each keyboard layout
    transformed_CRULP = transform(native, CRULP_MAPPTING)
    transformed_Windows = transform(native, WINDOWS_MAPPING)
    # write results
    write_tsv(transformed_CRULP,roman,"transformed/keystroke_CRULP/"+dataset_name)
    write_tsv(transformed_Windows,roman,"transformed/keystroke_CRULP/"+dataset_name)

    crulp_roman_dist    = []
    windows_roman_dist  = []
    crulp_windows_dist  = []

    if not calculate_distance:
        return
    
    # calculate levinsteine distance
    for i in tqdm(range(len(roman))):
        if(i==58):
            # this sentence is bugged. It is too long to reasonabily calculate the distance.
            crulp_roman_dist.append(None)
            windows_roman_dist.append(None)
            crulp_windows_dist.append(None)
            continue
        crulp_roman_dist.append(edit_distance(transformed_CRULP[i],roman[i]))
        windows_roman_dist.append(edit_distance(transformed_Windows[i],roman[i]))
        crulp_windows_dist.append(edit_distance(transformed_CRULP[i],transformed_Windows[i]))

    # write levinsteine distance to csv
    output = pd.DataFrame({
        "CRULP":transformed_CRULP,
        "WINDOWS":transformed_Windows,
        "IME":roman,
        "CRULP_2_IME_DISTANCE": crulp_roman_dist,
        "WINDOWS_2_IME_DISTANCE": windows_roman_dist,
        "CRULP_2_WINDOWS_DISTANCE": crulp_windows_dist
    })
    output.to_csv("./DiscountEvaluation/output/levinsteine/"+dataset_name+".csv", index=True)


##################
##     MAIN     ##
##################
def main():
    # Dataset: Dakshina
    print("Keystroke Transformation: dakshina")
    transform_keystrokes("dakshina_dataset")
    # Dataset: Roman Urdu Parl
    print("Keystroke Transformation: roUrParl")
    transform_keystrokes("roUrParl_dataset")

if __name__ == "__main__":
    main()
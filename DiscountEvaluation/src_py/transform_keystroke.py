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
    '''
    transformed = []
    distance = []
    for i in range(len(native)):
        transformed_line = ''
        for char in native[i]:
            transformed_line = transformed_line + mapping[char]
        transformed.append(transformed_line)
    return transformed


def transform_keystrokes(dataset_name):
    '''
    '''
    native,roman = read_tsv("transformed/sentences/"+dataset_name)
    transformed_CRULP = transform(native, CRULP_MAPPTING)
    transformed_Windows = transform(native, WINDOWS_MAPPING)
    write_tsv(transformed_CRULP,roman,"transformed/keystroke_CRULP/"+dataset_name)
    write_tsv(transformed_Windows,roman,"transformed/keystroke_CRULP/"+dataset_name)

    crulp_roman_dist    = []
    windows_roman_dist  = []
    crulp_windows_dist  = []

    for i in range(len(roman)):
        crulp_roman_dist.append(edit_distance(transformed_CRULP[i],roman[i]))
        windows_roman_dist.append(edit_distance(transformed_CRULP[i],roman[i]))
        crulp_windows_dist.append(edit_distance(transformed_CRULP[i],transformed_Windows[i]))

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
    transform_keystrokes("dakshina_dataset")
    # Dataset: Roman Urdu Parl
    transform_keystrokes("roUrParl_dataset")

if __name__ == "__main__":
    main()
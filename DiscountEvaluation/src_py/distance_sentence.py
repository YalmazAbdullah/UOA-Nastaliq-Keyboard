#STL
from tqdm import tqdm

# VENDOR
import pandas as pd
from nltk import edit_distance

# CUSTOM
from transform_keystroke import transform
from util import read_tsv
from util import CRULP_MAPPTING, WINDOWS_MAPPING

def edit_dist(dataset_name):
    native,roman = read_tsv("transformed/sentences/"+dataset_name)
    keystroke_CRULP = transform(native, CRULP_MAPPTING)
    keystroke_Windows = transform(native, WINDOWS_MAPPING)

    crulp_roman_levin    = []
    windows_roman_levin  = []
    crulp_windows_levin  = []
    
    # calculate levinsteine distance
    for i in tqdm(range(len(roman))):
        if(i==58 and dataset_name == "dakshina_dataset"):
            # this sentence is bugged. It is too long to reasonabily calculate the distance.
            crulp_roman_levin.append(None)
            windows_roman_levin.append(None)
            crulp_windows_levin.append(None)
        else:
            crulp_roman_levin.append(edit_distance(keystroke_CRULP[i],roman[i]))
            windows_roman_levin.append(edit_distance(keystroke_Windows[i],roman[i]))
            crulp_windows_levin.append(edit_distance(keystroke_CRULP[i],keystroke_Windows[i]))
    
    # write levinsteine distance to csv
    output = pd.DataFrame({
        "CRULP":keystroke_CRULP,
        "WINDOWS":keystroke_Windows,
        "IME":roman,

        "CRULP_2_IME_DISTANCE": crulp_roman_levin,
        "WINDOWS_2_IME_DISTANCE": windows_roman_levin,
        "CRULP_2_WINDOWS_DISTANCE": crulp_windows_levin
    })
    output.to_csv("./DiscountEvaluation/output/sentence/distance/"+dataset_name+".csv", index=True)

##################
##     MAIN     ##
##################
def main():
    edit_dist("dakshina_dataset")
    edit_dist("roUrParl_dataset")

if __name__ == "__main__":
    main()
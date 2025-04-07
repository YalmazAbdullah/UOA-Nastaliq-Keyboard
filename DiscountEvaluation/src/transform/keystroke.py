#STL
from tqdm import tqdm

# Vendor
import pandas as pd

# Custom
from util import read_tsv, write_tsv
from util import read_json
from util import CRULP_MAPPTING,WINDOWS_MAPPING


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
    for i in tqdm(range(len(native)), desc="Transforming to Keystrokes"):
        transformed_line = ''
        for char in native[i]:
            transformed_line = transformed_line + mapping[char]
        transformed.append(transformed_line)
    return transformed


def transform_keystrokes(dataset_name):
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
    native,roman = read_tsv("interim/transformed/sentences/"+dataset_name)
    # transform for each keyboard layout
    transformed_CRULP = transform(native, CRULP_MAPPTING)
    transformed_Windows = transform(native, WINDOWS_MAPPING)
    # write results
    write_tsv(transformed_CRULP,roman,"interim/transformed/keystroke_CRULP/"+dataset_name)
    write_tsv(transformed_Windows,roman,"interim/transformed/keystroke_Windows/"+dataset_name)


##################
##     MAIN     ##
##################
def main():
    # Dataset: Dakshina
    print("Dataset: Dakshina".center(100, "="))
    transform_keystrokes("dakshina_dataset")
    # Dataset: Roman Urdu Parl
    print("Dataset: Roman Urdu Parl".center(100, "="))
    transform_keystrokes("roUrParl_dataset")
    # Dataset: Combined
    print("Dataset: Combined Subset".center(100, "="))
    transform_keystrokes("combined_subset")

if __name__ == "__main__":
    main()
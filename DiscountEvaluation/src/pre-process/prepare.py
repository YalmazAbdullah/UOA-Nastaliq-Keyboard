# STL
import re
from tqdm import tqdm

# Custom
from util import eval
from util import write_tsv

def prep_roman_ur_parl(native_file_path, roman_file_path):
    '''
    Formats the Roman Urdu Parallel dataset in the same format as Dakshina headless tsv. Prints out
    the number of tokens in the raw file, the number of tokens after pre-processing, and the loss
    ratio.
    
    Args:
        native_file_path (string): path to native file.
        roman_file_path (string): path to roman file.
    '''
    # read data
    file = open(native_file_path)
    native_data = file.readlines()
    file = open(roman_file_path)
    roman_data = file.readlines()

    # prepare output
    native_out = []
    roman_out = []

    # prepare measures to calculate loss
    raw_count = 0
    valid_count = 0

    # check if line counts match
    if (len(native_data) != len(roman_data)):
        print("Warning: datasets do not match.")

    # re formant the data
    for i in tqdm(range(len(native_data)),desc="Preparing Roman-Ur-Parl"):
        # standardize spaces
        native_data[i] =   re.sub(r'\s+', ' ', native_data[i])
        
        # tokenize
        native_tokens = native_data[i].split()
        roman_tokens = roman_data[i].split()
        raw_count += len(native_tokens)                 # storing raw token count for loss calculation
        
        # check to ensure token count matches
        if(len(native_tokens) == len(roman_tokens)):
            # save in dakshina format
            native_out.extend(native_tokens)
            roman_out.extend(roman_tokens)
            native_out.append("</s>")
            roman_out.append("</s>")
            valid_count += len(native_tokens)           # storing count of valid tokens where both roman and 
                                                        # native match for loss calculation.
        else:
            print(i)
            print(native_data[i])
            print(roman_data[i])
            print()
    
    # write to headless .tsv
    write_tsv(native_out, roman_out, 'interim/prepared/roUrParl_dataset')
    # print loss evaluation
    print("="*100)
    eval(raw_count,valid_count)


##################
##     MAIN     ##
##################
def main(
        native_file_path = '../_raw/uncompressed/Roman-Urdu-Parl/Urdu.txt', 
        roman_file_path = '../_raw/uncompressed/Roman-Urdu-Parl/Roman-Urdu.txt'
    ):
    prep_roman_ur_parl(native_file_path, roman_file_path)

if __name__ == "__main__":
    main()
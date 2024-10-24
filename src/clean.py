# STL
import re
from pprint import pprint

# Vendor
from urduhack.preprocessing import remove_accents

# Custom
from util import eval
from util import read_tsv,output_tsv
from util import read_json


'''
Standardizes the input, only has substitution and addition.
No subtraction.
'''
def standardize(native, roman):
    # roman dakshina has these random tokens that well remove
    native = [s for s in native if s != '""""']
    roman = [s for s in roman if s != '""""']

    # The datasets contain a mix of ltr and rtl punctuations
    # It also contains charachters that are similar but not quite the same ex: - and –
    # We will be standardizing them using this table
    chars = {
        ";":"؛",
        ",":"،",
        ".":"۔",
        "?":"؟",
        "*":"٭",
        "“":'"',
        "“":'"',
        "‘‘":'"',
        "’’":'"',
        "‘":"'",
        "–":"-",
        "ى ":"ی",
        "ي":"ی",
    }
    pattern = re.compile('|'.join(re.escape(key) for key in chars.keys()))

    for i in range(len(native)):
        if (native[i]=="</s>"):
            continue

        # Remove diacritcs
        native[i] = remove_accents(native[i])

        # standardize punctuation
        native[i] = remove_accents(native[i])
        native[i] = pattern.sub(lambda match: chars[match.group(0)], native[i])

    for i in range(len(roman)): 
        if (roman[i]=="?me"):
            roman[i] = "me"
            roman[i+1] = "?"
            native[i+1] = "؟"

    return native,roman

def remove_missing(native, roman):
    native_cleaned = []
    roman_cleaned = []
    for i in range(len(roman)): 
        if (roman[i]=="?" and native[i]!="؟"):
            continue
        native_cleaned.append(native[i])
        roman_cleaned.append(roman[i])
    return native_cleaned,roman_cleaned

def is_inaccessible(token,set:set):
    for char in token:
        if char not in set:
            return True
    return False

def remove_inaccessible(native,roman):
    # get set of accessible charachters
    set_CRULP = set(read_json("keyboards/mappings/CRULP").keys())
    set_Windows = set(read_json("keyboards/mappings/Windows").keys())
    set_intersection = set_CRULP.intersection(set_Windows)

    print("Set of Excluded Charachters:")
    union = set_CRULP.union(set_Windows)
    print(union.difference(set_intersection))

    # prepare output
    native_accessible = []
    roman_accessible = []

    print("Inaccessible Tokens:")
    # for each token
    for i in range(len(native)):
        # check if all chars accessible
        if(native[i] != "</s>" and is_inaccessible(native[i],set_intersection)):
            # ignore if they are not
            print(native[i])
            continue
        # add to ouput if they are
        native_accessible.append(native[i])
        roman_accessible.append(roman[i])
    return native_accessible,roman_accessible

'''
Main
'''
def main():
    print("Dataset: Dakshina")
    native,roman = read_tsv("prepared/dakshina_dataset")
    native,roman = standardize(native,roman)
    native_cleaned,roman_cleaned = remove_missing(native,roman)
    native_cleaned,roman_cleaned = remove_inaccessible(native_cleaned,roman_cleaned)

    eval(len(native),len(native_cleaned))
    output_tsv(native_cleaned,roman_cleaned,"cleaned/dakshina_dataset")

    print("Dataset: Roman Urdu Parl")
    native,roman = read_tsv("prepared/roUrParl_dataset")
    native,roman = standardize(native,roman)
    native_cleaned,roman_cleaned = remove_missing(native,roman)
    native_cleaned,roman_cleaned = remove_inaccessible(native_cleaned,roman_cleaned)
    
    eval(len(native),len(native_cleaned))
    output_tsv(native_cleaned,roman_cleaned,"cleaned/roUrParl_dataset")

if __name__ == "__main__":
    main()
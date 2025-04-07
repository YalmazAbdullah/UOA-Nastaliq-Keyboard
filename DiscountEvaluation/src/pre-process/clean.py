# STL
import re
from pprint import pprint
from tqdm import tqdm

# Vendor
from urduhack import preprocessing
from urduhack import normalization

# Custom
from util import eval
from util import read_tsv,write_tsv
from util import read_json


STANDARD_SUBSTITUTIONS = {
    # Punctuation and special
    ";":"؛", ",":"،", ".":"۔",
    "?":"؟", "*":"٭", "“":'"',
    "”":'"', "‘‘":'"', "’’":'"',
    "‘":"'", "’":"'", "–":"-",
    "٬":"،","…":"...",

    # # Same but different
    # "ى ":"ی",
    # "ي":"ی",
    # "ى":"ی",
    # "ه":"ہ",
    # "ك":"ک"
}


def standardize(native, roman):
    '''
    Standardizes the data. All diacritics are removed from the text. The data contains a mix of ltr and rtl punctuation. Ltr punc in urdu with the proper rtl punctuation. The numerals are also not accessible on all keyboard so we replace all urdu numerals with  regular numbers. Lastly there are some chars like ى which have mixed urdu arabic encoding. Replaces these to follow the same encoding.
    
    This function only does substitution and addition. No subtraction.

    Args:
        native (list): list holding urdu tokens
        roman (list): list holding roman tokens
    Returns:
        native (list): list holding urdu tokens 
        roman (list): list holding roman tokens
    '''
    
    pattern = re.compile('|'.join(re.escape(key) for key in STANDARD_SUBSTITUTIONS.keys()))

    # process urdu text
    for i in tqdm(range(len(native)), desc="Standardizing Tokens"):
        if (native[i]=="</s>"):
            continue

        # Remove diacritcs
        native[i] = preprocessing.remove_accents(native[i])
        native[i] = preprocessing.normalize_whitespace(native[i])
        native[i] = normalization.normalize_characters(native[i])
        native[i] = pattern.sub(lambda match: STANDARD_SUBSTITUTIONS[match.group(0)], native[i])
    return native,roman


def remove_missing(native, roman):
    '''
    Dakshina format uses ? for tokens that have no romanization. We will remove these pairs.

    Args:
        native (list): list holding urdu tokens
        roman (list): list holding roman tokens
    Returns:
        native (list): list holding urdu tokens 
        roman (list): list holding roman tokens
    '''
    native_cleaned = []
    roman_cleaned = []
    print("Tokens Removed Because Missing (?)")
    for i in tqdm(range(len(roman)), desc="Removing tokens with ?"): 
        if (roman[i]=="?" and native[i]!="؟"):
            print(native[i]+ "||" +roman[i])
            continue
        native_cleaned.append(native[i])
        roman_cleaned.append(roman[i])
    return native_cleaned,roman_cleaned


def _is_inaccessible(token, char_set):
    for char in token:
        if char not in char_set:
            return char
    return False


def remove_inaccessible(a_text,b_text,char_set):
    '''
    Remove any token that is not fully accessible to all keyboards

    Args:
        a_text (list): list holding tokens. Urdu or roman either is fine but urdu prefered.
        b_text (list): list holding tokens. Roman or roman either is fine but roman prefered.
        set (set): set of accessible tokens
    Returns:
        a_text (list): list holding tokens. 
        b_text (list): list holding tokens.
    '''
    # prepare output
    a_accessible = []
    b_accessible = []
    inaccessible_tokens = []
    freq = {}
    # for each token
    for i in tqdm(range(len(a_text)),desc="Removing Inaccessible"):
        # check if all chars accessible
        val = _is_inaccessible(a_text[i],char_set)
        if(a_text[i] != "</s>" and val):
            # add to list of inaccessible tokens
            freq[val] = freq.get(val,0) + 1
            inaccessible_tokens.append(a_text[i])
            continue
        # add to ouput if they are
        a_accessible.append(a_text[i])
        b_accessible.append(b_text[i])

    # build frequency table of inaccessible charachters
    removal_freq = {}
    inaccessible_token_set = set()
    for token in inaccessible_tokens:
        inaccessible_token_set.add(token)
        for char in token:
            if (char not in char_set):
                removal_freq[char] = removal_freq.get(char,0)+1

    # print out some info for error analysis
    print("Inaccessible Char Frequency Table".center(100, "-"))
    pprint(freq)
    print("Removed Char Frequency Table".center(100, "-"))
    pprint(removal_freq)
    print("Inaccessible Tokens:".center(100, "-"))
    pprint(inaccessible_token_set)
    print()

    return a_accessible,b_accessible


def clean(name,path,native_set,roman_set):
    """
    Cleans the provided data by standardizing coding variances, removing inaccessible charachters, and removing tokens with missing romanziations. The results are writtend to disk as tsv
    
    Args:
        name (str): name of the dataset being processed used when saving
        path (str): location of dirty dataset
        native_set (set): a set of universally accessible charachters
        roman_set (set): a set of roman charachters
    """
    # read file
    native,roman = read_tsv(path)
    # standardize the text by replacing or adding certain chars
    native,roman = standardize(native,roman)
    # remove tokens that have no equivilent roman token
    native_cleaned,roman_cleaned = remove_missing(native,roman)
    # remove tokens that have charachters that are not accessible
    print("Native".center(100, "/"))
    native_cleaned,roman_cleaned = remove_inaccessible(native_cleaned,roman_cleaned,native_set)
    print("Roman".center(100, "/"))
    roman_cleaned,native_cleaned = remove_inaccessible(roman_cleaned,native_cleaned,roman_set)

    eval(len(native),len(native_cleaned))
    write_tsv(native_cleaned,roman_cleaned,"interim/cleaned/"+name)


##################
##     MAIN     ##
##################
def main():
    # get set of accessible charachters
    roman_set = set(read_json("keyboards/QWERTY")["Charachters"])
    CRULP_set = set(read_json("keyboards/mappings/CRULP").keys())
    Windows_set = set(read_json("keyboards/mappings/Windows").keys())
    native_set = CRULP_set.intersection(Windows_set)

    # print set of inaccessible charachters for rigour
    union = CRULP_set.union(Windows_set)
    print("Set of Excluded Native Charachters:")
    print(union.difference(native_set))

    # clean the data
    dakshina_path = "raw/uncompressed/Dakshina/ur.romanized.rejoined.aligned"
    roman_path = "interim/prepared/roUrParl_dataset"
    print("Dataset: Dakshina".center(100, "="))
    clean("dakshina_dataset",dakshina_path,native_set,roman_set)
    print("Dataset: Roman Urdu Parl".center(100, "="))
    clean("roUrParl_dataset",roman_path,native_set,roman_set)

if __name__ == "__main__":
    main()
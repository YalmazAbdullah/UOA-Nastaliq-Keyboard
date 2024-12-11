# STL
import re
from pprint import pprint

# Vendor
from urduhack.preprocessing import remove_accents

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

    # Numerals
    "۱":"1", "۲":"2", "۳":"3",
    "۴":"4", "۵":"5", "۶":"6", 
    "۷":"7", "۸":"8", "۹":"9", 
    "۰":"0",

    # Same but different
    "ى ":"ی",
    "ي":"ی",
    "ى":"ی",
    "ه":"ہ",
    "ك":"ک"
}

def standardize(native, roman):
    '''
    Standardizes the data. All diacritics are removed from the text.
    The data contains a mix of ltr and rtl punctuation. Ltr punc in urdu with 
    the proper rtl punctuation. The numerals
    are also not accessible on all keyboard so we replace all urdu numerals with 
    regular numbers. Lastly there are some chars like ى which have mixed urdu arabic
    encoding. Replaces these to follow the same encoding.
    
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
    for i in range(len(native)):
        if (native[i]=="</s>"):
            continue

        # Remove diacritcs
        native[i] = remove_accents(native[i])

        # standardize punctuation
        native[i] = remove_accents(native[i])
        native[i] = pattern.sub(lambda match: STANDARD_SUBSTITUTIONS[match.group(0)], native[i])

    # process roman text
    for i in range(len(roman)): 
        if (roman[i]=="?me"):
            roman[i] = "me"
            roman[i+1] = "?"
            native[i+1] = "؟"

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
    for i in range(len(roman)): 
        if (roman[i]=="?" and native[i]!="؟"):
            continue
        native_cleaned.append(native[i])
        roman_cleaned.append(roman[i])
    return native_cleaned,roman_cleaned

g_inaccessable_chars = set()
def is_inaccessible(token, char_set):
    '''
    Checks to see if all charachters in token are accessabile to the keyboards.
    
    Args:
        token (string): token that is being checked
        char_set (set): char_set of accessible tokens
    '''
    for char in token:
        if char not in char_set:
            g_inaccessable_chars.add(char)
            return True
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
    # for each token
    for i in range(len(a_text)):
        # check if all chars accessible
        if(a_text[i] != "</s>" and is_inaccessible(a_text[i],char_set)):
            # add to list of inaccessible tokens
            inaccessible_tokens.append(a_text[i])
            continue
        # add to ouput if they are
        a_accessible.append(a_text[i])
        b_accessible.append(b_text[i])

    # build frequency table of inaccessible charachters
    freq = {}
    inaccessible_token_set = set()
    for token in inaccessible_tokens:
        inaccessible_token_set.add(token)
        for char in token:
            if (char not in char_set):
                freq[char] = freq.get(char,0)+1

    # print out some info for error analysis
    print("Inaccessible char frequency table")
    pprint(freq)
    print("Inaccessible Tokens:")
    pprint(inaccessible_token_set)
    print()

    return a_accessible,b_accessible


def clean(name,path,native_set,roman_set):
    # read file
    native,roman = read_tsv(path)
    # standardize the text by replacing or adding certain chars
    native,roman = standardize(native,roman)
    # remove tokens that have no equivilent roman token
    native_cleaned,roman_cleaned = remove_missing(native,roman)
    # remove tokens that have charachters that are not accessible
    native_cleaned,roman_cleaned = remove_inaccessible(native_cleaned,roman_cleaned,native_set)
    roman_cleaned,native_cleaned = remove_inaccessible(roman_cleaned,native_cleaned,roman_set)

    eval(len(native),len(native_cleaned))
    write_tsv(native_cleaned,roman_cleaned,"cleaned/"+name)


##################
##     MAIN     ##
##################
def main():
    print("###############################################")
    print("=====================CLEAN=====================")
    print("###############################################")
    print()

    # get set of accessible charachters
    set_CRULP = set(read_json("keyboards/mappings/CRULP").keys())
    set_Windows = set(read_json("keyboards/mappings/Windows").keys())
    native_set = set_CRULP.intersection(set_Windows)
    roman_set = set(read_json("keyboards/QWERTY")["Charachters"])

    print("Set of Excluded Native Charachters:")
    union = set_CRULP.union(set_Windows)
    print(union.difference(native_set))

    # clean the data
    print("=============Dataset: Dakshina=============")
    clean("dakshina_dataset","raw/uncompressed/Dakshina/ur.romanized.rejoined.aligned",native_set,roman_set)
    print("=============Dataset: Roman Urdu Parl=============")
    clean("roUrParl_dataset","prepared/roUrParl_dataset",native_set,roman_set)

    print("Set of Unintentionally Exluded")
    print(g_inaccessable_chars.difference(union.difference(native_set)))

if __name__ == "__main__":
    main()
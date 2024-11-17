# STL
import re
from pprint import pprint

# Vendor
from urduhack.preprocessing import remove_accents

# Custom
from util import eval
from util import read_tsv,write_tsv
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
        "”":'"',
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

'''
Dakshina format uses ? for tokens that have no romanization. We will remove these pairs
'''
def remove_missing(native, roman):
    native_cleaned = []
    roman_cleaned = []
    for i in range(len(roman)): 
        if (roman[i]=="?" and native[i]!="؟"):
            continue
        native_cleaned.append(native[i])
        roman_cleaned.append(roman[i])
    return native_cleaned,roman_cleaned

'''
Checks to see if all charachters in token are accessabile to the keyboards
'''
def is_inaccessible(token,set:set):
    for char in token:
        if char not in set:
            return True
    return False

'''
Remove any token that is not fully accessible to all keyboards
'''
def remove_inaccessible(a_text,b_text,set):
    # prepare output
    a_accessible = []
    b_accessible = []
    inaccessible_tokens = []
    print("Inaccessible Tokens:")
    # for each token
    for i in range(len(a_text)):
        # check if all chars accessible
        if(a_text[i] != "</s>" and is_inaccessible(a_text[i],set)):
            # ignore if they are not
            inaccessible_tokens.append(a_text[i])
            print(a_text[i])
            continue
        # add to ouput if they are
        a_accessible.append(a_text[i])
        b_accessible.append(b_text[i])

    # print out frequency of inaccessible charachters
    freq = {}
    for token in inaccessible_tokens:
        for char in token:
            if (char not in set):
                freq[char] = freq.get(char,0)+1

    print("Inaccessible frequency table")
    pprint(freq)
    return a_accessible,b_accessible

'''
Main
'''
def main():
    # get set of accessible charachters
    set_CRULP = set(read_json("keyboards/mappings/CRULP").keys())
    set_Windows = set(read_json("keyboards/mappings/Windows").keys())
    native_set = set_CRULP.intersection(set_Windows)
    roman_set = set(read_json("keyboards/QWERTY")["Mapping"].keys())

    print("Set of Excluded Native Charachters:")
    union = set_CRULP.union(set_Windows)
    print(union.difference(native_set))

    print("=============Dataset: Dakshina=============")
    native,roman = read_tsv("raw/uncompressed/Dakshina/ur.romanized.rejoined.aligned")
    native,roman = standardize(native,roman)
    native_cleaned,roman_cleaned = remove_missing(native,roman)
    native_cleaned,roman_cleaned = remove_inaccessible(native_cleaned,roman_cleaned,native_set)
    roman_cleaned,native_cleaned = remove_inaccessible(roman_cleaned,native_cleaned,roman_set)

    eval(len(native),len(native_cleaned))
    write_tsv(native_cleaned,roman_cleaned,"cleaned/dakshina_dataset")

    print("=============Dataset: Roman Urdu Parl=============")
    native,roman = read_tsv("prepared/roUrParl_dataset")
    native,roman = standardize(native,roman)
    native_cleaned,roman_cleaned = remove_missing(native,roman)
    native_cleaned,roman_cleaned = remove_inaccessible(native_cleaned,roman_cleaned,native_set)
    roman_cleaned,native_cleaned = remove_inaccessible(roman_cleaned,native_cleaned,roman_set)
    
    eval(len(native),len(native_cleaned))
    write_tsv(native_cleaned,roman_cleaned,"cleaned/roUrParl_dataset")

if __name__ == "__main__":
    main()
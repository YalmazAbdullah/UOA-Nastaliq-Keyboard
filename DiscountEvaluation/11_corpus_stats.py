# STL
import math
from statistics import median

# CUSTOM
from util import read_tsv


def get_stats(data):
    '''
    Gets the summary stats for roman-urdu-parl
    NOTE: The token count for dakshina post cleaning is incorrect. That does not neccessarily follow the space based tokenizing format we need to do some other way of counting.
    '''
    lines = len(data)
    tokens = 0
    characters = 0
    counts = []
    
    min_chars = math.inf
    max_chars = -1
    for line in data:
        line = line.strip()
        tokenized = line.split()
        tokens += len(tokenized)

        length = len(line)
        characters += length
        counts.append(length)
        min_chars = min(min_chars, length)
        max_chars = max(max_chars, length)

    mean_characters = float(characters)/lines
    median_characters = median(counts)
    print("Number of Lines:", lines)
    print("Number of Tokens:", tokens)
    print("Number of Characters:", characters)
    print("Mean Characters per Line:", mean_characters)
    print("Median Characters per Line:", median_characters)
    print("Min Characters per Line:", min_chars)
    print("Max Characters per Line:", max_chars)

def get_stats2(data):
    '''
    Gets the summary stats for dakshina
    '''
    lines = 0
    total_characters  = 0
    total_tokens  = 0
    chars_in_line  = 0
    tokens_in_line = 0
    counts = []
    
    min_chars = math.inf
    max_chars = -1
    for token in data:
        if(token == "</s>"):
            lines +=1
            min_chars = min(min_chars, chars_in_line)
            max_chars = max(max_chars, chars_in_line)
            counts.append(chars_in_line)
            tokens_in_line = 0
            chars_in_line = 0
        else:
            total_tokens +=1
            tokens_in_line+=1
            total_characters += len(token)
            chars_in_line += len(token)
    mean_charachters = float(total_characters)/lines
    median_charachters = median(counts)
    
    print ("Number of Lines: ", lines)
    print ("Number of Tokens: ", total_tokens)
    print ("Number of Charachters: ", total_characters)
    print ("Mean Charachters per Line: ", mean_charachters)
    print ("Median Charachters per Line: ", median_charachters)
    print ("Min Charachters per Line: ", min)
    print ("Max Charachters per Line: ", max)

##################
##     MAIN     ##
##################
def main():
    print("#"*100)
    print("RAW Stats".center(100, "+"))
    print("#"*100)
    
    print("Dataset: Dakshina".center(100, "="))
    native, roman = read_tsv("Data_Discount/raw/Dakshina/ur.romanized.rejoined.aligned")
    print("Urdu".center(100, "-"))
    get_stats2(native)
    print("Roman".center(100, "-"))
    get_stats2(roman)
    print()

    print("Dataset: Roman Urdu Parl".center(100, "="))
    print("Urdu".center(100, "-"))
    file = open('../Data_Discount/raw/Roman-Urdu-Parl/Urdu.txt')
    data = file.readlines()
    get_stats(data)
    print("Roman".center(100, "-"))
    file = open('../Data_Discount/raw/Roman-Urdu-Parl/Roman-Urdu.txt')
    data = file.readlines()
    get_stats(data)


    print("#"*100)
    print("PROCESSED Stats".center(100, "+"))
    print("#"*100)

    print("Dataset: Dakshina".center(100, "="))
    native, roman = read_tsv("Data_Discount/transformed_sentences/dakshina_dataset")
    print("Urdu".center(100, "-"))
    get_stats(native)
    print("Roman".center(100, "-"))
    get_stats(roman)
    
    print("Dataset: Roman Urdu Parl".center(100, "="))
    native, roman = read_tsv("Data_Discount/transformed_sentences/roUrParl_dataset")
    print("Urdu".center(100, "-"))
    get_stats(native)
    print("Roman".center(100, "-"))
    get_stats(roman)
    
    
    print("Dataset: Combined Subset".center(100, "="))
    native, roman = read_tsv("Data_Discount/transformed_sentences/combined_subset")
    print("Urdu".center(100, "-"))
    get_stats(native)
    print("Roman".center(100, "-"))
    get_stats(roman)
    
if __name__ == "__main__":
    main()
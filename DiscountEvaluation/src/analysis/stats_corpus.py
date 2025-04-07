from util import read_tsv
import math
from statistics import median

def get_stats(data):
    '''
    Gets the summary stats for roman-urdu-parl
    '''
    lines = len(data)
    tokens = 0
    min = math.inf
    max = -1
    counts = []
    for line in data:
        tokenized = line.split()
        tokens += len(tokenized)
        counts.append(len(tokenized))
        if (min>len(tokenized)):
            min=len(tokenized)
        if(max<len(tokenized)):
            max=len(tokenized)
    mean_tokens = float(tokens)/lines
    median_tokens = median(counts)
    print ("Number of Lines: ", lines)
    print ("Number of Tokens: ", tokens)
    print ("Mean Tokens per Line: ", mean_tokens)
    print ("Median Tokens per Line: ", median_tokens)
    print ("Min Tokens per Line: ", min)
    print ("Max Tokens per Line: ", max)

def get_stats2(data):
    '''
    Gets the summary stats for dakshina
    '''
    lines = 0
    tokens = 0
    tokens_in_line = 0
    min = math.inf
    max = -1
    counts = []
    for token in data:
        if(token == "</s>"):
            if (min>tokens_in_line):
                min=tokens_in_line
            if(max<tokens_in_line):
                max=tokens_in_line
            lines +=1
            counts.append(tokens_in_line)
            tokens_in_line = 0
        else:
            tokens +=1
            tokens_in_line+=1
    mean_tokens = float(tokens)/lines
    median_tokens = median(counts)
    
    print ("Number of Lines: ", lines)
    print ("Number of Tokens: ", tokens)
    print ("Mean Tokens per Line: ", mean_tokens)
    print ("Median Tokens per Line: ", median_tokens)
    print ("Min Tokens per Line: ", min)
    print ("Max Tokens per Line: ", max)

##################
##     MAIN     ##
##################
def main():
    print("#"*100)
    print("RAW Stats".center(100, "+"))
    print("#"*100)
    
    print("Dataset: Dakshina".center(100, "="))
    native, roman = read_tsv("raw/uncompressed/Dakshina/ur.romanized.rejoined.aligned")
    print("Urdu".center(100, "-"))
    get_stats2(native)
    print("Roman".center(100, "-"))
    get_stats2(roman)
    print()

    print("Dataset: Roman Urdu Parl".center(100, "="))
    print("Urdu".center(100, "-"))
    file = open('../raw/uncompressed/Roman-Urdu-Parl/Urdu.txt')
    data = file.readlines()
    get_stats(data)
    print("Roman".center(100, "-"))
    file = open('../raw/uncompressed/Roman-Urdu-Parl/Roman-Urdu.txt')
    data = file.readlines()
    get_stats(data)


    print("#"*100)
    print("PROCESSED Stats".center(100, "+"))
    print("#"*100)

    print("Dataset: Dakshina".center(100, "="))
    native, roman = read_tsv("interim/transformed/sentences/dakshina_dataset")
    print("Urdu".center(100, "-"))
    get_stats(native)
    print("Roman".center(100, "-"))
    get_stats(roman)
    
    print("Dataset: Roman Urdu Parl".center(100, "="))
    native, roman = read_tsv("interim/transformed/sentences/roUrParl_dataset")
    print("Urdu".center(100, "-"))
    get_stats(native)
    print("Roman".center(100, "-"))
    get_stats(roman)
    
    
    print("Dataset: Combined Subset".center(100, "="))
    native, roman = read_tsv("interim/transformed/sentences/combined_subset")
    print("Urdu".center(100, "-"))
    get_stats(native)
    print("Roman".center(100, "-"))
    get_stats(roman)
    
if __name__ == "__main__":
    main()
from util import read_tsv
import math
from statistics import median

'''
Gets the summary stats for roman-urdu-parl
'''
def get_stats(data):
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

'''
Gets the summary stats for dakshina
'''
def get_stats2(data):
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
    print("###############################################")
    print("===================RAW STATS===================")
    print("###############################################")
    print("=============Dataset: Roman Urdu Parl=============")
    print("-------------Urdu-------------")
    file = open('./DiscountEvaluation/corpus/raw/uncompressed/Roman-Urdu-Parl/Urdu.txt')
    data = file.readlines()
    get_stats(data)
    print("-------------Roman-------------")
    file = open('./DiscountEvaluation/corpus/raw/uncompressed/Roman-Urdu-Parl/Roman-Urdu.txt')
    data = file.readlines()
    get_stats(data)
    print("=============Dataset: Dakshina=============")
    native, roman = read_tsv("raw/uncompressed/Dakshina/ur.romanized.rejoined.aligned")
    print("-------------Urdu-------------")
    get_stats2(native)
    print("-------------Roman-------------")
    get_stats2(roman)
    print()


    print("###############################################")
    print("================PROCESSED STATS================")
    print("###############################################")
    print("=============Dataset: Roman Urdu Parl=============")
    native, roman = read_tsv("transformed/sentences/roUrParl_dataset")
    print("-------------Urdu-------------")
    get_stats(native)
    print("-------------Roman-------------")
    get_stats(roman)
    print("=============Dataset: Dakshina=============")
    native, roman = read_tsv("transformed/sentences/dakshina_dataset")
    print("-------------Urdu-------------")
    get_stats(native)
    print("-------------Roman-------------")
    get_stats(roman)
    
if __name__ == "__main__":
    main()
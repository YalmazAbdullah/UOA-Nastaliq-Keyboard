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
    charahcters = 0
    min = math.inf
    max = -1
    counts = []
    for line in data:
        charahcters += len(line)
        counts.append(len(line))
        if (min>len(line)):
            min=len(line)
        if(max<len(line)):
            max=len(line)
    mean_charachters = float(charahcters)/lines
    median_charachters = median(counts)
    print ("Number of Lines: ", lines)
    print ("Number of Charachters: ", charahcters)
    print ("Mean Charachters per Line: ", mean_charachters)
    print ("Median Charachters per Line: ", median_charachters)
    print ("Min Charachters per Line: ", min)
    print ("Max Charachters per Line: ", max)

def get_stats2(data):
    '''
    Gets the summary stats for dakshina
    '''
    lines = 0
    charachters = 0
    charachters_in_line = 0
    min = math.inf
    max = -1
    counts = []
    for token in data:
        if(token == "</s>"):
            if (min>charachters_in_line):
                min=charachters_in_line
            if(max<charachters_in_line):
                max=charachters_in_line
            lines +=1
            counts.append(charachters_in_line)
            charachters_in_line = 0
        else:
            charachters += len(token)
            charachters_in_line += len(token)
    mean_charachters = float(charachters)/lines
    median_charachters = median(counts)
    
    print ("Number of Lines: ", lines)
    print ("Number of Charachters: ", charachters)
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
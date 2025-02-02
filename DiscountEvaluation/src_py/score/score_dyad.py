# STL
from itertools import product

# VENDOR
import pandas as pd

# CUSTOM
from transform_dyad import transform
from util import CHAR_SET
from util import evaluate_dyad

def score(dataset_name):
    '''
    Score the dyads for the dataset by caculating travel distance, frequency
    and checking if same finger, same key, same hand, reach, and hurdle. Results
    are saved to output csv.

    Args:
        dataset_name (string): name of dataset
    Returns:
        None
    '''
    # generate all possible dyads
    dyad_data = pd.DataFrame()
    two_char_permutations = list(product(CHAR_SET, repeat=2))
    permutation_strings = [''.join(p) for p in two_char_permutations]
    
    # handle all dyad permutations
    for dyad in permutation_strings:
       results = evaluate_dyad(dyad[0],dyad[1])
       dyad_data = pd.concat([dyad_data, pd.DataFrame([results])], ignore_index=True)

    # handle special start and end cases:
    for char in CHAR_SET:
        markers = ["<s>","</s>"]
        for i in range(len(markers)):
            mark = markers[i]
            if(i==0):
                results = evaluate_dyad(mark,char)
                dyad_data = pd.concat([dyad_data, pd.DataFrame([results])], ignore_index=True)
            else:
                results = evaluate_dyad(char,mark)
                dyad_data = pd.concat([dyad_data, pd.DataFrame([results])], ignore_index=True)
    dyad_data = dyad_data.set_index("dyad")

    # Retrive data for each keyboard dyad frequency counting
    crulp,windows,roman = transform(dataset_name)
    data_sets = {"CRULP":crulp,"WINDOWS":windows,"IME":roman}

    output = pd.DataFrame()
    
    # tally frequency of dyad
    for keyboard in data_sets.keys():
        dyad_counts = {key: 0 for key in dyad_data.index.tolist()}
        data_set = data_sets[keyboard]
        for sentence in data_set:
            for i in range(len(sentence)):
                dyad = sentence[i]
                dyad_counts[dyad] +=1
        count_data = pd.DataFrame.from_dict(dyad_counts, orient="index", columns=["Frequency"])
        combined = pd.concat([dyad_data,count_data], axis= 1)
        combined["Keyboard"] = keyboard
        output = pd.concat([output,combined])
    
    # write results
    output.to_csv("./DiscountEvaluation/data/dyad/"+dataset_name+".csv", index=True)

##################
##     MAIN     ##
##################
def main():
    print("Dyad")
    # score("dakshina_dataset")
    # score("roUrParl_dataset")
    score("combined_dataset")

if __name__ == "__main__":
    main()
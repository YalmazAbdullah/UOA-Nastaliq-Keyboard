#STL
from tqdm import tqdm

# VENDOR
import pandas as pd

# CUSTOM
from util import evaluate_dyad
from util import read_tsv

def score_sentence(sentence):
    # ignore white space we dotn consider it when calculating distance
    sentence = sentence.replace(" ", "")
    # handle start of sentence
    sentence_total = evaluate_dyad("<s>",sentence[0])
    # make sure to add sentnece index
    for i in range(len(sentence)-1):
        result = evaluate_dyad(sentence[i],sentence[i+1])
        sentence_total = {key: sentence_total[key]+ result[key] for key in result}
    # handle end of sentence
    result = evaluate_dyad(sentence[len(sentence)-1],"</s>")
    sentence_total = {key: sentence_total[key]+ result[key] for key in result}
    sentence_total["StrokeCount"] = len(sentence)
    del sentence_total["dyad"]
    return sentence_total

def score(dataset_name):
    _,roman = read_tsv("interim/transformed/keystroke_CRULP/"+dataset_name)
    
    # calculate sentence scores
    inputs = {
        "CRULP":read_tsv("interim/transformed/keystroke_CRULP/"+dataset_name)[0],
        "IME":roman,
        "WINDOWS":read_tsv("interim/transformed/keystroke_Windows/"+dataset_name)[0],
    }

    # Score each sentence
    output = pd.DataFrame()
    for keyboard in inputs:
        full_results = []
        for i in tqdm(range(len(roman))):
            # for each keyboard 
            result = score_sentence(inputs[keyboard][i])
            result["ID"] = i
            result["Keyboard"] = keyboard
            full_results.append(result)
        output = pd.concat([output, pd.DataFrame(full_results)], ignore_index=True)
    
    # Write results
    output.to_csv("../data/sentence/score/"+dataset_name+".csv", index=True)

##################
##     MAIN     ##
##################
def main():
    print("Dataset: Dakshina".center(100, "="))
    score("dakshina_dataset")
    print("Dataset: Roman Urdu Parl".center(100, "="))
    score("roUrParl_dataset")
    print("Dataset: Combined Subset".center(100, "="))
    score("combined_subset")

if __name__ == "__main__":
    main()
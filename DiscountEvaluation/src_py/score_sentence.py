#STL
from tqdm import tqdm

# VENDOR
import pandas as pd

# CUSTOM
from transform_keystroke import transform
from util import evaluate_dyad
from util import read_tsv
from util import CRULP_MAPPTING, WINDOWS_MAPPING
import pprint
def score_sentence(sentence):
    # handle start of sentence
    sentence_total = evaluate_dyad("<s>",sentence[0])
    # make sure to add sentnece index
    for i in range(len(sentence)-1):
        result = evaluate_dyad(sentence[i],sentence[i+1])
        sentence_total = {key: sentence_total[key]+ result[key] for key in result}
    # handle end of sentence
    result = evaluate_dyad(sentence[len(sentence)-1],"</s>")
    sentence_total = {key: sentence_total[key]+ result[key] for key in result}
    del sentence_total["dyad"]
    return sentence_total

def score(dataset_name):
    native,roman = read_tsv("transformed/sentences/"+dataset_name)
    # calculate sentence scores
    inputs = {
        "CRULP":transform(native, CRULP_MAPPTING),
        "IME":roman,
        "WINDOWS":transform(native, WINDOWS_MAPPING),
    }

    # Score each sentence
    output = pd.DataFrame()
    for i in tqdm(range(len(roman))):
        # for each keyboard 
        for keyboard in inputs:
            result = score_sentence(inputs[keyboard][i])
            result["ID"] = i
            result["Keyboard"] = keyboard
            output = pd.concat([output, pd.DataFrame([result])], ignore_index=True)
    
    # Write results
    output.to_csv("./DiscountEvaluation/output/sentence/score/"+dataset_name+".csv", index=True)

##################
##     MAIN     ##
##################
def main():
    score("dakshina_dataset")
    score("roUrParl_dataset")

if __name__ == "__main__":
    main()
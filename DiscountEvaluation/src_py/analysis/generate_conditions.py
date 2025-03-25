# from data 
# calculate hurdles and reaches etc.
# find subset with roughly equal 

# read csv for dak and rourparl

import pandas as pd
from util import read_tsv


def select_similar_rows(group):
    if len(group) <= 10:
        return group  # If less than 10 rows, return all

    # Compute local median within the group
    median_hurdle = group["Hurdle"].median()
    median_reach = group["Reach"].median()

    # Calculate absolute difference from group median
    group["hurdle_diff"] = abs(group["Hurdle"] - median_hurdle)
    group["reach_diff"] = abs(group["Reach"] - median_reach)

    # Sort by closeness to group median
    group = group.sort_values(by=["hurdle_diff", "reach_diff"])

    # Select up to 10 rows closest to the group's median
    return group.head(10).drop(columns=["hurdle_diff", "reach_diff"])

def main():
    dataset_name = "dakshina_dataset"
    scores = pd.read_csv("../data/sentence/score/"+dataset_name+".csv")
    urdu,_ = read_tsv("transformed/keystroke_CRULP/"+dataset_name)

    global_median_hurdle = scores["Hurdle"].median()
    global_median_reach = scores["Reach"].median()
    
    print(global_median_hurdle)
    print(global_median_reach)
    # filter out IDs that are beyond tolerance
    # filter out IDs that are 
    print(scores["ID"])

if __name__ == "__main__":
    main()
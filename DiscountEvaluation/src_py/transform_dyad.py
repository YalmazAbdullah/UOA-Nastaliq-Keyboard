# Custom
from util import read_tsv,write_tsv
import json

def generate_dyads(text):
    transformed = []
    for line in text:
        line = line.replace(" ", "") 
        dyads = ["<s>"+line[0]]
        dyads = dyads + [line[i:i+2] for i in range(len(line) - 1)]
        dyads = dyads + [line[len(line) - 1] + "</s>"]
        transformed.append(dyads)
    return transformed

def write_dyads(native1,native2,roman,path):
    with open("./DiscountEvaluation/data/"+path+".json", "w") as file:
        json.dump([native1,native2,roman], file, indent=4)

def transform(dataset_name,write = False):
    crulp,roman = read_tsv("transformed/keystroke_CRULP/"+dataset_name)
    windows,roman = read_tsv("transformed/keystroke_Windows/"+dataset_name)
    roman_dyads = generate_dyads(roman)
    crulp_dyads = generate_dyads(crulp)
    windows_dyads = generate_dyads(windows)
    if(write):
        write_dyads(crulp_dyads,windows_dyads,roman_dyads,"transformed/dyads/"+dataset_name)
    return crulp_dyads,windows_dyads,roman_dyads

def main():
    transform("dakshina_dataset",True)
    transform("roUrParl_dataset",True)
    

if __name__ == "__main__":
    main()
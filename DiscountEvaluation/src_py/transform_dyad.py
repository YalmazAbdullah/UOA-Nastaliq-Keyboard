# Custom
from util import read_tsv,write_tsv
import json

def generate_dyads(text):
    transformed = []
    for line in text:
        line = line.replace(" ", "") 
        triads = [line[i:i+2] for i in range(len(line) - 2 + 1)]
        transformed.append(triads)
    return transformed

def write_triads(native1,native2,roman,path):
    with open("./DiscountEvaluation/data/"+path+".json", "w") as file:
        json.dump([native1,native2,roman], file, indent=4)

def transform(dataset_name):
    crulp,roman = read_tsv("transformed/keystroke_CRULP/"+dataset_name)
    windows,roman = read_tsv("transformed/keystroke_Windows/"+dataset_name)
    roman_dyads = generate_dyads(roman)
    crulp_dyads = generate_dyads(crulp)
    windows_dyads = generate_dyads(windows)
    write_triads(crulp_dyads,windows_dyads,roman_dyads,"transformed/dyads/"+dataset_name)
    return crulp_dyads,windows_dyads,roman_dyads

def main():
    transform("dakshina_dataset")
    transform("roUrParl_dataset")
    

if __name__ == "__main__":
    main()
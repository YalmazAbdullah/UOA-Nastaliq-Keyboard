# Custom
from util import read_tsv
import json

def generate_dyads(text):
    '''
    Takes a sentence, strips spaces and generates alll the dyads with overlap. Ex:
    Hello World
    HelloWorld
    He
     el
      ll
       oW
        Wr
         rl
          ld
    adds tm all to list and returns. Also adds dyad with start and end delimiter

    Args:
        text (string): sentence
    Returns:
        transformed (string): all dyads for the setnece in a list
    '''
    transformed = []
    for line in text:
        line = line.replace(" ", "") 
        dyads = ["<s>"+line[0]]
        dyads = dyads + [line[i:i+2] for i in range(len(line) - 1)]
        dyads = dyads + [line[len(line) - 1] + "</s>"]
        transformed.append(dyads)
    return transformed

def write_dyads(native1,native2,roman,path):
    '''
    dump the transformation results into a json file. Mostly for debuging purposes.
    
    Args:
        native1 (list): Results of first layout transformation
        native2 (list): Results of second layout transformation
        roman (list): Results of the roman keystrokes
        path (string): Path to save to

    Returns:
        None
    '''
    with open("./DiscountEvaluation/corpus/"+path+".json", "w") as file:
        json.dump([native1,native2,roman], file, indent=4)

def transform(dataset_name,write = False):
    '''
    Transform sentences into collection of dyads.

    Args:
        dataset_name (string): name of the dataset
        write (bool): we dont actually need to write all the time so this is for testing and stuff.
    
    Returns:
        crulp_dyads (list): list of lists which hold all dyads in sentence
        windows_dyads (list):  list of lists which hold all dyads in sentence
        roman_dyads (list):  list of lists which hold all dyads in sentence
    '''
    crulp,roman = read_tsv("transformed/keystroke_CRULP/"+dataset_name)
    windows,roman = read_tsv("transformed/keystroke_Windows/"+dataset_name)
    roman_dyads = generate_dyads(roman)
    crulp_dyads = generate_dyads(crulp)
    windows_dyads = generate_dyads(windows)
    if(write):
        write_dyads(crulp_dyads,windows_dyads,roman_dyads,"transformed/dyads/"+dataset_name)
    return crulp_dyads,windows_dyads,roman_dyads

##################
##     MAIN     ##
##################
def main():
    print("Dyad Transformation: dakshina")
    transform("dakshina_dataset",True)
    print("Dyad Transformation: roUrParl")
    transform("roUrParl_dataset",True)
    print("Dyad Transformation: combined")
    transform("combined_dataset",True)
    

if __name__ == "__main__":
    main()
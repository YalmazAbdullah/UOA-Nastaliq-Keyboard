# Vendor
import pandas as pd

# Custom
from util import read_tsv,write_tsv

def generate():
    native1,roman1 = read_tsv("interim/transformed/sentences/dakshina_dataset")
    native2,roman2 = read_tsv("interim/transformed/sentences/roUrParl_dataset")
    data1 = pd.DataFrame(
        {
            "U":native1,
            "R":roman1
        }
    )

    data2 = pd.DataFrame(
        {
            "U":native2,
            "R":roman2
        }
    )

    data1 = data1.sample(frac=1, random_state = 1)
    data2 = data2.sample(frac=1, random_state = 1)
    
    data1 = data1.sample(n=9000, random_state = 1)
    data2 = data2.sample(n=9000, random_state = 1)
    
    data3 = pd.concat([data1,data2], ignore_index=True)
    
    write_tsv(data3['U'].tolist(),data3['R'].tolist(),"interim/transformed/sentences/combined_subset")

def main():
    generate()

if __name__ == "__main__":
    main()
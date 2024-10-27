# Custom
from util import read_tsv,output_tsv

def transform(text):
    transformed = []
    for line in text:
        line = line.replace(" ", "") 
        triads = [line[i:i+3] for i in range(len(line) - 3 + 1)]
        transformed.append(triads)
    return transformed

def main():
    # Dataset: Dakshina
    crulp,roman = read_tsv("transformed/keystroke_CRULP/dakshina_dataset")
    windows,roman = read_tsv("transformed/keystroke_Windows/dakshina_dataset")
    roman_traids = transform(roman)
    crulp_triads = transform(crulp)
    windows_triads = transform(windows)
    output_tsv(crulp_triads,roman_traids,"transformed/triad_CRULP/dakshina_dataset")
    output_tsv(windows_triads,roman_traids,"transformed/triad_Windows/dakshina_dataset")

    # Dataset: Roman Urdu Parl
    crulp,roman = read_tsv("transformed/keystroke_CRULP/roUrParl_dataset")
    windows,roman = read_tsv("transformed/keystroke_Windows/roUrParl_dataset")
    roman_traids = transform(roman)
    crulp_triads = transform(crulp)
    windows_triads = transform(windows)
    output_tsv(crulp_triads,roman_traids,"transformed/triad_CRULP/roUrParl_dataset")
    output_tsv(windows_triads,roman_traids,"transformed/triad_Windows/roUrParl_dataset")    

if __name__ == "__main__":
    main()
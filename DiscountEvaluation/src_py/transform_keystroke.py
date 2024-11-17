# Custom
from util import read_tsv, write_tsv
from util import read_json

def transform(native, mapping_adress):
    mapping = read_json(mapping_adress)

    transformed = []
    for i in range(len(native)):
        transformed_line = ''
        for char in native[i]:
            transformed_line = transformed_line + mapping[char]
        transformed.append(transformed_line)
    return transformed


def main():
    # Dataset: Dakshina
    native,roman = read_tsv("transformed/sentences/dakshina_dataset")
    transformed_CRULP = transform(native,"keyboards/mappings/CRULP")
    transformed_Windows = transform(native,"keyboards/mappings/Windows")
    write_tsv(transformed_CRULP,roman,"transformed/keystroke_CRULP/dakshina_dataset")
    write_tsv(transformed_Windows,roman,"transformed/keystroke_Windows/dakshina_dataset")

    # # Dataset: Roman Urdu Parl
    native,roman = read_tsv("transformed/sentences/roUrParl_dataset")
    transformed_CRULP = transform(native,"keyboards/mappings/CRULP")
    transformed_Windows = transform(native,"keyboards/mappings/Windows")
    write_tsv(transformed_CRULP,roman,"transformed/keystroke_CRULP/roUrParl_dataset")
    write_tsv(transformed_Windows,roman,"transformed/keystroke_Windows/roUrParl_dataset")

if __name__ == "__main__":
    main()
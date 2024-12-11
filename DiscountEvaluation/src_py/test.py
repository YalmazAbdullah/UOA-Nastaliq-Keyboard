from util import read_json

set_CRULP = set(read_json("keyboards/mappings/CRULP").keys())
set_Windows = set(read_json("keyboards/mappings/Windows").keys())
char_set = set_CRULP.intersection(set_Windows)
token = "هاشم"
for char in token:
    if char not in char_set:
        print(char)
        break



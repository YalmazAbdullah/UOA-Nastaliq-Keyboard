from util import read_tsv,output_tsv
from util import read_json
import pandas as pd

def calculate_freq(data,key_set,upper_set,key_mapping):
    frequency_data = {key: 0 for key in key_set}
    for line in data:
        for char in line:
            if (char == ' '):
                continue
            if(char in upper_set):
                frequency_data["shift"]+=1
            frequency_data[key_mapping[char]]+=1
    return frequency_data 

def calculate_sp(data):
    for triad in data:
        # figure out how this is gonna work
        # TODO
        pass

def main():    
    # read keyboard data
    qwerty_data = read_json("keyboards/QWERTY")
    key_set = qwerty_data["Keys"]
    key_mapping = qwerty_data["Mapping"]
    upper_set = set(qwerty_data["Cases"]["Upper"])

    finger_data = []
    hand_data = []
    distance_data = []

    for key in qwerty_data["Keys"]:
        finger_data.append(qwerty_data["Finger-Assignment"][key])
        hand_data.append(qwerty_data["Hand-Assignment"][key])
        distance_data.append(qwerty_data["Distance"][key])

    # Dataset: Dakshina
    crulp,roman = read_tsv("transformed/keystroke_CRULP/dakshina_dataset")
    windows,roman = read_tsv("transformed/keystroke_Windows/dakshina_dataset")

    frequency_roman = calculate_freq(roman,key_set,upper_set,key_mapping)
    frequency_windows = calculate_freq(windows,key_set,upper_set,key_mapping)
    frequency_crulp = calculate_freq(crulp,key_set,upper_set,key_mapping)

    crulp,roman = read_tsv("transformed/triad_CRULP/dakshina_dataset")
    windows,roman = read_tsv("transformed/triad_Windows/dakshina_dataset")

    strokePenalty_roman = calculate_sp()
    strokePenalty_windows = calculate_sp()
    strokePenalty_crulp = calculate_sp()

    df_roman = pd.DataFrame({
        'Key':qwerty_data["Keys"],
        'Frequency':frequency_roman.values(),
        'Distance':distance_data,
        'Finger':finger_data,
        'Hand':hand_data
    })
    df_roman['Keyboard'] = 'Roman'

    df_crulp = df_roman.copy()
    df_crulp['Frequency'] = frequency_windows.values()
    df_crulp['Keyboard'] = 'Windows'

    df_windows = df_roman.copy()
    df_windows['Frequency'] = frequency_crulp.values()
    df_windows['Keyboard'] = 'CRULP'
    
    df_dakshina = pd.concat([df_roman, df_crulp,df_windows], ignore_index=True)
    df_dakshina.to_csv("./output/data/dakshina.csv", index=True)

    # Dataset: Roman Urdu Parl
    crulp,roman = read_tsv("transformed/keystroke_CRULP/roUrParl_dataset")
    windows,roman = read_tsv("transformed/keystroke_Windows/roUrParl_dataset")

    frequency_roman = calculate_freq(roman,key_set,upper_set,key_mapping)
    frequency_windows = calculate_freq(windows,key_set,upper_set,key_mapping)
    frequency_crulp = calculate_freq(crulp,key_set,upper_set,key_mapping)

    df_roman['Frequency'] = frequency_roman.values()
    df_crulp['Frequency'] = frequency_windows.values()
    df_windows['Frequency'] = frequency_crulp.values()

    df_roUrParl = pd.concat([df_roman, df_crulp,df_windows], ignore_index=True)
    df_roUrParl.to_csv("./output/data/roUrParl.csv", index=True)

if __name__ == "__main__":
    main()
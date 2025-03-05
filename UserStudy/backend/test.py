import pandas as pd
import json


STIMULUS_ADRESS = "./backend/assets/stimulus_bins.json"
CSV_ADRESS = "./backend/assets/counter_balance.csv"

counter_balance = pd.read_csv(CSV_ADRESS)
experiemnt_index = counter_balance[counter_balance["State"] == "incomplete"].index[0]
current_experiment = counter_balance.iloc[experiemnt_index]
counter_balance.at[experiemnt_index, "State"] = "InProgress"
current_experiment = counter_balance.iloc[experiemnt_index]
print(current_experiment)

with open(STIMULUS_ADRESS) as file:
    stimuli = json.load(file)
    # fetch stimuli
    stimuli_bins = [
        stimuli[current_experiment["Bin 1"]],
        stimuli[current_experiment["Bin 2"]],
        stimuli[current_experiment["Bin 3"]]
    ]
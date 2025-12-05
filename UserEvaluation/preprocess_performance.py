
import pandas as pd
import json

data = pd.read_csv("../Data_User/raw/measures.csv")
users = pd.read_csv("../Data_User/raw/users.csv")

def read_json(adress):
    file = open(adress+".json")
    data = json.load(file)
    file.close()
    return data

# for all incomplete or withdraw, drop from database
users = users[users["status"] != "WITHDRAWN"]

# drop inclomplete latin square
users = users[users["uid"] != 3]
users = users[users["uid"] != 4]
users = users[users["uid"] != 11]
users = users[users["uid"] != 13]
users = users[users["uid"] != 18]
# users = users[users["uid"] != 2] # dropped beacuse gls incomplete
# users = users[users["uid"] != 9] # dropped because gls incomplete

# minimize gls id
users["gls_id"] = users["gls_id"]%3
print(users)

#filter from data
data = data[data["user"].isin(users["uid"])]

# filter first two conditions
training_stims = [
    'crings fi fi paren.',
    'oleadossing gon lorick pells.',
    "جو ظلم تو سہتا ہے بغاوت نہیں کرتا",
    "خود شہزادی سکینہ علیہ السلام کا فیصلہ کافی ہے۔",
    "گنتی میں اسے سات سو پینسٹھ بولا جاتا ہے۔",
    "جس سے ساری کہانی میں مزہ پیدا ہوتا ہے۔",
    "یہ تو کسی ناول کا نام لگتا ہے",
    "یہ عمارت زراعت کے ترقی یافتہ ہونے کا ثبوت ہے۔",
]
data = data[~data["stimulus"].isin(training_stims)]

# check speed calculation was correct
stim = data["stimulus"]
wpm = data["wpm"]
time = data["end_time"]-data["start_time"]
for i in range(len(data)):
    words = stim.iloc[i].split(" ")
    calc = (data["end_time"].iloc[i]-data["start_time"].iloc[i])/float(len(words))
    if abs(wpm.iloc[i] - calc)>=0.00000001:
        print("error at line %",i)
        print(wpm.iloc[i])
        print(calc)
        print(len(words))
        pass

# check for start time misalignment
for i in range(len(data)):
    if data["start_time"].iloc[i] != json.loads(data["log"].iloc[i])[0]["timestamp"]:
        print("start time misaligned")
        print(data["user"].iloc[i])
        print(data["condition"].iloc[i])
        pass

stim_level = data[["user","condition","wpm"]]
stim_level = stim_level.rename(columns={"wpm": "performance"})
stim_level['stim'] = stim_level.groupby(['user', 'condition']).cumcount() + 1

# add bin number
bin_order = {
    0:{"baseline":0,"crulp":1,"ime":2,"windows":3},
    1:{"baseline":0,"ime":3,"windows":1,"crulp":2},
    2:{"baseline":0,"windows":2,"crulp":3,"ime":1},
}

stim_level = stim_level.merge(users[["uid","gls_id"]], left_on="user", right_on="uid", how="left")
stim_level["bin"] = stim_level.apply(
    lambda row: bin_order[row["gls_id"]][row["condition"]],
    axis=1
).astype(int)
    
# add condition code
stim_level["code"] = stim_level["bin"].astype(str) + "_" + stim_level["stim"].astype(str)
stim_level.to_csv('stim_level.csv')

# Info for debugging and verification
stim_counts = (
    stim_level.groupby(["user", "condition"])["stim"]
    .nunique()
    .reset_index(name="stim_count")
)

# Filter pairs where stim_count < 8
missing_stims = stim_counts[stim_counts["stim_count"] < 8]

print("User-condition pairs missing some stimuli:")
print(missing_stims)
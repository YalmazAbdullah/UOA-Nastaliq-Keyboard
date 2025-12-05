import pandas as pd
import json

data = pd.read_csv("../Data_User/raw/questions.csv")
print

ranking = []
for i in range(len(data)):
    ranking.append(json.loads(data["ranking"].iloc[i]))

data = data[['user']]
data = data.join(pd.DataFrame(ranking, columns=["1", "2", "3"]))
print(data)
data.to_csv('preference_rankings.csv')
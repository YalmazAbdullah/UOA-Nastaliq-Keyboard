import pandas as pd

users = pd.read_csv("../Data_User/raw/users.csv")

# for all withdraw, drop from database
users = users[users["status"] != "WITHDRAWN"]
users["gls_id"] = users["gls_id"]%3+1

print("Dropped rows:")
dropped = pd.concat([
    users[users["uid"] == 3], # dropped because langague ability
    users[users["uid"] == 4], # dropped because incomplete
    users[users["uid"] == 11], # dropped because baseline missing 1 measurement (bug)
    users[users["uid"] == 13], # dropped because langague ability
    users[users["uid"] == 18], # dropped because incomplete

    # users[users["uid"] == 2], # dropped beacuse gls incomplete
    # users[users["uid"] == 9], # dropped because gls incomplete
])
print(dropped)

users = users[~users["uid"].isin(dropped["uid"])]

print("\nGreco-Latin order counts:")
print("one-{0} two-{1} three-{2}\n".format(users["gls_id"].eq(1).sum(), users["gls_id"].eq(2).sum(), users["gls_id"].eq(3).sum()))
print("Final user selection")
print(users)
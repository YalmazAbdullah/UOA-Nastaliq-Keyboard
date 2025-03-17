import sqlite3
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import schemas
import utils
from json import dumps, load
import pandas as pd
from fastapi import HTTPException
import hmac
import hashlib
import base64

# define stimulus bins
STIMULUS_ADRESS = "./backend/assets/stimulus_bins.json"
CSV_ADRESS = "./backend/assets/counter_balance.csv"

# set up api
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# connect to databse
con = sqlite3.connect("./backend/_database.db")
cursor = con.cursor()
test_db = {}

# cached variables
stimuli_bins = []
baseline_stims = [
    "this is a test input for the baseline 1",
    "this is a test input for the baseline 2",
    "this is a test input for the baseline 3",
    "this is a test input for the baseline 4",
    "this is a test input for the baseline 5",
]

SECRET_KEY = b"user-code-seed"  # Encryption Key

def generate_code(num):
    num_bytes = str(num).encode()
    hash_bytes = hmac.new(SECRET_KEY, num_bytes, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(hash_bytes)[:6].decode() 


@app.post("/start_session")
async def start_session():
    # create new enetery in database
    cursor.execute("INSERT INTO users DEFAULT VALUES")
    
    # get that entery id
    new_uid = cursor.lastrowid 

    # create user_code
    u_code = generate_code(new_uid)

    # get last incomplete condition and bin form gls csv
    counter_balance = pd.read_csv(CSV_ADRESS)
    incomplete_rows = counter_balance[counter_balance["State"] == "incomplete"]
    
    if incomplete_rows.empty:
        # if no incomplete then repeate an inprogress condition
        incomplete_rows = counter_balance[counter_balance["State"] == "inprogress"]
        if incomplete_rows.empty:
            # exit prematurely if study is complete
            return {"message": "Study Complete"}
    
    experiemnt_index = incomplete_rows.index[0]
    current_experiment = counter_balance.iloc[experiemnt_index]
    
    # mark it as in-progress  in csv
    counter_balance.at[experiemnt_index, "State"] = "inprogress"
    counter_balance.to_csv(CSV_ADRESS, index=False)

    # send gls id to database and commit to database
    cursor.execute("UPDATE users SET gls_id = ? WHERE uid = ?", (int(current_experiment["id"]), new_uid))
    con.commit()
    cursor.execute("UPDATE users SET code = ? WHERE uid = ?", (u_code, new_uid))
    con.commit()

    # set up condition order
    condition_order = [
        "baseline",
        current_experiment["Condition 1"],
        current_experiment["Condition 2"],
        current_experiment["Condition 3"],
        "questionnaire"
    ]

    with open(STIMULUS_ADRESS) as file:
        stimuli = load(file)
        # fetch stimuli
        stimuli_bins = [
            baseline_stims,
            stimuli[current_experiment["Bin 1"]],
            stimuli[current_experiment["Bin 2"]],
            stimuli[current_experiment["Bin 3"]]
        ]
    
    # send information to client as response
    return {"uid": new_uid, "conditions": condition_order, "stimuli": stimuli_bins, "code": u_code}


@app.post("/result", status_code=201)
async def create_user(measure:schemas.Measure):
    try:
        cursor.execute("INSERT INTO measures ( user, condition, stimulus, start_time, end_time, log, error_log, transposition_count, ommission_count, substitution_count, addition_count, wpm) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
            measure.user, measure.condition, measure.stimulus, 
            measure.start_time, measure.end_time,  
            dumps(measure.log),  dumps(measure.error_log), 
            measure.transposition_count, measure.ommission_count, 
            measure.substitution_count, measure.addition_count,  
            measure.wpm))
        con.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")


# test ping: http://XYZ/withdraw?uid=1
@app.put("/withdraw", status_code=201)
async def withdraw(uid: int = Query(-1)):
    try:
        cursor.execute("UPDATE users SET status = ? WHERE uid = ?", ("WITHDRAWN", uid))
        con.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {str(e)}")


























# def build_experiment(id:int):
#     # query database for all incomplete sequences
#     # pick the first
#     pass



# # root. does nothing for now
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# # post new user
# @app.post("/user/", status_code=201)
# async def create_user(user:schemas.User):
#     # TODO: check if name and email already in database. If yes apologize. If no continue.
    
#     # add this info to database
#     cursor.execute("INSERT INTO user (name, email) VALUES (?, ?)", 
#                    (user.name, user.email))
#     con.commit()
#     user_id = cursor.lastrowid

#     # TODO: replace this with the build experiment function
#     data = schemas.ExperimentData(
#         **{"uid" : user_id,
#         "condition1" : utils.CONDITIONS[0],
#         "condition2" : utils.CONDITIONS[1],
#         "condition3" : utils.CONDITIONS[2],
#         "condition1_cases" : utils.TEST_CASES[:3],
#         "condition2_cases" : utils.TEST_CASES[3:6],
#         "condition3_cases" : utils.TEST_CASES[6:9],}
#     )

#     # also commit to data base
#     cursor.execute("INSERT INTO experiment (uid, condition1, condition2, condition3,\
#                    condition1_cases, condition2_cases, condition3_cases)\
#                    VALUES (?, ?, ?, ?, ?, ?, ?)", 
#                    (data.uid, data.condition1, data.condition2, data.condition3,
#                     dumps(data.condition1_cases), dumps(data.condition2_cases), dumps(data.condition3_cases)))
#     con.commit()
#     return data

# # post experiment results
# @app.post("/result/", status_code=201)
# async def create_user(results:schemas.ExperimentResult):
#     cursor.execute("INSERT INTO results (uid, condition, test_case,\
#                    raw_input, time,\
#                    omissions, insertions, substitutions, doublings, alternations)\
#                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
#                    (results.name, results.email))
#     con.commit()
#     return

# # post experiment results
# @app.post("/complete/", status_code=204)
# async def create_user(complete:bool):
#     # if completed then mark sequence as completed 
#     # also mark user as complete
#     return 
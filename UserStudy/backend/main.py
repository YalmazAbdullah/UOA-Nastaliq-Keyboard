import sqlite3
from fastapi import FastAPI
import schemas
import utils
from json import dumps

# set up api
app = FastAPI()

# connect to databse
con = sqlite3.connect("./backend/_database.db")
cursor = con.cursor()

test_db = {}

def build_experiment(id:int):
    # query database for all incomplete sequences
    # pick the first
    pass

# root. does nothing for now
@app.get("/")
async def root():
    return {"message": "Hello World"}

# post new user
@app.post("/user/", status_code=201)
async def create_user(user:schemas.User):
    # TODO: check if name and email already in database. If yes apologize. If no continue.
    # add this info to database
    cursor.execute("INSERT INTO user (name, email) VALUES (?, ?)", 
                   (user.name, user.email))
    con.commit()
    user_id = cursor.lastrowid

    # TODO: replace this with the build experiment function
    data = schemas.ExperimentData(
        **{"uid" : user_id,
        "condition1" : utils.CONDITIONS[0],
        "condition2" : utils.CONDITIONS[1],
        "condition3" : utils.CONDITIONS[2],
        "condition1_cases" : utils.TEST_CASES[:3],
        "condition2_cases" : utils.TEST_CASES[3:6],
        "condition3_cases" : utils.TEST_CASES[6:9],}
    )

    # also commit to data base
    cursor.execute("INSERT INTO experiment (uid, condition1, condition2, condition3,\
                   condition1_cases, condition2_cases, condition3_cases)\
                   VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (data.uid, data.condition1, data.condition2, data.condition3,
                    dumps(data.condition1_cases), dumps(data.condition2_cases), dumps(data.condition3_cases)))
    con.commit()
    return data

# post experiment results
@app.post("/result/", status_code=201)
async def create_user(results:schemas.ExperimentResult):
    cursor.execute("INSERT INTO results (uid, condition, test_case,\
                   raw_input, time,\
                   omissions, insertions, substitutions, doublings, alternations)\
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (results.name, results.email))
    con.commit()
    return

# post experiment results
@app.post("/complete/", status_code=204)
async def create_user(complete:bool):
    # if completed then mark sequence as completed 
    # also mark user as complete
    return 
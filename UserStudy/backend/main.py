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
STIMULUS_ADRESS = "./assets/stimulus_bins.json"
CSV_ADRESS = "./assets/counter_balance.csv"

# set up api
app = FastAPI()

origins = [
    "http://localhost:3000",  
    "http://127.0.0.1:3000",  
    "https://yalmazadbdullah.com",  
    "https://www.yalmazadbdullah.com",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/test")
def read_root():
    return {"message": "CORS enabled!"}

def get_db():
    con = sqlite3.connect("./_database.db")
    cursor = con.cursor()
    return con, cursor

# cached variables
stimuli_bins = []

baseline_stims = [
    'oleadossing gon lorick pells.',
    'forten thebemmer wentor sunch fatimand starget.',
    '"kickspeck kifferent pells fi, ints anding fi hanchoin jus resh."',
    'sevent ruggling happentry rept, tex saidaw lasky upcoren nakes.',
    '"ubas tecon bankit, plandle os stis os, besters hannicatrace twent."',
    'savid hannicatrace gred sprin belents gandoff?',
    'crings fi fi paren.',
    '"soundid togetting lenew squick, a cancake gred ruggling gon kims."',
    'folden fi gast sunch tren hanchoin hanchoin?',
    '"tast os askets classengers, jobjector tanin fi, besters gast."',
    'shood hannicatrace nat os twent kickspeck, thebemmer clively sprin hanchoin.'
    'stor oleadossing gunt a hant oldrummer, os trings smind regist.',
]

SECRET_KEY = b"user-code-seed"  # Encryption Key

def generate_code(num):
    num_bytes = str(num).encode()
    hash_bytes = hmac.new(SECRET_KEY, num_bytes, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(hash_bytes)[:6].decode() 


@app.post("/api/start_session")
async def start_session():
    con, cursor = get_db()
    try:
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
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()


@app.post("/api/result", status_code=201)
async def create_user(measure:schemas.Measure):
    con, cursor = get_db()
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
    finally:
        con.close()


# test ping: http://XYZ/withdraw?uid=1
@app.put("/api/withdraw", status_code=201)
async def withdraw(uid: int = Query(-1)):
    con, cursor = get_db()
    try:
        if uid == -1:
            raise HTTPException(status_code=400, detail="Invalid user ID")

        cursor.execute("UPDATE users SET status = ? WHERE uid = ?", ("WITHDRAWN", uid))
        con.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Invalid request: {str(e)}")
    finally:
        con.close()
    
@app.post("/api/submit")
def submit_data(data: schemas.QuestionData, uid: int = Query(-1)):
    con, cursor = get_db()
    try:
        if uid == -1:
            raise HTTPException(status_code=400, detail="Invalid user ID")

        cursor.execute(
            """INSERT INTO questions (
                user, ranking, rankingReason, romanUrduUsage, urduScriptUsage, 
                urduContexts, otherCommunication, accessDifficulty, urduContent, 
                langaugeUse, langaugeAcq, birthYear, gender, feedback
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                uid, dumps(data.ranking), data.rankingReason, data.romanUrduUsage,
                data.urduScriptUsage, data.urduContexts, data.otherCommunication,
                data.accessDifficulty, data.urduContent, data.langaugeUse,
                data.langaugeAcq, data.birthYear, data.gender, data.feedback
            ),
        )
        cursor.execute("UPDATE users SET status = ? WHERE uid = ?", ("COMPLETED", uid))
        con.commit()
        return {"message": "Data submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()
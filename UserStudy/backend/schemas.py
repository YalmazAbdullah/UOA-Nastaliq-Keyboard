from pydantic import BaseModel

class Measure(BaseModel):
    user: int
    condition: str
    stimulus: str
    start_time : float
    end_time: float
    log: list
    error_log: list
    transposition_count:int
    ommission_count:int
    substitution_count:int
    addition_count:int
    wpm : float

class QuestionData(BaseModel):
    ranking: list
    rankingReason: str
    romanUrduUsage: str
    urduScriptUsage: str
    urduContexts: str
    otherCommunication: str
    accessDifficulty: str
    urduContent: str
    langaugeUse: str
    langaugeAcq: str
    birthYear: int
    gender: str
    feedback: str = None  # Optional field















class User(BaseModel):
    name:str
    email:str

class ExperimentData(BaseModel):
    uid:int
    condition1:str
    condition2:str
    condition3:str
    condition1_cases:list
    condition2_cases:list
    condition3_cases:list


class ExperimentResult(BaseModel):
    uid:int
    condition:str
    test_case:str
    raw_input:str
    time:int
    omissions:int 
    insertions:int 
    substitutions:int 
    doublings:int 
    alternations:int
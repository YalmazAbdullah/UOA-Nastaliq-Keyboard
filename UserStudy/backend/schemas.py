from pydantic import BaseModel

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
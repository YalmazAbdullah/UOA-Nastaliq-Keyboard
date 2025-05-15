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
    priorUse: list
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

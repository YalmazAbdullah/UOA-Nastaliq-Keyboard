import sqlite3

def main():
    # Create SQLite database and table
    conn = sqlite3.connect("./_database.db")
    cursor = conn.cursor()

    # build user table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users(
                        uid INTEGER PRIMARY KEY AUTOINCREMENT,
                        gls_id INTEGER DEFAULT 0, 
                        code TEXT,
                        status TEXT DEFAULT INCOMPLETE
                    )
                    """)
    
    # build measures table
    cursor.execute(""" 
                   CREATE TABLE IF NOT EXISTS measures(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user INTEGER,
                        condition TEXT,
                        stimulus TEXT,
                        start_time REAL,
                        end_time REAL,
                        log TEXT,
                        error_log TEXT,
                        transposition_count INTEGER,
                        ommission_count INTEGER,
                        substitution_count INTEGER,
                        addition_count INTEGER,
                        wpm REAL,
                        FOREIGN KEY(user) REFERENCES users(uid)
                    )
                   """)
    
    # build measures table
    cursor.execute(""" 
                   CREATE TABLE IF NOT EXISTS questions(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user INTEGER,
                        ranking TEXT,
                        rankingReason TEXT,
                        priorUse TEXT,
                        romanUrduUsage TEXT,
                        urduScriptUsage TEXT,
                        urduContexts TEXT,
                        otherCommunication TEXT,
                        accessDifficulty TEXT,
                        urduContent TEXT,
                        langaugeUse TEXT,
                        langaugeAcq TEXT,
                        birthYear INTEGER,
                        gender TEXT,
                        feedback TEXT,
                        FOREIGN KEY(user) REFERENCES users(uid)
                    )
                   """)

    conn.commit()

if __name__=="__main__":
    main()
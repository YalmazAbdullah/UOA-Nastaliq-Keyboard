import sqlite3

def main():
    # Create SQLite database and table
    conn = sqlite3.connect("./backend/_database.db")
    cursor = conn.cursor()

    # build user table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users(
                        uid INTEGER PRIMARY KEY AUTOINCREMENT,
                        gls_id INTEGER DEFAULT 0, 
                        code TEXT,
                        completed BOOLEAN DEFAULT 0
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

    # # build measures table
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS experiment(
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         uid INTEGER NOT NULL,
    #         condition1 TEXT NOT NULL,
    #         condition2 TEXT NOT NULL,
    #         condition3 TEXT NOT NULL,
    #         condition1_cases TEXT NOT NULL,
    #         condition2_cases TEXT NOT NULL,
    #         condition3_cases TEXT NOT NULL
    #     )
    # """)

    # # build measures table
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS results(
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         uid INTEGER NOT NULL,
    #         condition TEXT NOT NULL,
    #         test_case TEXT NOT NULL,
    #         raw_input TEXT NOT NULL,
    #         time FLOAT NOT NULL,
    #         omissions INT NOT NULL, 
    #         insertions INT NOT NULL, 
    #         substitutions INT NOT NULL, 
    #         doublings INT NOT NULL, 
    #         alternations INT NOT NULL
    #     )
    # """)

    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS squences(
    #         sequence TEXT NOT NULL,
    #         completed BOOLEAN DEFAULT 0 
    #     )
    # """)

    conn.commit()

if __name__=="__main__":
    main()
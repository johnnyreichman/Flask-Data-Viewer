#Functions to help load the election csv data into the SQLite database.
#Not used to run the application.

def CreateSenateTable():
    conn = sqlite3.connect('VotingPatterns.db')
    conn.execute('''CREATE TABLE SENATE
             (ID INT PRIMARY KEY     NOT NULL,
             YEAR          INT    NOT NULL,
             STATE            TEXT     NOT NULL,
             STATE_ABB        CHAR(2),
             STAGE         TEXT,
             SPECIAL          INT,
             CANDIDATE          TEXT,
             PARTY_DETAIL          TEXT,
             WRITE_IN          INT,
             CANDIDATE_VOTES          INT,
             TOTAL_VOTES          INT,
             UNOFFICIAL          INT,
             PARTY_SIMPLE          TEXT

             );''')
    conn.close()

def CreateHouseTable():
    conn = sqlite3.connect('VotingPatterns.db')
    conn.execute('''CREATE TABLE HOUSE
             (ID INT PRIMARY KEY     NOT NULL,
             YEAR          INT    NOT NULL,
             STATE            TEXT     NOT NULL,
             STATE_ABB        CHAR(2),
             DISTRICT          TEXT,
             STAGE         TEXT,
             RUNOFF          INT,
             SPECIAL          INT,
             CANDIDATE          TEXT,
             PARTY          TEXT,
             WRITE_IN          INT,
             CANDIDATE_VOTES          INT,
             TOTAL_VOTES          INT,
             UNOFFICIAL          INT,
             FUSION_TICKET          INT

             );''')
    conn.close()
def CreatePresidentTable():
    conn = sqlite3.connect('VotingPatterns.db')
    conn.execute('''CREATE TABLE PRESIDENT
             (ID INT PRIMARY KEY     NOT NULL,
             YEAR          INT    NOT NULL,
             STATE            TEXT     NOT NULL,
             STATE_ABB        CHAR(2),
             CANDIDATE          TEXT,
             PARTY_DETAIL          TEXT,
             WRITE_IN          INT,
             CANDIDATE_VOTES          INT,
             TOTAL_VOTES          INT,
             PARTY_SIMPLE          TEXT

             );''')
    conn.close()

def AddCSVToSenateTable():
    con = sqlite3.connect("VotingPatterns.db") # change to 'sqlite:///your_filename.db'
    cur = con.cursor()
    with open('data/1976-2020-senate.csv','r') as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin) # comma is default delimiter
        to_db = [(i['id'],
            i['year'],
            i['state'],
            i['state_po'],
            i['stage'],
            i['special'],
            i['candidate'],
            i['party_detailed'],
            i['writein'],
            i['candidatevotes'],
            i['totalvotes'],
            i['unofficial'],
            i['party_simplified'],
            ) for i in dr]
    cur.executemany("INSERT INTO SENATE (ID,YEAR,STATE,STATE_ABB,STAGE,SPECIAL,CANDIDATE,PARTY_DETAIL,WRITE_IN,CANDIDATE_VOTES,TOTAL_VOTES,UNOFFICIAL,PARTY_SIMPLE) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
    con.commit()
    con.close()

#House data needed a little encoding recognition
def AddCSVToHouseTable():
    con = sqlite3.connect("VotingPatterns.db") # change to 'sqlite:///your_filename.db'
    cur = con.cursor()

    with codecs.open('data/1976-2018-house.csv', encoding='iso-8859-1') as fin:
        dr = csv.DictReader(fin) # comma is default delimiter

        to_db = [(i['id'],
            i['year'],
            i['state'],
            i['state_po'],
            i['district'],
            i['stage'],
            i['runoff'],
            i['special'],
            i['candidate'],
            i['party'],
            i['writein'],
            i['candidatevotes'],
            i['totalvotes'],
            i['unofficial'],
            i['fusion_ticket'],
            ) for i in dr]

    cur.executemany("INSERT INTO HOUSE (ID,YEAR,STATE,STATE_ABB,DISTRICT,STAGE,RUNOFF,SPECIAL,CANDIDATE,PARTY,WRITE_IN,CANDIDATE_VOTES,TOTAL_VOTES,UNOFFICIAL,FUSION_TICKET) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
    con.commit()
    con.close()

def AddCSVToPresidentTable():
    con = sqlite3.connect("VotingPatterns.db") # change to 'sqlite:///your_filename.db'
    cur = con.cursor()
    with open('data/1976-2020-president.csv','r') as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin) # comma is default delimiter
        to_db = [(i['id'],
            i['year'],
            i['state'],
            i['state_po'],
            i['candidate'],
            i['party_detailed'],
            i['writein'],
            i['candidatevotes'],
            i['totalvotes'],
            i['party_simplified'],
            ) for i in dr]
    cur.executemany("INSERT INTO PRESIDENT (ID,YEAR,STATE,STATE_ABB,CANDIDATE,PARTY_DETAIL,WRITE_IN,CANDIDATE_VOTES,TOTAL_VOTES,PARTY_SIMPLE) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
    con.commit()
    con.close()

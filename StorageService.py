import sqlite3, csv
from OverTimeViewModel import *
import codecs

def convertElectionListToDictList(elections):
    electionDictList = []
    for election in elections:
        electionDict = convertElectionToDict(election)
        electionDictList.append(electionDict)
    return electionDictList

def convertElectionToDict(election):
    candidatesList = []
    for candidate in election.Candidates:
        candidatesList.append(vars(candidate))
    electionDict = {"year": election.Year, "TotalVotes": election.TotalVotes, "Candidates": candidatesList}
    return electionDict

def convertTurnoutToDict(rawTurnout):
    turnoutDict = {}
    for row in rawTurnout:
        turnoutDict[str(row[0])] = row[1]
    return turnoutDict


def GetElectionsOverTime(state,race,district):
    conn = sqlite3.connect('VotingPatterns.db')
    cur = conn.cursor()
    command = ""
    if race == "SENATE":
        command = "SELECT YEAR,CANDIDATE,PARTY_SIMPLE,TOTAL_VOTES,CANDIDATE_VOTES FROM SENATE WHERE STATE_ABB=?"
    elif race == "HOUSE":
        command = "SELECT YEAR,CANDIDATE,PARTY,TOTAL_VOTES,CANDIDATE_VOTES FROM HOUSE WHERE STATE_ABB=? AND DISTRICT=?"
    else:
        command = "SELECT YEAR,CANDIDATE,PARTY_SIMPLE,TOTAL_VOTES,CANDIDATE_VOTES FROM PRESIDENT WHERE STATE_ABB=?"
    if race == "HOUSE":
        cur.execute(command, (state,district))
    else:
        cur.execute(command, (state,))
    stateElections = []
    electionToAdd = None
    for row in cur:
        if electionToAdd is None:
            electionToAdd = Election(row[0],row[3],[])
            electionToAdd.Candidates.append(Candidate(row[1], row[2],row[4]))
        elif row[0] != electionToAdd.Year:
            stateElections.append(electionToAdd)
            electionToAdd = Election(row[0],row[3],[])
            electionToAdd.Candidates.append(Candidate(row[1], row[2],row[4]))
        else:
            electionToAdd.Candidates.append(Candidate(row[1], row[2],row[4]))
    print(convertElectionToDict(stateElections[0]))
    return convertElectionListToDictList(stateElections)


def CreateSenateTable():
    conn = sqlite3.connect('VotingPatterns.db')
    print("Opened database successfully")

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
    print("Table created successfully")

    conn.close()
def CreateHouseTable():
    conn = sqlite3.connect('VotingPatterns.db')
    print("Opened database successfully")

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
    print("Table created successfully")

    conn.close()
def CreatePresidentTable():
    conn = sqlite3.connect('VotingPatterns.db')
    print("Opened database successfully")

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
    print("Table created successfully")

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

    print("opened db")
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

def GetPopularCandidateData():
    conn = sqlite3.connect('VotingPatterns.db')
    cur = conn.cursor()
    cur.execute("select COUNT(*), CANDIDATE FROM SENATE WHERE CANDIDATE_VOTES > (TOTAL_VOTES / 2) GROUP BY CANDIDATE HAVING COUNT(CANDIDATE) < 2\
        UNION select COUNT(*), CANDIDATE FROM HOUSE WHERE CANDIDATE_VOTES > (TOTAL_VOTES / 2) GROUP BY CANDIDATE HAVING COUNT(CANDIDATE) < 2")
    oneTerm = len(cur.fetchall())
    cur.execute("select COUNT(*), CANDIDATE FROM SENATE WHERE CANDIDATE_VOTES > (TOTAL_VOTES / 2) GROUP BY CANDIDATE HAVING COUNT(CANDIDATE) = 2\
        UNION select COUNT(*), CANDIDATE FROM HOUSE WHERE CANDIDATE_VOTES > (TOTAL_VOTES / 2) GROUP BY CANDIDATE HAVING COUNT(CANDIDATE) =2")
    twoTerm = len(cur.fetchall())
    cur.execute("select COUNT(*), CANDIDATE FROM SENATE WHERE CANDIDATE_VOTES > (TOTAL_VOTES / 2) GROUP BY CANDIDATE HAVING COUNT(CANDIDATE) > 2\
        UNION select COUNT(*), CANDIDATE FROM HOUSE WHERE CANDIDATE_VOTES > (TOTAL_VOTES / 2) GROUP BY CANDIDATE HAVING COUNT(CANDIDATE) > 2")
    manyTerm = len(cur.fetchall())
    return oneTerm,twoTerm,manyTerm

def GetILTurnout():
    conn = sqlite3.connect('VotingPatterns.db')
    cur = conn.cursor()
    cur.execute("select distinct YEAR, TOTAL_VOTES from SENATE where STATE_ABB='IL'group by YEAR")
    senateTurnout = convertTurnoutToDict(cur.fetchall())
    cur.execute("select distinct YEAR, SUM(CANDIDATE_VOTES) from HOUSE where STATE_ABB='IL'group by YEAR")
    houseTurnout = convertTurnoutToDict(cur.fetchall())
    cur.execute("select distinct YEAR, TOTAL_VOTES from PRESIDENT where STATE_ABB='IL'group by YEAR")
    presTurnount = convertTurnoutToDict(cur.fetchall())
    return senateTurnout,houseTurnout,presTurnount


if __name__ == '__main__':
    #start all of out thingies
    GetILTurnout()

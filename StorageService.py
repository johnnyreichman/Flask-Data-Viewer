import sqlite3, csv
from OverTimeViewModel import *

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


def GetSenateOverTime(state):
    conn = sqlite3.connect('VotingPatterns.db')
    cur = conn.cursor()
    cur.execute("SELECT YEAR,CANDIDATE,PARTY_SIMPLE,TOTAL_VOTES,CANDIDATE_VOTES FROM SENATE WHERE STATE_ABB=?", (state,))
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

def AddRow(id, name, age, state, otherNumber):
    conn = sqlite3.connect('test.db')
    conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (" + id + ",'" + name + "'," + age + ",'" + state + "'," + otherNumber + ")");
    conn.commit()
    conn.close()


if __name__ == '__main__':
    #start all of out thingies
    GetSenateOverTime("WI")

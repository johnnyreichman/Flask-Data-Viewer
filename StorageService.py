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
    return convertElectionListToDictList(stateElections)

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

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

#Retrieves historical election data for the specified state, race, and district (if house race)
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

#Retrieves the number of Congresspeople who serve 1, 2, and 2+ terms
#Note: this only retrieves the number of terms they serve in a particular assembly
#      So if a candidate serves one term as a house member and one term as a senator, they are considered
#      a one-term house member as well as a one-term senator.
def GetPopularCandidateData():
    conn = sqlite3.connect('VotingPatterns.db')
    cur = conn.cursor()
    cur.execute("SELECT candidate,COUNT(*) \
	             FROM ( \
                    SELECT year, state,candidate, MAX(candidate_votes) \
                    FROM SENATE \
                    GROUP BY year, state \
                    ) AS subqueryone \
                 GROUP BY subqueryone.candidate \
                 HAVING COUNT(candidate) < 2 \
                 UNION \
                 SELECT candidate,COUNT(*) \
                 FROM ( \
                    SELECT year, state,candidate, MAX(candidate_votes) \
                    FROM HOUSE \
                    GROUP BY year, state \
                    ) AS subquerytwo \
                 GROUP BY subquerytwo.candidate \
                 HAVING COUNT(candidate) < 2")
    oneTerm = len(cur.fetchall())
    cur.execute("SELECT candidate,COUNT(*) \
	             FROM ( \
                    SELECT year, state,candidate, MAX(candidate_votes) \
                    FROM SENATE \
                    GROUP BY year, state \
                    ) AS subqueryone \
                 GROUP BY subqueryone.candidate \
                 HAVING COUNT(candidate) = 2 \
                 UNION \
                 SELECT candidate,COUNT(*) \
                 FROM ( \
                    SELECT year, state,candidate, MAX(candidate_votes) \
                    FROM HOUSE \
                    GROUP BY year, state \
                    ) AS subquerytwo \
                 GROUP BY subquerytwo.candidate \
                 HAVING COUNT(candidate) = 2")
    twoTerm=len(cur.fetchall())
    cur.execute("SELECT candidate,COUNT(*) \
	             FROM ( \
                    SELECT year, state,candidate, MAX(candidate_votes) \
                    FROM SENATE \
                    GROUP BY year, state \
                    ) AS subqueryone \
                 GROUP BY subqueryone.candidate \
                 HAVING COUNT(candidate) > 2 \
                 UNION \
                 SELECT candidate,COUNT(*) \
                 FROM ( \
                    SELECT year, state,candidate, MAX(candidate_votes) \
                    FROM HOUSE \
                    GROUP BY year, state \
                    ) AS subquerytwo \
                 GROUP BY subquerytwo.candidate \
                 HAVING COUNT(candidate) > 2")
    manyTerm = len(cur.fetchall())
    return oneTerm,twoTerm,manyTerm

#Retrieves Illinois house, presidential, and senate turnout over the years
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

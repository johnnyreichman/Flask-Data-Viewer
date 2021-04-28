class Candidate:
    def __init__(self, name, party, votesRecieved):
        self.Name = name
        self.Party = party
        self.VotesRecieved = votesRecieved
    def __str__(self):
        return "\n Name: " + self.Name + " Party: " + self.Party + str(self.VotesRecieved)

class Election:
    def __init__(self, year, totalVotes, candidates):
        self.Year = year
        self.TotalVotes = totalVotes
        self.Candidates = []
        for candidate in candidates:
            self.Candidates.append(candidate)
    def __str__(self):
        display = "Year: " + str(self.Year) + " TotalVotes: " + str(self.TotalVotes) + "Candidates: "
        for candidate in self.Candidates:
            display += "\n Name: " + candidate.Name + " Party: " + candidate.Party + " VotesRecieved: " + str(candidate.VotesRecieved)
        return display


class State(object):
    def __init__(self, name, elections):
        self.Name = name
        for electionYear in elections:
            self.Elections.append(electionYear)

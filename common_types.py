class Fixture:
    """
    Stores info for one (forthcoming) fixture
    """
    home  = "Not defined"
    away  = "Not defined"

    def __init__(self, home_tm, away_tm):
        self.home = home_tm
        self.away = away_tm

    def __str__(self):
        return self.home + " v " +self.away

class Match:
    """
    Stores the results of one match
    """
    home = "Not defined"
    away = "Not defined"
    home_gls = 0
    away_gls = 0

    def __init__(self, home_tm, away_tm, home_score, away_score):
        self.home = home_tm
        self.away = away_tm
        self.home_gls = home_score
        self.away_gls = away_score

    def __str__(self):
        return self.home + int(self.home_gls) + "-" + int(self.away_gls) + self.away

class TimeFrame:
    """
    Stores info (can be either goals scored, goals conceded or clean sheets)
    for each of the last 10 matches, last 6 matches or all season.
    """
    last10m = 0
    last6m = 0
    all = 0

    def __init__(self):
        self.last10m = 0
        self.last6m = 0
        self.all = 0

    def __str__(self):
        return self.all + " " + self.last10m + " " + self.last6m

    def __eq__(self, other):
        return ( (self.last10m == other.last10m) and
                 (self.last6m == other.last6m) and
                 (self.all == other.all) )

    def __lt__(self, other):
        """
        Use the last6m value as the highest priority in the comparison
        """
        result = True

        if(self.last6m > other.last6m):
            result = True
        elif(self.last6m < other.last6m):
            result = False
        elif(self.all > other.all):
            result = True
        elif(self.all < other.all):
            result = False
        
        return result
    
class AttackingSummary:
    """
    Summary of a team's attacking ability
    """
    team = "Not defined"
    goals_scored = TimeFrame()

#    def __init__(self):
#        self.goals_scored = TimeFrame()

    def __init__(self, team):
        self.goals_scored = TimeFrame()
        self.team = team

    def __str__(self):
        padding = "\t"
        if(len(self.team) < 7):
            padding += "\t"
            
        return self.team + " " + padding + " " + self.goals_scored.all + " " + \
               self.goals_scored.last10m + " " + self.goals_scored.last6m

    def __eq__(self, other):
        
        result = False
        if isinstance(other, self.__class__):
            result = (self.team == other.team) and (self.goals_scored == other.goals_scored)
        else:
            result = False

        return result
    
    def __lt__(self, other):
        """
        Compares two AttackingSummaries. It considers the results over the last
        6 matches to be the most significant stat
        """
        if(self.goals_scored != other.goals_scored):
            return (self.goals_scored < other.goals_scored)
        else:
            return (self.team > other.team)

class DefensiveSummary:
    """
    Summary of a team's defensive ability
    """
    team = "Not defined"
    goals_conceded = TimeFrame()
    clean_sheets = TimeFrame()

    def __init__(self):
        self.goals_conceded = TimeFrame()
        self.clean_sheets = TimeFrame()

    def __init__(self, team):
        self.goals_conceded = TimeFrame()
        self.clean_sheets = TimeFrame()
        self.team = team

    def __str__(self):
        padding = "\t"
        if(len(self.team) < 7):
            padding += "\t"
            
        return self.team + " " + padding + " " + self.goals_conceded.all + " " + \
               self.goals_conceded.last10m + " " + self.goals_conceded.last6m + " " + \
               self.clean_sheets.all + " " + self.clean_sheets.last10m + " " + self.clean_sheets.last6m

    # TO DO: Replace with lt
    def greaterThanCS(self, rhs):
        """
        Compares the clean sheets within two DefensiveSummarys.
        It considers the results over the last 6 matches to be the most significant stat
        """
        result = True
        if(self.clean_sheets.last6m > rhs.clean_sheets.last6m):
            result = True
        elif(self.clean_sheets.last6m < rhs.clean_sheets.last6m):
            result = False
        elif(self.clean_sheets.all > rhs.clean_sheets.all):
            result = True
        elif(self.clean_sheets.all < rhs.clean_sheets.all):
            result = False
        else:
            result = (self.team > rhs.team)

        return result

    def greaterThanGls(self, rhs):
        """
        Compares the goals scored within two DefensiveSummarys.
        It considers the results over the last 6 matches to be the most significant stat
        """
        result = True
        if(self.goals_conceded.last6m > rhs.goals_conceded.last6m):
            result = True
        elif(self.goals_conceded.last6m < rhs.goals_conceded.last6m):
            result = False
        elif(self.goals_conceded.all > rhs.goals_conceded.all):
            result = True
        elif(self.goals_conceded.all < rhs.goals_conceded.all):
            result = False
        else:
            result = (self.team > rhs.team)

        return result


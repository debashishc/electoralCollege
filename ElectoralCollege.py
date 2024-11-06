from enum import Enum, auto

class State(Enum):
    AL = "Alabama"
    AK = "Alaska"
    AZ = "Arizona"
    AR = "Arkansas"
    CA = "California"
    CO = "Colorado"
    CT = "Connecticut"
    DE = "Delaware"
    DC = "District of Columbia"
    FL = "Florida"
    GA = "Georgia"
    HI = "Hawaii"
    ID = "Idaho"
    IL = "Illinois"
    IN = "Indiana"
    IA = "Iowa"
    KS = "Kansas"
    KY = "Kentucky"
    LA = "Louisiana"
    ME = "Maine"
    MD = "Maryland"
    MA = "Massachusetts"
    MI = "Michigan"
    MN = "Minnesota"
    MS = "Mississippi"
    MO = "Missouri"
    MT = "Montana"
    NE = "Nebraska"
    NV = "Nevada"
    NH = "New Hampshire"
    NJ = "New Jersey"
    NM = "New Mexico"
    NY = "New York"
    NC = "North Carolina"
    ND = "North Dakota"
    OH = "Ohio"
    OK = "Oklahoma"
    OR = "Oregon"
    PA = "Pennsylvania"
    RI = "Rhode Island"
    SC = "South Carolina"
    SD = "South Dakota"
    TN = "Tennessee"
    TX = "Texas"
    UT = "Utah"
    VT = "Vermont"
    VA = "Virginia"
    WA = "Washington"
    WV = "West Virginia"
    WI = "Wisconsin"
    WY = "Wyoming"

class Party(Enum):
    DEM = "Democrat"
    REP = "Republican"
    # no point of these parties 
    # but added for completeness
    IND =  "Independent" 
    GRE ="Green"
    LIB = "Liberaterian"


class ElectoralCollege:
    def __init__(self):
        """
        Initialize the Electoral College system using Enums for type safety.
        """
        # Electoral votes mapped to State enum
        self.electoral_votes = {
            State.AL: 9,
            State.AK: 3,
            State.AZ: 11,
            State.AR: 6,
            State.CA: 54,
            State.CO: 10,
            State.CT: 7,
            State.DE: 3,
            State.DC: 3,
            State.FL: 30,
            State.GA: 16,
            State.HI: 4,
            State.ID: 4,
            State.IL: 19,
            State.IN: 11,
            State.IA: 6,
            State.KS: 6,
            State.KY: 8,
            State.LA: 8,
            State.ME: 4,
            State.MD: 10,
            State.MA: 11,
            State.MI: 15,
            State.MN: 10,
            State.MS: 6,
            State.MO: 10,
            State.MT: 4,
            State.NE: 5,
            State.NV: 6,
            State.NH: 4,
            State.NJ: 14,
            State.NM: 5,
            State.NY: 28,
            State.NC: 16,
            State.ND: 3,
            State.OH: 17,
            State.OK: 7,
            State.OR: 8,
            State.PA: 19,
            State.RI: 4,
            State.SC: 9,
            State.SD: 3,
            State.TN: 11,
            State.TX: 40,
            State.UT: 6,
            State.VT: 3,
            State.VA: 13,
            State.WA: 12,
            State.WV: 4,
            State.WI: 10,
            State.WY: 3
        }
        
        # calculate total electoral votes (538)
        self.total_electoral_votes = sum(self.electoral_votes.values())

        # divide total by 2 and add 1 to ensure a majority
        # 538 // 2 = 269, + 1 = 270 (minimum to win)
        self.votes_to_win = (self.total_electoral_votes // 2) + 1

    def get_state_votes(self, state):
        return self.electoral_votes.get(state, 0)

    def calculate_electoral_votes(self, state_results):
        results = dict()

        for state, party in state_results.items():
            if state in self.electoral_votes:
                current_votes = results.get(party, 0)
                results[party] = current_votes + self.electoral_votes[state]

        return results


    def check_winner(self, state_results):
        results = self.calculate_electoral_votes(state_results=state_results)

        for party, votes in results.items():
            if votes >= self.votes_to_win:
                return True, party
        return False, None

    def get_remaining_paths(self, current_results, uncalled_states):
        
        current_totals = self.calculate_electoral_votes(current_results)
        remaining_votes = sum(self.electoral_votes[state] for state in uncalled_states)
        
        paths = {}
        for party, current_votes in current_totals.items():
            needed_votes = self.votes_to_win - current_votes
            paths[party] = {
                'current_votes': current_votes,
                'needed_votes': needed_votes,
                'possible': needed_votes <= remaining_votes
            }
        return paths


if __name__ == "__main__":

    # create instance
    ec = ElectoralCollege()

    # test results:
    test_results = {
        # Northeast
        State.CT: None,  # Connecticut
        State.ME: None,  # Maine
        State.MA: Party.DEM,  # Massachusetts
        State.NH: None,  # New Hampshire
        State.RI: Party.DEM,  # Rhode Island
        State.VT: Party.DEM,  # Vermont
        State.NJ: None,  # New Jersey
        State.NY: None,  # New York
        State.PA: None,  # Pennsylvania
        
        # Midwest
        State.IL: Party.DEM,  # Illinois
        State.IN: Party.REP,  # Indiana
        State.MI: None,  # Michigan
        State.OH: Party.REP,  # Ohio
        State.WI: None,  # Wisconsin
        State.IA: None,  # Iowa
        State.KS: None,  # Kansas
        State.MN: None,  # Minnesota
        State.MO: Party.REP,  # Missouri
        State.NE: None,  # Nebraska
        State.ND: Party.REP,  # North Dakota
        State.SD: Party.REP,  # South Dakota
        
        # South
        State.DE: Party.DEM,  # Delaware
        State.FL: Party.REP,  # Florida
        State.GA: None,  # Georgia
        State.MD: Party.DEM,  # Maryland
        State.NC: None,  # North Carolina
        State.SC: Party.REP,  # South Carolina
        State.VA: None,  # Virginia
        State.WV: Party.REP,  # West Virginia
        State.AL: Party.REP,  # Alabama
        State.KY: Party.REP,  # Kentucky
        State.MS: Party.REP,  # Mississippi
        State.TN: Party.REP,  # Tennessee
        State.AR: Party.REP,  # Arkansas
        State.LA: Party.REP,  # Louisiana
        State.OK: Party.REP,  # Oklahoma
        State.TX: Party.REP,  # Texas
        
        # West
        State.AZ: None,  # Arizona
        State.CO: Party.DEM,  # Colorado
        State.ID: None,  # Idaho
        State.MT: Party.REP,  # Montana
        State.NV: None,  # Nevada
        State.NM: None,  # New Mexico
        State.UT: Party.REP,  # Utah
        State.WY: Party.REP,  # Wyoming
        State.AK: None,  # Alaska
        State.CA: None,  # California
        State.HI: None,  # Hawaii
        State.OR: None,  # Oregon
        State.WA: None,  # Washington
        
        # District of Columbia
        State.DC: Party.DEM,  # District of Columbia
    }

    # calculate current electoral votes
    vote_totals = ec.calculate_electoral_votes(test_results)

    # check if there is a winner
    has_winner, winner = ec.check_winner(test_results)

    # check uncalled states for remaining paths to victory
    test_uncalled_states = [state for state, result in test_results.items() if result is None]
    remaining_paths = ec.get_remaining_paths(test_results, test_uncalled_states)
    print("\nPaths to victory:", remaining_paths)



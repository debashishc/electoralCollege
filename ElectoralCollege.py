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
    DEM: "Democrat"
    REP: "Republican"
    # no point of these parties 
    # but added for completeness
    IND: "Independent" 
    GRE: "Green"
    LIB: "Liberaterian"


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
        
        self.total_electoral_votes = sum(self.electoral_votes.values())
        self.votes_to_win = (self.total_electoral_votes // 2) + 1


if __name__ == "__main__":

    # create instance
    ec = ElectoralCollege()

    # test results:
    test_results = {
        State.CA = Party.DEM, # 54
        State.FL = Party.REP, # 
        State.NY = Party.DEM,
        State.TX = Party.REP
    }

    # calculate current electoral votes
    vote_totals = ec.calculate_electoral_votes(test_results)

    # check if there is a winner
    has_winner, winner = ec.check_winner(test_results)

    # check uncalled states for remaining paths to victory
    test_uncalled_states = [State.OH, State.PA, State.MI, State.WI]
    remaining_paths = ec.get_remaining_paths(test_results, test_uncalled_states)




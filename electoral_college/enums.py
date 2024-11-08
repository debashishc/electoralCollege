from enum import Enum
from typing import Final

TOTAL_ELECTORAL_VOTES: Final[int] = 538
VOTES_TO_WIN: Final[int] = 270


class State(Enum):
    """
    Enumeration of all US states and DC with their full names.
    Used for consistent state identification throughout the system.
    """

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
    """
    Enumeration of political parties.
    Includes major parties and significant third parties for completeness.
    """

    DEM = "Democrat"
    REP = "Republican"
    IND = "Independent"
    GRN = "Green"  # Fixed inconsistency from GRE
    LIB = "Libertarian"  # Fixed typo


class SplitVoteState(Enum):
    """
    States that can split their electoral votes by congressional district.
    Currently only Maine and Nebraska use this system.

    Reference:
    https://apnews.com/article/nebraska-maine-president-electoral-votes-district-omaha-90382054c29f546fd65a7e7cc5094801
    """

    MAINE = State.ME
    NEBRASKA = State.NE

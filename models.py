from dataclasses import dataclass
from typing import Dict, Optional, Set
from datetime import datetime
from enums import State, Party


@dataclass
class StateInfo:
    """
    Contains detailed information about a state's electoral properties.

    Attributes:
        name: Full name of the state
        electoral_votes: Number of electoral votes
        congressional_districts: Number of congressional districts
        is_split_vote: Whether state can split electoral votes
        region: Geographic region of the state
    """

    name: str
    electoral_votes: int
    congressional_districts: int
    is_split_vote: bool = False
    region: Optional[str] = None


@dataclass
class ElectionResult:
    """
    Stores the results and analysis of an election calculation.

    Attributes:
        year: Election year
        state_results: Mapping of states to winning parties
        vote_totals: Total electoral votes per party
        winner: Winning party if any
        remaining_paths: Analysis of possible paths to victory
        timestamp: When the result was calculated
        notes: Additional information about the result
    """

    year: int
    state_results: Dict[State, Optional[Party]]
    vote_totals: Dict[Party, int]
    winner: Optional[Party]
    remaining_paths: Dict[Party, dict]
    timestamp: datetime = datetime.now()
    notes: Optional[str] = None

    @property
    def has_winner(self) -> bool:
        """Check if there is a winner."""
        return self.winner is not None

from dataclasses import dataclass
from typing import Dict, Optional
from enums import Party
from datetime import datetime

@dataclass
class StateInfo:
    name: str
    electoral_votes: int
    congressional_districts: int
    is_split_vote: bool = False
    region: Optional[str] = None

@dataclass
class ElectionResult:
    vote_totals: Dict[Party, int]
    winner: Optional[Party]
    remaining_paths: Dict[Party, dict]
    timestamp: datetime = datetime.now()

    @property
    def has_winner(self) -> bool:
        return self.winner is not None
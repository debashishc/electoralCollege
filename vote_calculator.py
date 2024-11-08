from typing import Dict, Set, Optional, List, Any, Tuple
from functools import lru_cache
import logging
from datetime import datetime

from .enums import State, Party, Region
from .models import ElectionResult, StateInfo
from .exceptions import InvalidStateError, InvalidPartyError, InvalidVoteCountError
from .config import ElectoralConfig, TOTAL_ELECTORAL_VOTES, VOTES_TO_WIN

logger = logging.getLogger(__name__)

class ElectoralCollege:
    """
    A class representing the United States Electoral College system.
    
    Handles electoral vote calculations, winner determination, and analysis
    of potential paths to victory in presidential elections.
    
    Attributes:
        electoral_votes (Dict[State, int]): Mapping of states to their electoral votes
        total_electoral_votes (int): Total number of electoral votes in the system
        votes_to_win (int): Number of electoral votes needed to win
        config (ElectoralConfig): Configuration instance for the electoral system
    """
    
    def __init__(self) -> None:
        """Initialize the Electoral College calculator."""
        self.config = ElectoralConfig
        
        # Validate configuration before proceeding
        if not self.config.validate_configuration():
            raise InvalidVoteCountError("Electoral configuration is invalid")
            
        self.electoral_votes: Dict[State, int] = {
            state: info.electoral_votes 
            for state, info in self.config.STATE_DATA.items()
        }
        self.total_electoral_votes: int = TOTAL_ELECTORAL_VOTES
        self.votes_to_win: int = VOTES_TO_WIN
        
        logger.info(
            f"Electoral College initialized with {self.total_electoral_votes} "
            f"total votes, {self.votes_to_win} needed to win"
        )

    def get_state_votes(self, state: State) -> int:
        """
        Get electoral votes for a state.
        
        Args:
            state: State to look up
            
        Returns:
            Number of electoral votes for the state
        """
        return self.electoral_votes.get(state, 0)

    def get_state_info(self, state: State) -> StateInfo:
        """
        Get complete information for a state.
        
        Args:
            state: State to look up
            
        Returns:
            StateInfo object containing state details
            
        Raises:
            KeyError: If state not found in configuration
        """
        return self.config.STATE_DATA[state]

    def get_state_summary(self, state: State) -> dict:
        """
        Get a summary of state information.
        
        Args:
            state: State to summarize
            
        Returns:
            Dictionary containing state summary information
        """
        info = self.get_state_info(state)
        return {
            'name': state.value,
            'electoral_votes': info.electoral_votes,
            'region': info.region,
            'is_split_vote': info.is_split_vote,
            'is_swing_state': self.config.is_swing_state(state),
            'historical_leaning': self.config.get_historical_leaning(state)
        }

    def _get_uncalled_states(self, current_results: Dict[State, Optional[Party]]) -> Set[State]:
        """
        Get set of states that haven't been called yet.
        
        Args:
            current_results: Current election results
            
        Returns:
            Set of uncalled states
        """
        return set(self.electoral_votes.keys()) - {
            state for state, party in current_results.items() 
            if party is not None
        }

    def validate_state(self, state: State) -> bool:
        """
        Validate if a state exists and has valid electoral votes.
        
        Args:
            state: State to validate
            
        Returns:
            True if state is valid, False otherwise
        """
        return (
            isinstance(state, State) and 
            state in self.electoral_votes and 
            self.electoral_votes[state] >= 3
        )

    def validate_party(self, party: Optional[Party]) -> bool:
        """
        Validate party, allowing None for uncalled states.
        
        Args:
            party: Party to validate
            
        Returns:
            True if party is valid or None, False otherwise
        """
        return party is None or isinstance(party, Party)
        
    def validate_inputs(self, state_results: Dict[State, Optional[Party]]) -> None:
        """
        Validate election result inputs.
        
        Args:
            state_results: Dictionary mapping states to winning parties
            
        Raises:
            InvalidStateError: If invalid states are found
            InvalidPartyError: If invalid parties are found
            InvalidVoteCountError: If vote counts are invalid
        """
        if not isinstance(state_results, dict):
            raise InvalidStateError("State results must be a dictionary")
            
        invalid_states = [
            state for state in state_results 
            if not self.validate_state(state)
        ]
        if invalid_states:
            raise InvalidStateError(f"Invalid states found: {invalid_states}")
            
        invalid_parties = [
            party for party in state_results.values() 
            if not self.validate_party(party)
        ]
        if invalid_parties:
            raise InvalidPartyError(f"Invalid parties found: {invalid_parties}")
            
        # Validate total votes don't exceed possible total
        called_votes = sum(
            self.get_state_votes(state)
            for state, party in state_results.items()
            if party is not None
        )
        if called_votes > self.total_electoral_votes:
            raise InvalidVoteCountError(
                f"Total called votes ({called_votes}) exceeds maximum "
                f"possible ({self.total_electoral_votes})"
            )
    
    @lru_cache(maxsize=128)
    def calculate_electoral_votes(
        self, 
        state_results: frozenset[tuple[State, Optional[Party]]]
    ) -> Dict[Party, int]:
        """
        Calculate electoral votes for each party.
        
        Args:
            state_results: Frozen set of (State, Party) tuples for caching
            
        Returns:
            Dict mapping parties to their total electoral votes
            
        Raises:
            InvalidStateError: If invalid states are found
            InvalidPartyError: If invalid parties are found
            InvalidVoteCountError: If vote counts are invalid
        """
        results: Dict[Party, int] = {}
        state_results_dict = dict(state_results)
        
        try:
            self.validate_inputs(state_results_dict)
            
            for state, party in state_results_dict.items():
                if party is not None:
                    if self.config.is_split_vote_state(state):
                        votes = self.calculate_split_vote_results(state, state_results_dict)
                        for split_party, split_votes in votes.items():
                            results[split_party] = results.get(split_party, 0) + split_votes
                    else:
                        current_votes = results.get(party, 0)
                        state_votes = self.get_state_votes(state)
                        results[party] = current_votes + state_votes
                    
            logger.debug(f"Vote calculation complete: {results}")
            return results
            
        except Exception as e:
            logger.error(f"Error calculating electoral votes: {e}")
            raise

    def calculate_split_vote_results(
        self, 
        state: State, 
        district_results: Dict[int, Party]
    ) -> Dict[Party, int]:
        """
        Calculate electoral votes for states that can split their votes.
        
        Args:
            state: The split vote state
            district_results: Dictionary mapping congressional districts to winning parties
            
        Returns:
            Dict mapping parties to their electoral votes in this state
        """
        state_info = self.get_state_info(state)
        results: Dict[Party, int] = {}
        
        # Implement ME/NE specific rules here
        logger.info(f"Calculating split vote results for {state.value}")
        return results

    def check_winner(self, state_results: Dict[State, Optional[Party]]) -> ElectionResult:
        """
        Determine if there's a winner based on current results.
        
        Args:
            state_results: Dictionary mapping states to winning parties
            
        Returns:
            ElectionResult object containing results and analysis
        """
        frozen_results = frozenset(state_results.items())
        vote_totals = self.calculate_electoral_votes(frozen_results)
        winner = None
        
        for party, votes in vote_totals.items():
            if votes >= self.votes_to_win:
                winner = party
                break
        
        remaining_paths = self.get_remaining_paths(
            frozen_results,
            frozenset(self._get_uncalled_states(state_results))
        )
        
        return ElectionResult(
            vote_totals=vote_totals,
            winner=winner,
            remaining_paths=remaining_paths,
            year=datetime.now().year,
            state_results=state_results
        )

    @lru_cache(maxsize=64)
    def get_remaining_paths(
        self, 
        current_results: frozenset[tuple[State, Optional[Party]]], 
        uncalled_states: frozenset[State]
    ) -> Dict[Party, dict]:
        """
        Analyze possible paths to victory with remaining uncalled states.
        
        Args:
            current_results: Current state results
            uncalled_states: Set of states not yet called
            
        Returns:
            Dict containing analysis of each party's possible paths to victory
        """
        current_totals = self.calculate_electoral_votes(current_results)
        remaining_votes = sum(self.electoral_votes[state] for state in uncalled_states)
        
        paths = {}
        for party in Party:
            current_votes = current_totals.get(party, 0)
            needed_votes = self.votes_to_win - current_votes
            paths[party] = {
                'current_votes': current_votes,
                'needed_votes': needed_votes,
                'possible': needed_votes <= remaining_votes,
                'minimum_states_needed': self._calculate_minimum_states_needed(
                    needed_votes, uncalled_states)
            }
        
        return paths

    def get_regional_results(
        self, 
        state_results: Dict[State, Optional[Party]]
    ) -> Dict[Region, Dict[Party, int]]:
        """
        Calculate vote totals by region.
        
        Args:
            state_results: Dictionary mapping states to winning parties
            
        Returns:
            Dictionary mapping regions to their vote totals by party
        """
        regional_results = {region: {} for region in Region}
        
        for state, party in state_results.items():
            if party is not None:
                region = Region(self.config.get_region(state))
                state_votes = self.get_state_votes(state)
                current = regional_results[region].get(party, 0)
                regional_results[region][party] = current + state_votes
                
        return regional_results

    def _calculate_minimum_states_needed(
        self, 
        needed_votes: int, 
        available_states: Set[State]
    ) -> int:
        """Calculate the minimum number of states needed to reach vote threshold."""
        if needed_votes <= 0:
            return 0
            
        state_votes = sorted(
            [self.electoral_votes[state] for state in available_states],
            reverse=True
        )
        
        total = 0
        states_needed = 0
        
        for votes in state_votes:
            total += votes
            states_needed += 1
            if total >= needed_votes:
                break
                
        return states_needed if total >= needed_votes else len(available_states) + 1

    def format_percentage(self, value: float) -> str:
        """Format a number as a percentage string."""
        return f"{value:.1f}%"

    def create_election_result(
        self,
        year: int,
        state_results: Dict[State, Optional[Party]],
        notes: Optional[str] = None
    ) -> ElectionResult:
        """Create an ElectionResult object from current results."""
        frozen_results = frozenset(state_results.items())
        vote_totals = self.calculate_electoral_votes(frozen_results)
        
        winner = None
        for party, votes in vote_totals.items():
            if votes >= self.votes_to_win:
                winner = party
                break
        
        remaining_paths = self.get_remaining_paths(
            frozen_results,
            frozenset(self._get_uncalled_states(state_results))
        )
        
        return ElectionResult(
            year=year,
            state_results=state_results,
            vote_totals=vote_totals,
            winner=winner,
            remaining_paths=remaining_paths,
            timestamp=datetime.now(),
            notes=notes
        )
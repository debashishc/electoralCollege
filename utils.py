from typing import Dict, Optional
from enums import State, Party


def get_state_votes(electoral_votes: Dict[State, int], state: State) -> int:
    """
    Get the number of electoral votes for a state.
    
    Args:
        electoral_votes: Dictionary mapping states to their electoral votes
        state: State to look up
        
    Returns:
        Number of electoral votes for the state, 0 if state not found
    """
    return electoral_votes.get(state, 0)


def validate_state(state: State) -> bool:
    """
    Validate if a state exists in the enumeration.
    
    Args:
        state: State to validate
        
    Returns:
        True if valid state, False otherwise
    """
    return isinstance(state, State)


def validate_party(party: Optional[Party]) -> bool:
    """
    Validate if a party exists in the enumeration.
    Allows None for uncalled states.
    
    Args:
        party: Party to validate
        
    Returns:
        True if valid party or None, False otherwise
    """
    return party is None or isinstance(party, Party)


def format_percentage(value: float) -> str:
    """
    Format a number as a percentage string.
    
    Args:
        value: Number to format
        
    Returns:
        Formatted percentage string
    """
    return f"{value:.1f}%"
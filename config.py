from enums import State
from typing import Dict, List
from models import StateInfo
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class ElectoralConfig:
    """Configuration for the Electoral College system."""
    
    STATE_DATA: Dict[State, StateInfo] = {
        # Northeast Region
        State.ME: StateInfo("Maine", 4, 2, True, "Northeast"),
        State.NH: StateInfo("New Hampshire", 4, 1, False, "Northeast"),
        State.VT: StateInfo("Vermont", 3, 1, False, "Northeast"),
        State.MA: StateInfo("Massachusetts", 11, 9, False, "Northeast"),
        State.RI: StateInfo("Rhode Island", 4, 2, False, "Northeast"),
        State.CT: StateInfo("Connecticut", 7, 5, False, "Northeast"),
        State.NY: StateInfo("New York", 28, 26, False, "Northeast"),
        State.NJ: StateInfo("New Jersey", 14, 12, False, "Northeast"),
        State.PA: StateInfo("Pennsylvania", 19, 17, False, "Northeast"),

        # Midwest Region
        State.OH: StateInfo("Ohio", 17, 15, False, "Midwest"),
        State.IN: StateInfo("Indiana", 11, 9, False, "Midwest"),
        State.IL: StateInfo("Illinois", 19, 17, False, "Midwest"),
        State.MI: StateInfo("Michigan", 15, 13, False, "Midwest"),
        State.WI: StateInfo("Wisconsin", 10, 8, False, "Midwest"),
        State.MN: StateInfo("Minnesota", 10, 8, False, "Midwest"),
        State.IA: StateInfo("Iowa", 6, 4, False, "Midwest"),
        State.MO: StateInfo("Missouri", 10, 8, False, "Midwest"),
        State.ND: StateInfo("North Dakota", 3, 1, False, "Midwest"),
        State.SD: StateInfo("South Dakota", 3, 1, False, "Midwest"),
        State.NE: StateInfo("Nebraska", 5, 3, True, "Midwest"),
        State.KS: StateInfo("Kansas", 6, 4, False, "Midwest"),

        # South Region
        State.DE: StateInfo("Delaware", 3, 1, False, "South"),
        State.MD: StateInfo("Maryland", 10, 8, False, "South"),
        State.VA: StateInfo("Virginia", 13, 11, False, "South"),
        State.WV: StateInfo("West Virginia", 4, 2, False, "South"),
        State.NC: StateInfo("North Carolina", 16, 14, False, "South"),
        State.SC: StateInfo("South Carolina", 9, 7, False, "South"),
        State.GA: StateInfo("Georgia", 16, 14, False, "South"),
        State.FL: StateInfo("Florida", 30, 28, False, "South"),
        State.KY: StateInfo("Kentucky", 8, 6, False, "South"),
        State.TN: StateInfo("Tennessee", 11, 9, False, "South"),
        State.AL: StateInfo("Alabama", 9, 7, False, "South"),
        State.MS: StateInfo("Mississippi", 6, 4, False, "South"),
        State.AR: StateInfo("Arkansas", 6, 4, False, "South"),
        State.LA: StateInfo("Louisiana", 8, 6, False, "South"),
        State.OK: StateInfo("Oklahoma", 7, 5, False, "South"),
        State.TX: StateInfo("Texas", 40, 38, False, "South"),

        # West Region
        State.MT: StateInfo("Montana", 4, 2, False, "West"),
        State.ID: StateInfo("Idaho", 4, 2, False, "West"),
        State.WY: StateInfo("Wyoming", 3, 1, False, "West"),
        State.CO: StateInfo("Colorado", 10, 8, False, "West"),
        State.NM: StateInfo("New Mexico", 5, 3, False, "West"),
        State.AZ: StateInfo("Arizona", 11, 9, False, "West"),
        State.UT: StateInfo("Utah", 6, 4, False, "West"),
        State.NV: StateInfo("Nevada", 6, 4, False, "West"),
        State.WA: StateInfo("Washington", 12, 10, False, "West"),
        State.OR: StateInfo("Oregon", 8, 6, False, "West"),
        State.CA: StateInfo("California", 54, 52, False, "West"),
        State.AK: StateInfo("Alaska", 3, 1, False, "West"),
        State.HI: StateInfo("Hawaii", 4, 2, False, "West"),

        # District of Columbia
        State.DC: StateInfo("District of Columbia", 3, 1, False, "District")
        # State.PR -- nope, Puerto Rico can't vote, aaargh
    }
    
    REGIONS = {
        "Northeast": ["ME", "NH", "VT", "MA", "RI", "CT", "NY", "NJ", "PA"],
        "Midwest": ["OH", "IN", "IL", "MI", "WI", "MN", "IA", "MO", "ND", "SD", "NE", "KS"],
        "South": ["DE", "MD", "VA", "WV", "NC", "SC", "GA", "FL", "KY", "TN", "AL", "MS", "AR", "LA", "OK", "TX"],
        "West": ["MT", "ID", "WY", "CO", "NM", "AZ", "UT", "NV", "WA", "OR", "CA", "AK", "HI"],
        "District": ["DC"]
    }
    
    TOTAL_ELECTORAL_VOTES: int = sum(info.electoral_votes for info in STATE_DATA.values())
    VOTES_TO_WIN: int = (TOTAL_ELECTORAL_VOTES // 2) + 1
    
    # States that split electoral votes
    SPLIT_VOTE_STATES = ["ME", "NE"]
    
    # Swing states (states that have been competitive in recent elections)
    SWING_STATES = ["AZ", "GA", "MI", "NV", "PA", "WI"]
    
    @classmethod
    def get_region(cls, state: State) -> str:
        """Get the region for a given state."""
        return cls.STATE_DATA[state].region
    
    @classmethod
    def get_states_in_region(cls, region: str) -> List[State]:
        """Get all states in a given region."""
        return [State[state] for state in cls.REGIONS.get(region, [])]
    
    @classmethod
    def is_swing_state(cls, state: State) -> bool:
        """Check if a state is considered a swing state."""
        return state.name in cls.SWING_STATES
    
    @classmethod
    def is_split_vote_state(cls, state: State) -> bool:
        """Check if a state splits its electoral votes."""
        return state.name in cls.SPLIT_VOTE_STATES
    
    @classmethod
    def get_congressional_districts(cls, state: State) -> int:
        """Get the number of congressional districts for a state."""
        return cls.STATE_DATA[state].congressional_districts

    @classmethod
    def validate_configuration(cls) -> bool:
        """
        Validate the electoral configuration.
        
        Checks:
        1. Total electoral votes = 538
        2. All states have at least 3 electoral votes
        3. Congressional districts match electoral votes - 2
        4. All states are assigned to regions
        """
        try:
            # Check total electoral votes
            if cls.TOTAL_ELECTORAL_VOTES != 538:
                raise ValueError(f"Total electoral votes must be 538, got {cls.TOTAL_ELECTORAL_VOTES}")
            
            # Check minimum electoral votes and congressional districts
            for state, info in cls.STATE_DATA.items():
                if info.electoral_votes < 3:
                    raise ValueError(f"{state.name} has less than 3 electoral votes")
                    
                # Check congressional districts (electoral votes = districts + 2)
                if info.electoral_votes != info.congressional_districts + 2:
                    raise ValueError(
                        f"{state.name} congressional districts don't match electoral votes"
                    )
            
            # Check all states are in regions
            all_region_states = set()
            for states in cls.REGIONS.values():
                all_region_states.update(states)
                
            if len(all_region_states) != len(State):
                raise ValueError("Not all states are assigned to regions")
            
            return True
            
        except Exception as e:
            print(f"Configuration validation failed: {str(e)}")
            return False
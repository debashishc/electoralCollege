from enum import Enum
from typing import Dict, List, Final, Set, Optional
from dataclasses import dataclass
from models import StateInfo
import logging
from enums import State, Party


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# constants
TOTAL_ELECTORAL_VOTES: Final[int] = 538
VOTES_TO_WIN: Final[int] = 270
MIN_STATE_VOTES: Final[int] = 3

class Region(Enum):
    """Enumeration of US geographic regions"""
    NORTHEAST = "Northeast"
    MIDWEST = "Midwest"
    SOUTH = "South"
    WEST = "West"
    DISTRICT = "District"

class ElectoralConfig:
    """Configuration for the Electoral College system."""
    
    STATE_DATA: Final[Dict[State, StateInfo]] = { 
        # Northeast Region
        State.ME: StateInfo("Maine", 4, 2, True, Region.NORTHEAST.value),
        State.NH: StateInfo("New Hampshire", 4, 1, False, Region.NORTHEAST.value),
        State.VT: StateInfo("Vermont", 3, 1, False, Region.NORTHEAST.value),
        State.MA: StateInfo("Massachusetts", 11, 9, False, Region.NORTHEAST.value),
        State.RI: StateInfo("Rhode Island", 4, 2, False, Region.NORTHEAST.value),
        State.CT: StateInfo("Connecticut", 7, 5, False, Region.NORTHEAST.value),
        State.NY: StateInfo("New York", 28, 26, False, Region.NORTHEAST.value),
        State.NJ: StateInfo("New Jersey", 14, 12, False, Region.NORTHEAST.value),
        State.PA: StateInfo("Pennsylvania", 19, 17, False, Region.NORTHEAST.value),

        # Midwest Region
        State.OH: StateInfo("Ohio", 17, 15, False, Region.MIDWEST.value),
        State.IN: StateInfo("Indiana", 11, 9, False, Region.MIDWEST.value),
        State.IL: StateInfo("Illinois", 19, 17, False, Region.MIDWEST.value),
        State.MI: StateInfo("Michigan", 15, 13, False, Region.MIDWEST.value),
        State.WI: StateInfo("Wisconsin", 10, 8, False, Region.MIDWEST.value),
        State.MN: StateInfo("Minnesota", 10, 8, False, Region.MIDWEST.value),
        State.IA: StateInfo("Iowa", 6, 4, False, Region.MIDWEST.value),
        State.MO: StateInfo("Missouri", 10, 8, False, Region.MIDWEST.value),
        State.ND: StateInfo("North Dakota", 3, 1, False, Region.MIDWEST.value),
        State.SD: StateInfo("South Dakota", 3, 1, False, Region.MIDWEST.value),
        State.NE: StateInfo("Nebraska", 5, 3, True, Region.MIDWEST.value),
        State.KS: StateInfo("Kansas", 6, 4, False, Region.MIDWEST.value),

        # South Region
        State.DE: StateInfo("Delaware", 3, 1, False, Region.SOUTH.value),
        State.MD: StateInfo("Maryland", 10, 8, False, Region.SOUTH.value),
        State.VA: StateInfo("Virginia", 13, 11, False, Region.SOUTH.value),
        State.WV: StateInfo("West Virginia", 4, 2, False, Region.SOUTH.value),
        State.NC: StateInfo("North Carolina", 16, 14, False, Region.SOUTH.value),
        State.SC: StateInfo("South Carolina", 9, 7, False, Region.SOUTH.value),
        State.GA: StateInfo("Georgia", 16, 14, False, Region.SOUTH.value),
        State.FL: StateInfo("Florida", 30, 28, False, Region.SOUTH.value),
        State.KY: StateInfo("Kentucky", 8, 6, False, Region.SOUTH.value),
        State.TN: StateInfo("Tennessee", 11, 9, False, Region.SOUTH.value),
        State.AL: StateInfo("Alabama", 9, 7, False, Region.SOUTH.value),
        State.MS: StateInfo("Mississippi", 6, 4, False, Region.SOUTH.value),
        State.AR: StateInfo("Arkansas", 6, 4, False, Region.SOUTH.value),
        State.LA: StateInfo("Louisiana", 8, 6, False, Region.SOUTH.value),
        State.OK: StateInfo("Oklahoma", 7, 5, False, Region.SOUTH.value),
        State.TX: StateInfo("Texas", 40, 38, False, Region.SOUTH.value),

        # West Region
        State.MT: StateInfo("Montana", 4, 2, False, Region.WEST.value),
        State.ID: StateInfo("Idaho", 4, 2, False, Region.WEST.value),
        State.WY: StateInfo("Wyoming", 3, 1, False, Region.WEST.value),
        State.CO: StateInfo("Colorado", 10, 8, False, Region.WEST.value),
        State.NM: StateInfo("New Mexico", 5, 3, False, Region.WEST.value),
        State.AZ: StateInfo("Arizona", 11, 9, False, Region.WEST.value),
        State.UT: StateInfo("Utah", 6, 4, False, Region.WEST.value),
        State.NV: StateInfo("Nevada", 6, 4, False, Region.WEST.value),
        State.WA: StateInfo("Washington", 12, 10, False, Region.WEST.value),
        State.OR: StateInfo("Oregon", 8, 6, False, Region.WEST.value),
        State.CA: StateInfo("California", 54, 52, False, Region.WEST.value),
        State.AK: StateInfo("Alaska", 3, 1, False, Region.WEST.value),
        State.HI: StateInfo("Hawaii", 4, 2, False, Region.WEST.value),

        # District of Columbia
        State.DC: StateInfo("District of Columbia", 3, 1, False, Region.DISTRICT.value)
        # State.PR -- nope, Puerto Rico can't vote, aaargh
    }
    
    REGIONS: Final[Dict[Region, List[str]]] = {
        Region.NORTHEAST: ["ME", "NH", "VT", "MA", "RI", "CT", "NY", "NJ", "PA"],
        Region.MIDWEST: ["OH", "IN", "IL", "MI", "WI", "MN", "IA", "MO", "ND", "SD", "NE", "KS"],
        Region.SOUTH: ["DE", "MD", "VA", "WV", "NC", "SC", "GA", "FL", "KY", "TN", "AL", "MS", "AR", "LA", "OK", "TX"],
        Region.WEST: ["MT", "ID", "WY", "CO", "NM", "AZ", "UT", "NV", "WA", "OR", "CA", "AK", "HI"],
        Region.DISTRICT: ["DC"]
    }
    
    # Electoral vote calculations
    TOTAL_ELECTORAL_VOTES: Final[int] = TOTAL_ELECTORAL_VOTES
    VOTES_TO_WIN: Final[int] = VOTES_TO_WIN
    
    # Special state classifications
    SPLIT_VOTE_STATES: Final[Set[str]] = {"ME", "NE"}  # Using set for O(1) lookup
    SWING_STATES: Final[Set[str]] = {"AZ", "GA", "MI", "NV", "PA", "WI"}
    
    # Historical electoral patterns
    HISTORICALLY_DEMOCRATIC: Final[Set[str]] = {"CA", "NY", "IL", "MA"}  # Example states
    HISTORICALLY_REPUBLICAN: Final[Set[str]] = {"TX", "WY", "ID", "UT"}  # Example states
    
    @classmethod
    def get_region(cls, state: State) -> str:
        """
        Get the region for a given state.
        
        Args:
            state: State enum value
            
        Returns:
            Region name as string
            
        Raises:
            KeyError: If state not found in configuration
        """
        try:
            return cls.STATE_DATA[state].region
        except KeyError:
            logger.error(f"Region not found for state: {state}")
            raise

    @classmethod
    def get_states_in_region(cls, region: Region) -> List[State]:
        """
        Get all states in a given region.
        
        Args:
            region: Region enum value
            
        Returns:
            List of states in the region
        """
        return [State[state] for state in cls.REGIONS.get(region, [])]

    @classmethod
    def is_swing_state(cls, state: State) -> bool:
        """
        Check if a state is considered a swing state.
        
        Args:
            state: State to check
            
        Returns:
            True if swing state, False otherwise
        """
        return state.name in cls.SWING_STATES

    @classmethod
    def get_historical_leaning(cls, state: State) -> Optional[Party]:
        """
        Get historical voting pattern of a state.
        
        Args:
            state: State to check
            
        Returns:
            Party that historically wins the state, or None if competitive
        """
        if state.name in cls.HISTORICALLY_DEMOCRATIC:
            return Party.DEM
        elif state.name in cls.HISTORICALLY_REPUBLICAN:
            return Party.REP
        return None

    @classmethod
    def validate_configuration(cls) -> bool:
        """
        Validate the electoral configuration.
        
        Performs comprehensive validation of the configuration data.
        
        Returns:
            True if configuration is valid, False otherwise
        
        Logs detailed error messages for any validation failures.
        """
        try:
            # Check total electoral votes
            if cls.TOTAL_ELECTORAL_VOTES != TOTAL_ELECTORAL_VOTES:
                raise ValueError(
                    f"Total electoral votes must be {TOTAL_ELECTORAL_VOTES}, "
                    f"got {cls.TOTAL_ELECTORAL_VOTES}"
                )
            
            # Validate state data
            all_states = set(State)
            configured_states = set(cls.STATE_DATA.keys())
            
            # Check for missing or extra states
            if all_states != configured_states:
                missing = all_states - configured_states
                extra = configured_states - all_states
                if missing:
                    logger.error(f"Missing states: {missing}")
                if extra:
                    logger.error(f"Extra states: {extra}")
                raise ValueError("State configuration mismatch")
            
            # Validate each state's data
            for state, info in cls.STATE_DATA.items():
                # Check minimum electoral votes
                if info.electoral_votes < MIN_STATE_VOTES:
                    raise ValueError(
                        f"{state.name} has less than {MIN_STATE_VOTES} electoral votes"
                    )
                
                # Validate congressional districts
                if info.electoral_votes != info.congressional_districts + 2:
                    raise ValueError(
                        f"{state.name} congressional districts don't match electoral votes"
                    )
                
                # Validate region assignment
                if not info.region or not any(
                    state.name in states 
                    for states in cls.REGIONS.values()
                ):
                    raise ValueError(f"{state.name} not properly assigned to a region")
            
            logger.info("Configuration validation successful")
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {str(e)}")
            return False

    @classmethod
    def get_region_summary(cls, region: Region) -> dict:
        """
        Get summary statistics for a region.
        
        Args:
            region: Region to summarize
            
        Returns:
            Dictionary containing regional statistics
        """
        states = cls.get_states_in_region(region)
        return {
            'name': region.value,
            'states': len(states),
            'electoral_votes': sum(
                cls.STATE_DATA[state].electoral_votes 
                for state in states
            ),
            'swing_states': sum(
                1 for state in states 
                if cls.is_swing_state(state)
            )
        }
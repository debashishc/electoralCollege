# Electoral College 

Implementing the US Electoral College system for analyzing presidential election scenarios, can potentially predict pathways left for parties to win. Implementation was documented and refactored using Claude AI.

## Features

### Core Functionality
- Electoral vote analysis for all 50 states and DC
- Vote calculations and winner determination
- Split electoral vote handling for Maine and Nebraska

### Analysis Capabilities
- Path to victory calculations
- Regional vote analysis
- Swing state identification
- Historical voting pattern analysis
- Minimum state combinations needed for victory

### Data Organization
- Geographic regional grouping
- State-level detailed information
- Congressional district tracking
- Historical voting patterns

## Usage

### Basic Example
```python
from vote_calculator import ElectoralCollege
from enums import State, Party

# Initialize calculator
ec = ElectoralCollege()

# Create test results
results = {
    State.CA: Party.DEM,    # California (54 votes)
    State.TX: Party.REP,    # Texas (40 votes)
    State.FL: Party.REP,    # Florida (30 votes)
    State.NY: Party.DEM,    # New York (28 votes)
    State.PA: None,         # Pennsylvania - uncalled
}

# Check results
election_result = ec.check_winner(results)

if election_result.has_winner:
    print(f"Winner: {election_result.winner.value}")
    print(f"Electoral Votes: {election_result.vote_totals[election_result.winner]}")
else:
    print("No winner yet")
```

### Regional Analysis
```python
# Get regional breakdown
regional_results = ec.get_regional_results(results)
for region, votes in regional_results.items():
    print(f"\n{region.value}:")
    for party, vote_count in votes.items():
        print(f"{party.value}: {vote_count} electoral votes")
```

### Path to Victory Analysis
```python
# Analyze remaining paths
paths = ec.get_remaining_paths(
    frozenset(results.items()),
    frozenset(ec._get_uncalled_states(results))
)

for party, path in paths.items():
    print(f"\n{party.value}:")
    print(f"Current votes: {path['current_votes']}")
    print(f"Needed for victory: {path['needed_votes']}")
    print(f"Victory possible: {path['possible']}")
```

## Project Structure

```
├── __init__.py
├── config.py         # Electoral configuration and constants
├── enums.py         # State and Party enumerations
├── exceptions.py    # Custom exception classes
├── models.py        # Data models and structures
└── vote_calculator.py # Main calculation logic
```

## Data Models

### State Information
```python
@dataclass
class StateInfo:
    name: str                # Full state name
    electoral_votes: int     # Number of electoral votes
    congressional_districts: int  # Number of districts
    is_split_vote: bool = False  # ME/NE split vote status
    region: Optional[str] = None # Geographic region
```

### Election Results
```python
@dataclass
class ElectionResult:
    year: int
    state_results: Dict[State, Optional[Party]]
    vote_totals: Dict[Party, int]
    winner: Optional[Party]
    remaining_paths: Dict[Party, dict]
    timestamp: datetime = datetime.now()
    notes: Optional[str] = None
```

## Features in Detail

### State Vote Handling
- Accurate electoral vote counts for all states
- Support for split electoral votes (ME/NE)
- Validation of vote counts and state data
- Regional and district-level organization

### Analysis Tools
- Victory path calculation
- Regional vote distribution
- Swing state analysis
- Historical pattern comparison
- Minimum state combinations

### Data Validation
- Input validation
- State/Party verification
- Vote count validation
- Configuration integrity checks

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Type Checking
```bash
mypy electoral_college
```

### Code Formatting
```bash
black electoral_college
```

## Notes

- Electoral vote counts based on 2024 election data
- Includes special handling for Maine and Nebraska's district-based allocation
- Swing state identification based on recent election patterns
- Historical voting patterns may be updated as new data becomes available

## TODO

- [ ] Add visualization capabilities
- [ ] Implement detailed split vote calculations
- [ ] Add historical election data
- [ ] Create CLI interface
- [ ] Add more test coverage
- [ ] Add interactive visualization dashboard
- [ ] Implement real-time result updates
- [ ] Add demographic analysis tools

## Acknowledgments

- Electoral vote data from official government sources
- Historical patterns based on past election results
- Regional groupings based on US Census Bureau definitions
- Anthropic Claude AI for documentation and refactoring

## Questions and Support

For questions and support, please open an issue in the GitHub repository.
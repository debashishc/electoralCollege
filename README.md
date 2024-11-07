
# Electoral College Calculator

A Python implementation of the United States Electoral College system for analyzing presidential election scenarios.

## Features

- Complete electoral vote tracking for all 50 states and DC
- Support for split electoral votes (Maine and Nebraska)
- Regional analysis capabilities
- Swing state identification
- Path to victory calculations
- Election result persistence

<!-- ## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/electoral-college.git
cd electoral-college
```

2. Install dependencies:
```bash
pip install -r requirements.txt
``` -->

## Usage

Basic usage:

```python
from vote_calculator import ElectoralCollege
from enums import State, Party

# Initialize the calculator
ec = ElectoralCollege()

# Create some test results
results = {
    State.CA: Party.DEM,  # California
    State.TX: Party.REP,  # Texas
    State.FL: Party.REP,  # Florida
    State.NY: Party.DEM,  # New York
}

# Check the results
election_result = ec.check_winner(results)

if election_result.has_winner:
    print(f"Winner: {election_result.winner.value}")
else:
    print("No winner yet")
```

## Project Structure

```
electoral_college/
├── config.py         # Configuration and state data
├── enums.py         # State and Party enumerations
├── exceptions.py    # Custom exceptions
├── models.py        # Data models
├── utils.py         # Utility functions
└── vote_calculator.py # Main calculation logic
```

## Features in Detail

### State Information
- Electoral votes per state
- Congressional districts
- Regional grouping
- Split vote state handling

### Analysis Capabilities
- Current vote totals
- Remaining paths to victory
- Minimum states needed to win
- Regional vote distribution

### Data Validation
- Vote count validation
- State/Party validation
- Configuration validation

## Notes

- Electoral vote counts are based on 2024 election data (at a certain time, not sure when)
- Includes special handling for Maine and Nebraska's district-based allocation
- Swing state identification based on recent election patterns

## TODO

- [ ] Fix installation instructions
- [ ] Add visualization capabilities
- [ ] Implement detailed split vote calculations
- [ ] Add historical election data
- [ ] Create CLI interface
- [ ] Add more test cases
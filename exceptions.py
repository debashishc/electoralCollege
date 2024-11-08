class ElectoralCollegeError(Exception):
    """Base exception class for all Electoral College related errors."""

    pass


class InvalidStateError(ElectoralCollegeError):
    """
    Raised when an invalid state is provided or when state data is incorrect.
    Examples: Invalid state code, missing state data, etc.
    """

    pass


class InvalidPartyError(ElectoralCollegeError):
    """
    Raised when an invalid party is provided or when party data is incorrect.
    Examples: Invalid party code, inconsistent party data, etc.
    """

    pass


class InvalidVoteCountError(ElectoralCollegeError):
    """
    Raised when vote counts are invalid.
    Examples:
    - Total electoral votes ≠ 538
    - Negative vote counts
    - Vote counts exceed state maximum
    """

    pass

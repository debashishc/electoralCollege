class ElectoralCollegeError(Exception):
    """Base exception"""
    pass

class InvalidStateError(ElectoralCollegeError):
    """Raised for an invalid state"""
    pass

class InvalidPartyError(ElectoralCollegeError):
    """Raised for an invalid party"""
    pass

class InvalidVoteCountError(ElectoralCollegeError):
    """Raised for invalid vote counts, checked for total votes"""
    pass

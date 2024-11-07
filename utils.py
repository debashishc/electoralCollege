from enums import State

def get_state_votes(self, state: State) -> int:
    return self.electoral_votes.get(state, 0)

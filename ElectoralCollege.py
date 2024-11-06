
class State:
    pass

class Party:
    pass

class ElectoralCollege:
    pass


if __name__ == "__main__":

    # create instance
    ec = ElectoralCollege()

    # test results:
    test_results = {
        State.CA = Party.Dem,
        State.FL = Party.Rep,
        State.NY = Party.Dem,
        State.TX = Party.Rep
    }

    # calculate current electoral votes
    vote_totals = ec.calculate_electoral_votes(test_results)

    # check if there is a winner
    has_winner, winner = ec.check_winner(test_results)

    # check uncalled states for remaining paths to victory
    test_uncalled_states = [State.OH, State.PA, State.MI, State.WI]
    remaining_paths = ec.get_remaining_paths(test_results, test_uncalled_states)




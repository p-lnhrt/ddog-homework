import ddog.processing

import pandas as pd


def test_triple_counter_compute():
    """
    Given a `pandas.DataFrame` where only a single team triple has a player count above the given threshold,
    When I pass it to the `ddog.processing.TripleCounter.compute` method,
    Then I should be returned a list of (team triple, player count) of length one.
    """
    df = pd.DataFrame(data={
        'league': 'NL',
        'team': ['A', 'B', 'C', 'A', 'A', 'B', 'C', 'A', 'B', 'C'],
        'player-id': ['Bob', 'Bob', 'Bob', 'Ben', 'Joe', 'Joe', 'Joe', 'Pete', 'Pete', 'Pete']
    })

    triple_counter = ddog.processing.TripleCounter(min_player_count=2)
    res = triple_counter.compute(df=df)
    exp = [(frozenset(['A-NL', 'B-NL', 'C-NL']), 3)]
    assert res == exp


def test_triple_counter_compute_no_triples():
    """
    Given a `pandas.DataFrame` where no team triple has a player count above the given threshold,
    When I pass it to the `ddog.processing.TripleCounter.compute` method,
    Then I should be returned an empty list.
    """
    df = pd.DataFrame(data={
        'league': 'NL',
        'team': ['A', 'B', 'C', 'A', 'C', 'D', 'E', 'D', 'B', 'C'],
        'player-id': ['Bob', 'Bob', 'Bob', 'Ben', 'Joe', 'Joe', 'Joe', 'Pete', 'Pete', 'Pete']
    })

    triple_counter = ddog.processing.TripleCounter(min_player_count=2)
    res = triple_counter.compute(df=df)
    exp = list()
    assert res == exp

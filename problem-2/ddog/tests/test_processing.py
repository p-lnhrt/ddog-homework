import ddog.processing

import pandas as pd


def test_triple_counter_compute():
    df = pd.DataFrame(data={
        'league': 'NL',
        'team': ['A', 'B', 'C', 'A', 'A', 'B', 'C', 'A', 'B', 'C'],
        'player': ['Bob', 'Bob', 'Bob', 'Ben', 'Joe', 'Joe', 'Joe', 'Pete', 'Pete', 'Pete']
    })

    triple_counter = ddog.processing.TripleCounter(min_player_count=2)
    res = triple_counter.compute(df=df)
    exp = [(frozenset(['A-NL', 'B-NL', 'C-NL']), 3)]
    assert res == exp


def test_triple_counter_compute_no_triples():
    df = pd.DataFrame(data={
        'league': 'NL',
        'team': ['A', 'B', 'C', 'A', 'C', 'D', 'E', 'D', 'B', 'C'],
        'player': ['Bob', 'Bob', 'Bob', 'Ben', 'Joe', 'Joe', 'Joe', 'Pete', 'Pete', 'Pete']
    })

    triple_counter = ddog.processing.TripleCounter(min_player_count=2)
    res = triple_counter.compute(df=df)
    exp = list()
    assert res == exp

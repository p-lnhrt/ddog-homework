import unittest.mock as mock

import ddog.output


def test_preprocess_triples():
    """
    Given a list of (team triple, player count) tuples,
    When I pass it to a function decorated with `ddog.output.preprocess_triples`,
    Then the decorated function should be passed a list of formatted strings sorted in decreasing player count order.
    """
    mock_sink = mock.Mock()
    func = mock.Mock()
    decorated_func = ddog.output.preprocess_triples(func)
    triples = [(frozenset(['A', 'B', 'C']), 4), (frozenset(['D', 'E', 'F']), 1), (frozenset(['G', 'H', 'I']), 10)]
    formatted_triples = ['Team triple: G|H|I - Count: 10',
                         'Team triple: A|B|C - Count: 4',
                         'Team triple: D|E|F - Count: 1']

    decorated_func(self=mock_sink, triples=triples)
    func.assert_called_with(mock_sink, formatted_triples)


@mock.patch('logging.warning')
def test_preprocess_triples_no_triples(mock_warning):
    """
    Given an empty list of (team triple, player count) tuples,
    When I pass it to a function decorated with `ddog.output.preprocess_triples`,
    Then the `logging.warning` functions should be called twice and the decorated function should not be called.
    """
    mock_sink = mock.Mock()
    func = mock.Mock()
    decorated_func = ddog.output.preprocess_triples(func)
    triples = list()
    decorated_func(self=mock_sink, triples=triples)
    assert mock_warning.call_count == 2
    func.assert_not_called()

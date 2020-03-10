import argparse
import pytest
import unittest.mock as mock

import ddog.cli


def test_positive_integer_pos_int():
    res = ddog.cli.positive_integer(string='10')
    exp = 10
    assert res == exp


def test_positive_integer_neg_int():
    with pytest.raises(argparse.ArgumentTypeError):
        ddog.cli.positive_integer(string='-10')


def test_positive_integer_float():
    with pytest.raises(argparse.ArgumentTypeError):
        ddog.cli.positive_integer(string='10.5')


def test_positive_integer_invalid_string():
    with pytest.raises(argparse.ArgumentTypeError):
        ddog.cli.positive_integer(string='abc')


def test_validate_args_valid_from_to():
    mock_parser = mock.Mock()
    mock_parser.min_year_arg_name = 'from'
    mock_parser.max_year_arg_name = 'to'
    args = {'from': 1871, 'to': 2014}
    res = ddog.cli.CliArgParser._validate_args(self=mock_parser, args=args)
    assert res == args


def test_validate_args_invalid_from_to():
    mock_parser = mock.Mock()
    mock_parser.min_year_arg_name = 'from'
    mock_parser.max_year_arg_name = 'to'
    args = {'from': 1910, 'to': 1900}
    with pytest.raises(ValueError):
        ddog.cli.CliArgParser._validate_args(self=mock_parser, args=args)


def test_parse_args():
    config = {'DEFAULT': {'MinYear': '1871', 'MaxYear': '2014'}}
    parser = ddog.cli.CliArgParser(config=config)
    args = ['--from', '1900', '--to', '1910', '--tmp', '/path/to/tmp',
            '--players', '40', '--sink', 'console', '--remove', 'True']

    res = parser.parse_args(args=args)
    exp = {
        'from': 1900,
        'to': 1910,
        'tmp': '/path/to/tmp',
        'players': 40,
        'sink': 'console',
        'remove': True
    }

    assert res == exp
import argparse
import pytest
import unittest.mock as mock

import ddog.cli
import ddog.constants as csts


def test_positive_integer_pos_int():
    """
    Given a positive integer string,
    When I pass it to `ddog.cli.positive_integer` function,
    Then I should be returned the corresponding integer object.
    """
    res = ddog.cli.positive_integer(string='10')
    exp = 10
    assert res == exp


def test_positive_integer_neg_int():
    """
    Given a negative integer string,
    When I pass it to `ddog.cli.positive_integer` function,
    Then an `argparse.ArgumentTypeError` error should be raised.
    """
    with pytest.raises(argparse.ArgumentTypeError):
        ddog.cli.positive_integer(string='-10')


def test_positive_integer_float():
    """
    Given a float string,
    When I pass it to `ddog.cli.positive_integer` function,
    Then an `argparse.ArgumentTypeError` error should be raised.
    """
    with pytest.raises(argparse.ArgumentTypeError):
        ddog.cli.positive_integer(string='10.5')


def test_positive_integer_invalid_string():
    """
    Given a non-numeric string,
    When I pass it to `ddog.cli.positive_integer` function,
    Then an `argparse.ArgumentTypeError` error should be raised.
    """
    with pytest.raises(argparse.ArgumentTypeError):
        ddog.cli.positive_integer(string='abc')


def test_validate_args_valid_from_to():
    """
    Given a set of parsed CLI arguments with the minimum year argument being lower than the maximum year argument,
    When I pass it to the `ddog.cli.CliArgParser._validate_args` method,
    Then the function should return the set of arguments unchanged.
    """
    min_year_arg_name = csts.CLI_MIN_YEAR_ARG
    max_year_arg_name = csts.CLI_MAX_YEAR_ARG
    mock_parser = mock.Mock()
    mock_parser.min_year_arg_name = min_year_arg_name
    mock_parser.max_year_arg_name = max_year_arg_name
    args = {min_year_arg_name: 1871, max_year_arg_name: 2014}
    res = ddog.cli.CliArgParser._validate_args(self=mock_parser, args=args)
    assert res == args


def test_validate_args_invalid_from_to():
    """
    Given a set of parsed CLI arguments with the minimum year argument being greater than the maximum year argument,
    When I pass it to the `ddog.cli.CliArgParser._validate_args` method,
    Then a `ValueError` should be raised.
    """
    min_year_arg_name = csts.CLI_MIN_YEAR_ARG
    max_year_arg_name = csts.CLI_MAX_YEAR_ARG
    mock_parser = mock.Mock()
    mock_parser.min_year_arg_name = min_year_arg_name
    mock_parser.max_year_arg_name = max_year_arg_name
    args = {min_year_arg_name: 1910, max_year_arg_name: 1900}
    with pytest.raises(ValueError):
        ddog.cli.CliArgParser._validate_args(self=mock_parser, args=args)


def test_parse_args():
    """
    Given a list of command line arguments, a configuration object and a `ddog.cli.CliArgParser` object,
    When I pass the list to the `ddog.cli.CliArgParser.parse_args` method,
    Then I should be returned a dictionary of parsed arguments with the appropriate type.
    """
    min_year_arg_name = csts.CLI_MIN_YEAR_ARG
    max_year_arg_name = csts.CLI_MAX_YEAR_ARG
    tmp_dir_arg_name = csts.CLI_TMP_DIR_ARG
    min_players_arg_name = csts.CLI_MIN_PLAYERS_ARG
    output_arg_name = csts.CLI_SINK_ARG
    keep_arg_name = csts.CLI_KEEP_FILES_ARG

    conf_section = csts.DEFAULT_CONF_SECTION
    conf_min_year = csts.CONF_MIN_YEAR
    conf_max_year = csts.CONF_MAX_YEAR

    config = {conf_section: {conf_min_year: '1871', conf_max_year: '2014'}}
    parser = ddog.cli.CliArgParser(config=config)
    args = ['--{}'.format(min_year_arg_name), '1900',
            '--{}'.format(max_year_arg_name), '1910',
            '--{}'.format(tmp_dir_arg_name), '/path/to/tmp',
            '--{}'.format(min_players_arg_name), '40',
            '--{}'.format(output_arg_name), 'console',
            '--{}'.format(keep_arg_name)]

    res = parser.parse_args(args=args)
    exp = {
        min_year_arg_name: 1900,
        max_year_arg_name: 1910,
        tmp_dir_arg_name: '/path/to/tmp',
        min_players_arg_name: 40,
        output_arg_name: 'console',
        keep_arg_name: True
    }

    assert res == exp

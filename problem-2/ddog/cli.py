"""
This modules gathers all the classes and functions dedicated to the parsing and validation of command-line arguments.
"""
import argparse

import ddog.constants as csts


def positive_integer(string):
    """ This functions casts an input string `string` as a positive integer.

    Args:
        string (str): String to be cast as a positive integer.

    Returns:
        int: The result of the casting of input `string` as an integer.

    Raises:
        argparse.ArgumentTypeError: If input argument `string` cannot be cast as a positive integer.
    """
    try:
        value = int(string)
        if value < 0:
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError('"{}" is not a positive integer'.format(string))
    return value


class CliArgParser:
    """ This class encapsulates all the logic dedicated to argument parsing and validation.

    Attributes:
        min_year_arg_name (str): Name of the CLI flag used to pass the year of the first report to use.
        max_year_arg_name (str): Name of the CLI flag used to pass the year of the last report to use.
        parser (argparse.ArgumentParser): Parser object used to parse a list of command line arguments.
    """
    def __init__(self, config):
        """ Initializes the `CliArgParser` object. Builds the `parser` attribute.

        Args:
            config (configparser.ConfigParser): Configuration object.
        """
        self.min_year_arg_name = csts.CLI_MIN_YEAR_ARG
        self.max_year_arg_name = csts.CLI_MAX_YEAR_ARG

        min_year = int(config[csts.DEFAULT_CONF_SECTION][csts.CONF_MIN_YEAR])
        max_year = int(config[csts.DEFAULT_CONF_SECTION][csts.CONF_MAX_YEAR])

        parser = argparse.ArgumentParser()

        parser.add_argument('--{flag_name:}'.format(flag_name=self.min_year_arg_name),
                            metavar='YYYY',
                            default=min_year,
                            type=int,
                            choices=range(min_year, max_year+1),
                            help='Year of the first baseball statistical report to include (Default: %(default)s)')
        parser.add_argument('--{flag_name:}'.format(flag_name=self.max_year_arg_name),
                            metavar='YYYY',
                            default=max_year,
                            type=int,
                            choices=range(min_year, max_year+1),
                            help='Year of the last baseball statistical report to include (Default: %(default)s)')
        parser.add_argument('--{flag_name:}'.format(flag_name=csts.CLI_TMP_DIR_ARG),
                            default='./tmp',
                            help='Path to a local directory where the downloaded data should be temporarily stored '
                                 '(Default: %(default)s)')
        parser.add_argument('--{flag_name:}'.format(flag_name=csts.CLI_MIN_PLAYERS_ARG),
                            default=50,
                            type=positive_integer,
                            help='Minimum number of players a team triple should contain to be returned '
                                 '(Default: %(default)s)')
        parser.add_argument('--{flag_name:}'.format(flag_name=csts.CLI_SINK_ARG),
                            default=csts.CONSOLE_SINK_NAME,
                            help='Output sink for the computed list of triples. Either "%(default)s" (default) to '
                                 'print to the standard output or a local path to an output text file')
        parser.add_argument('--{flag_name:}'.format(flag_name=csts.CLI_KEEP_FILES_ARG),
                            default=False,
                            action='store_true',
                            help='Whether the temporary directory and its content should be kept after running '
                                 '(Default: Content is dropped)')

        self.parser = parser

    def _validate_args(self, args):
        """ Validates the parsed command line arguments.

        Args:
            args (dict): Dictionary mapping the parsed CLI argument names and values.

        Returns:
            dict: The input arguments dictionary if no exception was raised.

        Raises:
            ValueError: If parsed starting year is higher than parsed finishing year.
        """
        if args[self.min_year_arg_name] > args[self.max_year_arg_name]:
            raise ValueError('Starting year must be lower or equal than finishing year')
        return args

    def parse_args(self, args):
        """ Parses and validate a list of command line arguments.

        Args:
            args (list): List of command line arguments (program name excluded).

        Returns:
            dict: Dictionary mapping the parsed and validated CLI argument names and values.
        """
        parsed_args = vars(self.parser.parse_args(args=args))
        return self._validate_args(args=parsed_args)

import argparse


def positive_integer(string):
    try:
        value = int(string)
        if value < 0:
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError('"{}" is not a positive integer'.format(string))
    return value


class CliArgParser:
    def __init__(self, config):
        self.min_year_arg_name = 'from'
        self.max_year_arg_name = 'to'

        min_year = int(config['DEFAULT']['MinYear'])
        max_year = int(config['DEFAULT']['MaxYear'])

        parser = argparse.ArgumentParser()

        parser.add_argument('--{}'.format(self.min_year_arg_name),
                            default=min_year,
                            type=int,
                            choices=range(min_year, max_year+1),
                            help='Year of the first baseball statistical report to include')
        parser.add_argument('--{}'.format(self.max_year_arg_name),
                            default=max_year,
                            type=int,
                            choices=range(min_year, max_year+1),
                            help='Year of the last baseball statistical report to include')
        parser.add_argument('--tmp-dir',
                            default='./tmp',
                            help='Path to a local directory where the downloaded data should be temporarily stored')
        parser.add_argument('--min-players',
                            default=50,
                            type=positive_integer,
                            help='Minimum number of players a team triple should contain to be displayed')
        parser.add_argument('--sink',
                            default='console',
                            help='Output sink for the computed list of triples')
        parser.add_argument('--remove-files',
                            default=True,
                            type=bool,
                            help='Whether the temporary directory and its content should be deleted after running')

        self.parser = parser

    def _validate_args(self, args):
        if args[self.min_year_arg_name] > args[self.max_year_arg_name]:
            raise ValueError('Starting year must be lower or equal than finishing year')
        return args

    def parse_args(self, args):
        parsed_args = vars(self.parser.parse_args(args=args))
        return self._validate_args(args=parsed_args)

import argparse


def positive_integer(string):
    try:
        value = int(string)
        if value < 0:
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError('"{}" is not a positive integer'.format(string))
    return value


def build_cli_arg_parser(config):
    min_year = config['DEFAULT']['MinYear']
    max_year = config['DEFAULT']['MaxYear']

    parser = argparse.ArgumentParser()

    parser.add_argument('--from',
                        default=min_year,
                        type=int,
                        choices=range(min_year, max_year+1),
                        help='Year of the first baseball statistical report to include')
    parser.add_argument('--to',
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

    return parser


def validate_args(args):
    if args['from'] > args['to']:
        raise ValueError('Starting year must be lower or equal than finishing year')
    return args

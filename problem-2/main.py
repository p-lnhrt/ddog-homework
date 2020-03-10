import configparser
import sys

import ddog.cli


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    parser = ddog.cli.build_cli_arg_parser(config=config)
    args = vars(parser.parse_args(sys.argv[1:]))
    args = ddog.cli.validate_args(args=args)

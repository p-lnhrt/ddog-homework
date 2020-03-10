import configparser
import sys

import ddog.cli


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    parser = ddog.cli.CliArgParser(config=config)
    args = parser.parse_args(args=sys.argv[1:])

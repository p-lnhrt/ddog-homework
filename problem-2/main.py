import configparser
import logging
import sys

import ddog.cli


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    level = config['DEFAULT']['LoggingLevel']
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)

    parser = ddog.cli.CliArgParser(config=config)
    args = parser.parse_args(args=sys.argv[1:])


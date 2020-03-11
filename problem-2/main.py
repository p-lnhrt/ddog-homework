import configparser
import logging
import sys

import ddog.cli
import ddog.source


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    level = config['DEFAULT']['LoggingLevel']
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)

    parser = ddog.cli.CliArgParser(config=config)
    args = parser.parse_args(args=sys.argv[1:])

    with ddog.source.TempDir(path=args['tmp'], remove=args['remove']) as tmp_dir_path:
        pass


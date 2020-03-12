import configparser
import logging
import os
import re
import sys

import ddog.cli
import ddog.sink
import ddog.source
import ddog.processing


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    level = config['DEFAULT']['LoggingLevel']
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)

    parser = ddog.cli.CliArgParser(config=config)
    args = parser.parse_args(args=sys.argv[1:])

    requested_year_range = range(args['from'], args['to'] + 1)
    tmp_file_regex = config['DEFAULT']['TmpFileRegex']
    regex = re.compile(tmp_file_regex)
    with ddog.source.TempDir(path=args['tmp'], remove=args['remove']) as tmp_dir_path:
        available_years = [int(regex.search(file_name).group(1)) for file_name in os.listdir(tmp_dir_path)
                           if regex.match(file_name)]
        missing_years = set(requested_year_range).difference(available_years)

        files_downloader = ddog.source.BaseballFilesDownloader(tmp_dir_path=tmp_dir_path, config=config)
        files_downloader.download(years=missing_years)

        files_loader = ddog.source.BaseballFilesLoader(tmp_dir_path=tmp_dir_path, config=config)
        df = files_loader.load()

        triple_counter = ddog.processing.TripleCounter(min_player_count=args['players'])
        triple_counts = triple_counter.compute(df=df)

        sink_factory = ddog.sink.SinkFactory(output=args['sink'])
        sink = sink_factory.build_sink()
        sink.write(triples=triple_counts)

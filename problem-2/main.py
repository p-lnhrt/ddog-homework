import configparser
import logging
import os
import re
import sys

import ddog.cli
import ddog.constants as csts
import ddog.sink
import ddog.source
import ddog.processing


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    level = config[csts.DEFAULT_CONF_SECTION][csts.CONF_LOG_LVL]
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)

    parser = ddog.cli.CliArgParser(config=config)
    args = parser.parse_args(args=sys.argv[1:])

    requested_year_range = range(args[csts.CLI_MIN_YEAR_ARG], args[csts.CLI_MAX_YEAR_ARG] + 1)
    tmp_file_regex = config[csts.DEFAULT_CONF_SECTION][csts.CONF_TMP_FILE_REGEX]
    regex = re.compile(tmp_file_regex)
    path, remove = args[csts.CLI_TMP_DIR_ARG], not args[csts.CLI_KEEP_FILES_ARG]
    with ddog.source.TempDir(path=path, remove=remove) as tmp_dir_path:
        available_years = [int(regex.search(file_name).group(1)) for file_name in os.listdir(tmp_dir_path)
                           if regex.match(file_name)]
        missing_years = set(requested_year_range).difference(available_years)

        if missing_years:
            logging.info('Starts downloading files corresponding to {:d} missing years'.format(len(missing_years)))
            files_downloader = ddog.source.BaseballFilesDownloader(tmp_dir_path=tmp_dir_path, config=config)
            files_downloader.download(years=missing_years)

        files_loader = ddog.source.BaseballFilesLoader(tmp_dir_path=tmp_dir_path, config=config)
        df = files_loader.load()

        triple_counter = ddog.processing.TripleCounter(min_player_count=args[csts.CLI_MIN_PLAYERS_ARG])
        triple_counts = triple_counter.compute(df=df)

        sink_factory = ddog.sink.SinkFactory(output=args[csts.CLI_SINK_ARG])
        sink = sink_factory.build_sink()
        sink.write(triples=triple_counts)

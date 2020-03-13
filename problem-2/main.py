import configparser
import logging
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

    path, remove = args[csts.CLI_TMP_DIR_ARG], not args[csts.CLI_KEEP_FILES_ARG]
    with ddog.source.TempDir(path=path, remove=remove) as tmp_dir_path:
        files_loader = ddog.source.BaseballFilesLoader(tmp_dir_path=tmp_dir_path,
                                                       config=config,
                                                       min_year=args[csts.CLI_MIN_YEAR_ARG],
                                                       max_year=args[csts.CLI_MAX_YEAR_ARG])
        df = files_loader.load()

        triple_counter = ddog.processing.TripleCounter(min_player_count=args[csts.CLI_MIN_PLAYERS_ARG])
        triple_counts = triple_counter.compute(df=df)

        sink_factory = ddog.sink.SinkFactory(output=args[csts.CLI_SINK_ARG])
        sink = sink_factory.build_sink()
        sink.write(triples=triple_counts)

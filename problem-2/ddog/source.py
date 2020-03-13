import functools
import logging
import os
import re
import shutil
import urllib

import pandas as pd

import ddog.constants as csts


class TempDir:
    def __init__(self, path, remove):
        self.path = path
        self.remove = remove

    def __enter__(self):
        try:
            os.mkdir(self.path)
            logging.info('Created temporary directory: {path:}'.format(path=self.path))
        except FileExistsError:
            logging.info('Temporary directory {path:} already exists'.format(path=self.path))
        return self.path

    def __exit__(self, exc_type, exc_value, traceback):
        if self.remove:
            shutil.rmtree(self.path, ignore_errors=True)
            logging.info('Removed temporary directory: {path:}'.format(path=self.path))


class BaseballFilesDownloader:
    def __init__(self, tmp_dir_path, config):
        self.tmp_dir_path = tmp_dir_path
        self.formatted_tmp_file_name = config[csts.DEFAULT_CONF_SECTION][csts.CONF_TMP_FILE_FMT_NAME]
        self.formatted_url = config[csts.DEFAULT_CONF_SECTION][csts.CONF_FMT_SOURCE_URL]

    def download(self, years):
        for year in years:
            local_file_name = self.formatted_tmp_file_name.format(year=year)
            url = self.formatted_url.format(year=year)
            try:
                with urllib.request.urlopen(url=url) as response:
                    file_name = os.path.join(self.tmp_dir_path, local_file_name)
                    with open(file_name, 'wb') as file_obj:
                        file_obj.write(response.read())
                logging.info('Successfully downloaded file for year {year:} at {path:}'
                             .format(year=year, path=file_name))

            except urllib.error.HTTPError as error:
                logging.warning('Requesting URL "{url:}" failed returning the following HTTP error: '
                                'Code: {code:} - {msg:}'.format(url=url, code=error.code, msg=error.msg))
                continue


class BaseballFilesLoader:
    def __init__(self, tmp_dir_path, config, min_year, max_year):
        self.tmp_dir_path = tmp_dir_path
        self.config = config
        self.min_year = min_year
        self.max_year = max_year

        tmp_file_regex = config[csts.DEFAULT_CONF_SECTION][csts.CONF_TMP_FILE_REGEX]
        self.regex = re.compile(tmp_file_regex)

    def _get_missing_years(self):
        requested_year_range = range(self.min_year, self.max_year + 1)
        available_years = [int(self.regex.search(file_name).group(1)) for file_name in os.listdir(self.tmp_dir_path)
                           if self.regex.match(file_name)]
        return set(requested_year_range).difference(available_years)

    def _download_years(self, years):
        logging.info('Starts downloading files corresponding to {:d} missing years'.format(len(years)))
        files_downloader = BaseballFilesDownloader(tmp_dir_path=self.tmp_dir_path, config=self.config)
        files_downloader.download(years=years)

    def load(self):
        missing_years = self._get_missing_years()
        if missing_years:
            self._download_years(years=missing_years)

        input_file_names = [os.path.join(self.tmp_dir_path, file_name) for file_name in os.listdir(self.tmp_dir_path)
                            if self.regex.match(file_name)]

        dataframes = [pd.read_csv(file_name, header=None, usecols=[1, 2, 4], names=['team', 'league', 'player'])
                      for file_name in input_file_names]

        return functools.reduce(lambda x, y: x.append(y), dataframes)

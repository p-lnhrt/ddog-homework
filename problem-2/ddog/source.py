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
        except FileExistsError:
            logging.info('Temporary directory {} already exists'.format(self.path))
        return self.path

    def __exit__(self, exc_type, exc_value, traceback):
        if self.remove:
            shutil.rmtree(self.path, ignore_errors=True)


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
    def __init__(self, tmp_dir_path, config):
        tmp_file_regex = config[csts.DEFAULT_CONF_SECTION][csts.CONF_TMP_FILE_REGEX]
        regex = re.compile(tmp_file_regex)

        self.input_file_names = [os.path.join(tmp_dir_path, file_name) for file_name in os.listdir(tmp_dir_path)
                                 if regex.match(file_name)]

    def load(self):
        dataframes = [pd.read_csv(file_name, header=None, usecols=[1, 2, 4], names=['team', 'league', 'player'])
                      for file_name in self.input_file_names]

        return functools.reduce(lambda x, y: x.append(y), dataframes)

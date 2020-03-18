"""
This modules gathers all the classes and functions dedicated to the downloading and reading of baseball-statistics
files.
"""
import functools
import logging
import os
import re
import shutil
import urllib

import pandas as pd

import ddog.constants as csts


class TempDir:
    """ Context manager class dedicated to the management of the local temporary directory where baseball-statistics
    files should be stored after being downloaded. Entering the context implies creating the directory on the local
    file system. Exiting the context may be associated to the removal of the directory depending on the value of the
    `remove` attribute.

    Attributes:
         path (str): Path of the local temporary directory on the local filesystem. Can already exist.
         remove (bool): Whether or not the temporary directory and its content should be removed when exiting.
    """
    def __init__(self, path, remove):
        """ Initializes the `TmpDir` object.

        Arguments:
            Cf. class docstring.
        """
        self.path = path
        self.remove = remove

    def __enter__(self):
        """ Creates the temporary directory on the local file system if it does not already exists.

        Returns:
            str: Path to the temporary directory on the local file system.
        """
        try:
            os.mkdir(self.path)
            logging.info('Created temporary directory: {path:}'.format(path=self.path))
        except FileExistsError:
            logging.info('Temporary directory {path:} already exists'.format(path=self.path))
        return self.path

    def __exit__(self, exc_type, exc_value, traceback):
        """ Removes the local temporary directory and its content if the `remove` attribute is set to `True`.

        Args:
            exc_type (type): Raised exception (`None` if no exception occurred) type (class) object.
            exc_value (Exception): Raised exception (`None` if no exception occurred).
            traceback (traceback): Raised exception traceback object (`None` if no exception occurred).
        """
        if self.remove:
            shutil.rmtree(self.path, ignore_errors=True)
            logging.info('Removed temporary directory: {path:}'.format(path=self.path))


class BaseballFilesDownloader:
    """ This class encapsulates all the logic dedicated to the downloading of yearly baseball-statistics files to the
    local file system.

    Attributes:
        tmp_dir_path (str): Directory on the local file system when the downloaded files should be stored.
        formatted_tmp_file_name (str): Formatted string used to generate the local names of the downloaded files.
        formatted_url (str): Formatted HTTP URL used to download the required files.
    """
    def __init__(self, tmp_dir_path, config):
        """ Initializes the `BaseballFilesDownloader` object.

        Args:
            tmp_dir_path (str): Cf. class docstring.
            config (configparser.ConfigParser): Configuration object.
        """
        self.tmp_dir_path = tmp_dir_path
        self.formatted_tmp_file_name = config[csts.DEFAULT_CONF_SECTION][csts.CONF_TMP_FILE_FMT_NAME]
        self.formatted_url = config[csts.DEFAULT_CONF_SECTION][csts.CONF_FMT_SOURCE_URL]

    def download(self, years):
        """ Downloads a single baseball-statistics file using an HTTP URL to the local file system for each requested
        year in `years`.

        Args:
            years (list[int]): List of years for which baseball-statistics files will be downloaded.
        """
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
    """ This class encapsulates all the logic dedicated to loading the content of baseball-statistics CSV files stored
    in the same directory on the local file system into a single `pandas.DataFrame` object.

    Attributes:
        tmp_dir_path (str): Directory on the local file system when the files to be loaded are stored.
        config (configparser.ConfigParser): Configuration object.
        min_year (int): Year of the first file to load.
        max_year (int): Year of the last file to load.
        tmp_file_formatted_name (str): Name (formatted string) used to store baseball-statistics files on the local FS.
        regex (_sre.SRE_Pattern): Regex object used to filter the files located in `tmp_dir_path`.
    """
    def __init__(self, tmp_dir_path, config, min_year, max_year):
        self.tmp_dir_path = tmp_dir_path
        self.config = config
        self.min_year = min_year
        self.max_year = max_year
        self.tmp_file_formatted_name = config[csts.DEFAULT_CONF_SECTION][csts.CONF_TMP_FILE_FMT_NAME]

        tmp_file_regex = config[csts.DEFAULT_CONF_SECTION][csts.CONF_TMP_FILE_REGEX]
        self.regex = re.compile(tmp_file_regex)

    def _get_missing_years(self):
        """ Returns the list of missing years considering the requested year range and the files already present in
        `tmp_dir_path`.

        Returns:
            set: Set of missing years.
        """
        requested_year_range = range(self.min_year, self.max_year + 1)
        available_years = [int(self.regex.search(file_name).group(1)) for file_name in os.listdir(self.tmp_dir_path)
                           if self.regex.match(file_name)]
        return set(requested_year_range).difference(available_years)

    def _download_years(self, years):
        """ For each year in `years`, download the associated baseball-statistics file to the local file system.

        Args:
            years (Iterable[int]): List of years for which the baseball-statistics file needs to be downloaded.
        """
        logging.info('Starts downloading files corresponding to {:d} missing years'.format(len(years)))
        files_downloader = BaseballFilesDownloader(tmp_dir_path=self.tmp_dir_path, config=self.config)
        files_downloader.download(years=years)

    def load(self):
        """ Loads the content of all the files (the name of which matches the `regex` attribute) from `tmp_dir_path`
        into a `pandas.DataFrame`

        Returns:
            pandas.DataFrame: DataFrames into which the 'team', 'league' and 'player' columns of the baseball-statistics
            files located in `tmp_dir_path` have been loaded.
        """
        missing_years = self._get_missing_years()
        if missing_years:
            self._download_years(years=missing_years)

        input_file_names = [os.path.join(self.tmp_dir_path, self.tmp_file_formatted_name.format(year=year))
                            for year in range(self.min_year, self.max_year + 1)]

        dataframes = [pd.read_csv(file_name, header=None, usecols=[1, 2, 3], names=['team', 'league', 'player-id'])
                      for file_name in input_file_names]

        return functools.reduce(lambda x, y: x.append(y), dataframes)

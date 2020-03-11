import logging
import os
import shutil
import urllib


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
        self.formatted_tmp_file_name = config['DEFAULT']['TmpFileFormattedName']
        self.formatted_url = config['DEFAULT']['FormattedSourceURL']

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

import logging
import os
import shutil


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

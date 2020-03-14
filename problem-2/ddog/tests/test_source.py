import re
import unittest.mock as mock

import ddog.source


@mock.patch('logging.info')
@mock.patch('os.mkdir')
def test_tmp_dir_enter_non_existing_dir(mock_mkdir, mock_info):
    """
    Given a `ddog.source.TempDir` context manager associated with a non-yet existing local directory,
    When I call the `__enter__` method of the context manager,
    Then the `os.mkdir` function should be called once with the directory path and the `logging.info` function should be
    called once.
    """
    path = '/path/to/tmp'
    mock_cm = mock.Mock()
    mock_cm.path = path
    ddog.source.TempDir.__enter__(mock_cm)
    mock_mkdir.assert_called_once_with(path)
    mock_info.assert_called_once()


@mock.patch('logging.info')
@mock.patch('os.mkdir')
def test_tmp_dir_enter_existing_dir(mock_mkdir, mock_info):
    """
    Given a `ddog.source.TempDir` context manager associated with an already-existing local directory,
    When I call the `__enter__` method of the context manager,
    Then the the `logging.info` function should be called once.
    """
    path = '/path/to/tmp'
    mock_cm = mock.Mock()
    mock_cm.path = path
    mock_mkdir.side_effect = FileExistsError
    ddog.source.TempDir.__enter__(mock_cm)
    mock_info.assert_called_once()


@mock.patch('logging.info')
@mock.patch('shutil.rmtree')
def test_tmp_dir_exit_rm_true(mock_rmtree, mock_info):
    """
    Given a `ddog.source.TempDir` context manager with a `remove` attribute set to `True`,
    When I call the `__exit__` method of the context manager,
    Then the `shutil.rmtree` and `logging.info` functions should be called once.
    """
    path = '/path/to/tmp'
    remove = True
    tmp_dir_context_manager = ddog.source.TempDir(path=path, remove=remove)
    tmp_dir_context_manager.__exit__(exc_type=None, exc_value=None, traceback=None)
    mock_rmtree.assert_called_once_with(path, ignore_errors=True)
    mock_info.assert_called_once()


@mock.patch('logging.info')
@mock.patch('shutil.rmtree')
def test_tmp_dir_exit_rm_false(mock_rmtree, mock_info):
    """
    Given a `ddog.source.TempDir` context manager with a `remove` attribute set to `False`,
    When I call the `__exit__` method of the context manager,
    Then the `shutil.rmtree` and `logging.info` functions should not be called.
    """
    path = '/path/to/tmp'
    remove = False
    tmp_dir_context_manager = ddog.source.TempDir(path=path, remove=remove)
    tmp_dir_context_manager.__exit__(exc_type=None, exc_value=None, traceback=None)
    mock_rmtree.assert_not_called()
    mock_info.assert_not_called()


@mock.patch('os.listdir')
def test_get_missing_years(mock_listdir):
    """
    Given a `ddog.source.BaseballFilesLoader` object set with a year range going from 2000 to 2010 (included) and a
    temporary directory containing baseball-statistics files from year 2000 to 2007 included,
    When I call its `_get_missing_years` method,
    Then I should be returned a set containing the years missing in the temporary directory (2008, 2009 and 2010).
    """
    min_year = 2000
    mock_loader = mock.Mock(min_year=min_year,
                            max_year=2010,
                            tmp_dir_path='/path/to/tmp',
                            regex=re.compile('baseball-([0-9]{4})\.csv'))

    mock_listdir.return_value = ['baseball-{:d}.csv'.format(year) for year in range(min_year, 2008)]
    res = ddog.source.BaseballFilesLoader._get_missing_years(self=mock_loader)
    exp = {2008, 2009, 2010}
    assert res == exp


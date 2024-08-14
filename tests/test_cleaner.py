'''
test_cleaner.py
===============

Author:
-------
Wyatt D. Scott (https://github.com/WD-Scott)

Last Updated:
-------------
14 August 2024
'''

import os
import shutil
import pytest
from pkg_cleaner import make_unique, config, scan_create, scan_new, MoverHandler

dst = '/Downloads/'
FLDRS = ["Images", "Videos", "Audio", "Documents", "Coding"]

if os.getcwd().endswith('Downloads_Cleaner'):
    DIR_SCAN = os.getcwd() + '/tests/Downloads/'
elif os.getcwd().endswith('tests'):
    DIR_SCAN = os.getcwd() + '/Downloads/'

os.chdir(DIR_SCAN)

test_cases = [
    ("tester(2).png", 'tester.png'),
    ("tester(2).py", 'tester.py'),
    ("tester(2).pdf", 'tester.pdf'),
    ("tester(2).mp4", 'tester.mp4'),
    ("tester(2).mp3", 'tester.mp3')
]

test_files = [
    'test_image.jpg',
    'test_video.mp4',
    'test_audio.mp3',
    'test_document.pdf',
    'test_code.py',
    'test_duplicate.jpg'
]

test_ids = [name for name, _ in test_cases]

@pytest.fixture(scope='module')
def mock_downloads_dir(tmpdir_factory):
    '''
    Fixture to create a temp Downloads dir with specified subdirs.
    '''
    mock_dir = tmpdir_factory.mktemp('Downloads')

    for subdir in FLDRS:
        os.makedirs(os.path.join(mock_dir, subdir))

    for file_name in test_files:
        with open(os.path.join(mock_dir, file_name), 'w') as f:
            f.write("test")

    yield mock_dir

    shutil.rmtree(str(mock_dir))

def test_scan_create_missing_subdirs(mock_downloads_dir):
    '''
    Tests that the `scan_create` function from `scanners.py`
    correctly identifies cases where specified subdirs do not
    exist before creating them.

    Not testing the function itself with this test, but testing
    the underlying functionality.

    GIVEN a Downloads dir without specified subdirs (i.e., FLDRS).
    WHEN the `scan_create` function scans for the subdirs.
    THEN ensure it correctly finds that they do not exist yet.
    '''
    expected = 5
    found = [i for i in os.listdir(mock_downloads_dir)
             if os.path.isdir(os.path.join(mock_downloads_dir, i))
             and i in FLDRS]
    actual = len(found)
    assert expected == actual, "Should find 5 specified subdirs"

def test_scan_create(mock_downloads_dir):
    '''
    Tests that the `scan_create` function from `scanners.py`
    correctly creates the specified subdirs.

    GIVEN a Downloads dir without specified subdirs (i.e., FLDRS).
    WHEN the `scan_create` function scans for the subdirs.
    THEN ensure it correctly creates them.
    '''
    scan_create(mock_downloads_dir, FLDRS)

    created = sorted([i for i in os.listdir(mock_downloads_dir)
                      if os.path.isdir(os.path.join(mock_downloads_dir, i))
                      and i in FLDRS])

    assert len(FLDRS) == len(created), "Should find 5 specified subdirs"
    assert sorted(FLDRS) == created, f"Missed {[i for i in FLDRS if i not in created]}"

def test_config():
    '''
    Tests the config setup in cleaner.py.

    GIVEN the config dict.
    WHEN source dir is initialized.
    THEN ensure it ends with '/Downloads'.
    '''
    cfg = config.get('source_dir')
    dl = '/Downloads'
    assert cfg[-10:] == dl, f"Source dir should end with {dl} but got {cfg}"

@pytest.mark.parametrize("new_name, original", test_cases, ids=test_ids)
def test_make_unique(new_name, original, counter=2):
    '''
    Tests the `make_unique` function from cleaner.py.

    GIVEN a file name and destination
    WHEN checking if a unique file name is generated
    THEN ensure the name is unique and formatted correctly
    '''
    assert make_unique(dst, original, counter=2) == new_name

def test_process(mock_downloads_dir):
    '''
    Tests the `MoverHandler` class' `process` method.

    GIVEN a MoverHandler instance.
    WHEN a user initializes the `process` method.
    THEN check that it correctly moves files.
    '''
    config['source_dir'] = str(mock_downloads_dir)
    config['directories'] = {folder: os.path.join(str(mock_downloads_dir), folder)\
                             for folder in config['directories'].keys()}

    handler = MoverHandler()
    handler.process()

    for category in config['directories']:
        directory = config['directories'][category]
        files = os.listdir(directory)
        assert len(files) > 0, f"No files found in {directory} after processing"
        for file in files:
            assert any(file.endswith(ext) for ext in config['extensions'][category]),\
            f"File {file} in {directory} does not have the correct extension"


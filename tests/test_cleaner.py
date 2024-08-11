'''
test_cleaner.py
===============

Author:
-------
Wyatt D. Scott (wyatt.d.scott28@gmail.com)

Last Updated:
-------------
11 August 2024
'''
import os
import logging
from os.path import exists, join, splitext
from shutil import move
import pytest
from pkg_cleaner import make_unique, config

dst = '/Downloads/'

test_cases = [
    ("tester(2).png", 'tester.png'),
    ("tester(2).py", 'tester.py'),
    ("tester(2).pdf", 'tester.pdf'),
    ("tester(2).mp4", 'tester.mp4'),
    ("tester(2).mp3", 'tester.mp3')
]

test_ids = [name for name, _ in test_cases]

def test_config():
    '''
    Tests the config setup in cleaner.py.

    GIVEN the config dict
    WHEN source dir is initialized
    THEN ensure it ends with '/Downloads'
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
    assert make_unique(dst, original, 2) == new_name

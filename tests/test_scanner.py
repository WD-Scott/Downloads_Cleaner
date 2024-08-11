'''
test_scanner.py
===============

Author:
-------
Wyatt D. Scott (wyatt.d.scott28@gmail.com)

Last Updated:
-------------
11 August 2024
'''

import os

DIR_SCAN_CREATE = os.getcwd()+'/tests/Downloads/'
FLDRS = ["Images", "Videos", "Audio", "Documents", "Coding"]

os.chdir(DIR_SCAN_CREATE)

def test_scan_create_missing_subdirs():
    '''
    Tests that the `scan_create` function from `scanners.py` 
    correctly identifies cases where specified subdirs do not
    exist before creating them.

    GIVEN a Downloads dir without specified subdirs (i.e., FLDRS)
    WHEN the `scan_create` function scans for the subdirs
    THEN ensure it correctly finds that they do not exist yet
    '''
    expected = 0
    found = [i for i in os.listdir(DIR_SCAN_CREATE)
             if os.path.isdir(os.path.join(DIR_SCAN_CREATE, i))
             and i in FLDRS]
    actual = len(found)
    assert expected == actual, "Should find 0 specified subdirs"

def test_scan_create():
    '''
    Tests that the `scan_create` function from `scanners.py`
    correctly creates the specified subdirs.

    GIVEN a Downloads dir without specified subdirs (i.e., FLDRS)
    WHEN the `scan_create` function scans for the subdirs
    THEN ensure it correctly creates them.
    '''
    [os.makedirs(os.path.join(DIR_SCAN_CREATE, f), exist_ok=True)
     for f in FLDRS
     if not os.path.exists(os.path.join(DIR_SCAN_CREATE, f))]
    created = sorted([i for i in os.listdir(DIR_SCAN_CREATE)
               if os.path.isdir(os.path.join(DIR_SCAN_CREATE, i))
               and i in FLDRS])
    actual = len(created)
    assert len(FLDRS) == actual, "Should find 5 specified subdirs"
    assert sorted(FLDRS) == created, f"Missed {[i for i in FLDRS if i not in created]}"
    fldrs_2 = ['Images', 'Videos', 'Audio', 'Documents', 'Coding', 'Missed']
    missed = [i for i in fldrs_2 if i not in created]
    assert missed[0] == 'Missed', "Not identifying missed folders"

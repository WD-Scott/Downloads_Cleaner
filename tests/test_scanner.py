'''
test_scanner.py
===============

Author:
-------
Wyatt D. Scott (wyatt.d.scott28@gmail.com)

Last Updated:
-------------
12 August 2024
'''

import os
from pkg_cleaner import scan_create, scan_new

if os.getcwd().endswith('Downloads_Cleaner'):
    DIR_SCAN = os.getcwd()+'/tests/Downloads/'
elif os.getcwd().endswith('tests'):
    DIR_SCAN = os.getcwd()+'/Downloads/'

FLDRS = ["Images", "Videos", "Audio", "Documents", "Coding"]

os.chdir(DIR_SCAN)

def test_scan_create_missing_subdirs():
    '''
    Tests that the `scan_create` function from `scanners.py`
    correctly identifies cases where specified subdirs do not
    exist before creating them.

    Not testing the function itself with this test, but testing
    the underlying functionality.

    GIVEN a Downloads dir without specified subdirs (i.e., FLDRS)
    WHEN the `scan_create` function scans for the subdirs
    THEN ensure it correctly finds that they do not exist yet
    '''
    expected = 0
    found = [i for i in os.listdir(DIR_SCAN)
             if os.path.isdir(os.path.join(DIR_SCAN, i))
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
    scan_create(DIR_SCAN, FLDRS)
    created = sorted([i for i in os.listdir(DIR_SCAN)
               if os.path.isdir(os.path.join(DIR_SCAN, i))
               and i in FLDRS])
    actual = len(created)
    assert len(FLDRS) == actual, "Should find 5 specified subdirs"
    assert sorted(FLDRS) == created, f"Missed {[i for i in FLDRS if i not in created]}"
    fldrs_2 = ['Images', 'Videos',
               'Audio', 'Documents',
               'Coding', 'Missed']
    missed = [i for i in fldrs_2 if i not in created]
    assert missed[0] == 'Missed', "Not identifying missed folders"


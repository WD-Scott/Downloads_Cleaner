"""
scanners.py
===========

This Python file includes utility functions for the cleaner.py file.

Functions:
----------
scan_create():
    Creates necessary folders in the Downloads dir if they do not exist.

scan_new():
     Scans the Downloads dir for new files.

prompt():
    Prompts users to run the cleaner if new files are in the Downloads dir.

Author:
-------
Wyatt D. Scott (wyatt.d.scott28@gmail.com)

Last Updated:
-------------
21 July 2024
"""

import os
import subprocess

DIR = os.path.expanduser('~/Downloads')
FLDRS = ["Imgs", "Videos", "Audio", "Docs", "py"]

def scan_create():
    """
    Create necessary folders in the Downloads directory if they do not exist.

    This function checks for the presence of specific folders in the Downloads
    directory and creates them if they do not exist.

    Raises
    ------
    Exception
        If there is an error creating the folders.
    """
    try:
        [os.makedirs(os.path.join(DIR, f), exist_ok=True) for f in FLDRS
         if not os.path.exists(os.path.join(DIR, f))]
    except Exception as err:
        print(f"Error creating folders: {err}")

def scan_new():
    """
    Scan the Downloads directory for new files.

    This function scans the Downloads directory for files that are not part of
    the predefined folders and do not start with a dot ("."). 
    The function ignores hidden files.

    Returns
    -------
    list of str
        A list of filenames that are new in the Downloads directory.

    Raises
    ------
    Exception
        If there is an error checking the files.
    """
    try:
        files = [f for f in os.listdir(DIR)
                 if os.path.isfile(os.path.join(DIR, f))
                 and f not in FLDRS
                 and not f.startswith('.')]
        files = sorted(files, key=lambda file: file.split('.')[-1])
        return files
    except Exception as err:
        print(f"Error checking files: {err}")
        return []

def prompt():
    """
    Prompt the user to run the cleaner if there are new files in the Downloads dir.

    This function lists new files in the Downloads dir and prompts the user
    to decide whether to run the cleaner to move these files to the appropriate folders.
    If the user input is invalid, it prompts again until a valid input is received.

    Raises
    ------
    subprocess.CalledProcessError
        If there is an error running the 'clean' Makefile target.
    """
    files = scan_new()
    if files:
        print("DOWNLOADS MESSY; CONTENTS INCLUDE:\n----------------------------------")
        for file in files:
            print(file)
        while True:
            user_input = input("\nWould you like to run the cleaner? y/n: ").strip().lower()
            if user_input == 'y':
                try:
                    subprocess.run(["make", "clean"], check=True)
                except subprocess.CalledProcessError as err:
                    print(f"Error running the cleaner: {err}")
                break
            if user_input == 'n':
                break
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

if __name__ == "__main__":
    scan_create()
    prompt()

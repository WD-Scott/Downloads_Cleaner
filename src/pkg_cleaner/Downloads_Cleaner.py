'''
Downloads_Cleaner.py
====================

This Python module contains code to set up the GUI.

Functions:
----------
scan_downloads():
    Runs the functions from scanners.py.

run_cleaner():
    Runs the functions from cleaner.py.

Author:
-------
Wyatt D. Scott (wyatt.d.scott28@gmail.com)

Last Updated:
-------------
26 July 2024
'''

import os
import PySimpleGUI as sg
import scanners
import cleaner

#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
# def resource_path(relative_path):
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")

#     return os.path.join(base_path, relative_path)

def scan_downloads():
    """
    Scans the Downloads directory for new files.
    """
    scanners.scan_create()
    new_files = scanners.scan_new()
    if new_files:
        message = "Your downloads folder is messy; the contents include:" + "\n" + "------------------------------------------------------------------------" + "\n" + "\n".join(new_files)
        return message, new_files
    message = "No new files found in Downloads."
    return message, []

def run_cleaner():
    """
    Runs the file cleaner on the Downloads directory.
    """
    try:
        download_files = [e.name for e in os.scandir(cleaner.config['source_dir']) if e.is_file() and not e.name.startswith('.')]
        total_files = len(download_files)
        if total_files == 0:
            return "No files to clean."

        mover = cleaner.MoverHandler()
        for idx, name in enumerate(download_files):
            moved = mover.move_file(name)
            if moved:
                if not sg.one_line_progress_meter('Progress', idx + 1, total_files, 'key', 'Cleaning files...'):
                    break
        return "Cleaning complete! \n You can click 'Exit' below to close this window"
    except Exception as err:
        return f"Error running cleaner: {err}"

layout = [
    [sg.Text('Downloads Cleaner', font=('Helvetica', 20, 'bold'))],
    [sg.Multiline(size=(65, 10), font=('Helvetica', 15), key='-OUTPUT-')],
    [sg.Button('Scan', font=('Helvetica', 16), key='-SCAN-'), sg.Button('Exit', font=('Helvetica', 16))]
]

window = sg.Window('Downloads Cleaner', layout, finalize=True)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == '-SCAN-':
        result, new_filez = scan_downloads()
        window['-OUTPUT-'].update(result)
        if new_filez:
            choice = sg.popup_yes_no("Run cleaner?")
            if choice == 'Yes':
                clean_result = run_cleaner()
                window['-OUTPUT-'].update(clean_result)

window.close()

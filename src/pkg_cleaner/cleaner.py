'''
cleaner.py
==========

This Python file contains code to cleanup the downloads directory.

Author:
-------
Wyatt D. Scott (https://github.com/WD-Scott)

Last Updated:
-------------
14 August 2024
'''

import os
import logging
from os.path import exists, join, splitext
from shutil import move
import PySimpleGUI as sg

config = {
    'source_dir': os.path.expanduser('~/Downloads'),
    'directories': {
        'images': os.path.expanduser('~/Downloads/Images'),
        'videos': os.path.expanduser('~/Downloads/Video'),
        'audio': os.path.expanduser('~/Downloads/Audio'),
        'documents': os.path.expanduser('~/Downloads/Documents'),
        'coding': os.path.expanduser('~/Downloads/Coding')
    },
    'extensions': {
        'images': [".jpg", ".jpeg", ".jpe", ".jif", ".jfif",
                   ".jfi", ".png", ".gif", ".webp", ".tiff",
                   ".tif", ".psd", ".raw", ".arw", ".cr2",
                   ".nrw", ".k25", ".bmp", ".dib", ".heif",
                   ".heic", ".ind", ".indd", ".indt", ".jp2",
                   ".j2k", ".jpf", ".jpf", ".jpx", ".jpm",
                   ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"],
        'videos': [".webm", ".mpg", ".mp2", ".mpeg", ".mpe",
                   ".mpv", ".ogg", ".mp4", ".mp4v", ".m4v",
                   ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"],
        'audio': [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"],
        'documents': [".doc", ".docx", ".odt", ".pdf", ".xls",
                      ".xlsx", ".ppt", ".pptx", ".csv"],
        'coding': [".py", ".ipynb", ".R", ".Rmd", ".rds"]
    }
}

def make_unique(dest, name, counter=1):
    '''
    Generate a unique file name if a file with the same name
    already exists in the destination directory.

    Params
    ------
    dest : str
        Destination directory.
    name : str
        Original file name.
    counter : int, optional
        Counter to generate a unique file name, by default 1.

    Returns
    -------
    str
        Unique file name.
    '''
    file_name, extn = splitext(name)
    new_name = f"{file_name}({counter}){extn}" if counter > 1 else name
    if exists(os.path.join(dest, new_name)):
        return make_unique(dest, name, counter + 1)
    return new_name

class MoverHandler:
    '''
    Handler for moving files based on their extensions.
    '''
    def process(self):
        '''
        Process files in downloads dir and move them
        to appropriate folders based on their extensions.

        Raises
        ------
        FileNotFoundError
            If the source directory or any file within it is not found.
        PermissionError
            If permission is denied while accessing or moving files.
        Exception
            For any other unexpected errors that occur during the file processing.
        '''
        try:
            downloads = [entry.name for entry in os.scandir(config['source_dir'])
                         if entry.is_file() and not entry.name.startswith('.')]
            total_files = len(downloads)

            sg.OneLineProgressMeter('Cleaning files', 0,
                                    total_files, 'key', 'Processing...')

            for index, name in enumerate(downloads):
                moved = self.move_file(name)
                if moved:
                    sg.OneLineProgressMeter('Cleaning Files', index + 1,
                                            total_files, 'key', 'Processing...')

            sg.OneLineProgressMeter('Cleaning Files', total_files, total_files,
                                    'key', 'Cleaning complete...')
            logging.info("Cleaning complete")

        except FileNotFoundError as e_name:
            logging.error("An error occurred: %s", e_name)
        except PermissionError as e_name:
            logging.error("An error occurred: %s", e_name)

    def move_file(self, name):
        '''
        Move a file to the appropriate subdirectory based on its extension.

        Params
        ------
        name : str
            Name of the file to be moved.

        Returns
        -------
        bool
            True if the file was moved, False otherwise.
        '''
        moved = False
        for category, extns in config['extensions'].items():
            if any(name.endswith(ext) or name.endswith(ext.upper()) for ext in extns):
                src = join(config['source_dir'], name)
                dest = config['directories'][category]
                if exists(os.path.join(dest, name)):
                    unique_name = make_unique(dest, name)
                    new_name = join(dest, unique_name)
                    os.rename(src, new_name)
                else:
                    move(src, dest)
                moved = True
                break

        return moved

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        handlers=[logging.StreamHandler(), logging.FileHandler('cleaner.log')])

    event_handler = MoverHandler()
    event_handler.process()

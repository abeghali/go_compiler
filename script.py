"""
Created on Sun Sep 3 2023

@author: Abanoub Ghali
"""

import os
import json
import shutil
from subprocess import PIPE, run
import sys

GAME_DIR_PATTERN = "game"


def main():
    
    args = sys.argv

    # Raise an exception if the script doesn't receive the 2 required arguments when run, source
    # and target directories, plus the name of the script itself, as it counts as a command line argument.
    if len(args) != 3:
        raise Exception("You must pass a source and target directory.")

    # Only assigning the values beginning at index 1 to disregard the name of the script itselt.
    source, target = args[1:]

    # Get current working directory, to join to path that was passed as an argument.
    cwd = os.getcwd()
    source_dir = os.path.join(cwd, source)
    target_dir = os.path.join(cwd, target)

    game_paths = find_all_game_paths(source_dir)

    # For testing.
    print(game_paths)
    print(len(game_paths))

    create_dir(target_dir)

#=====================================================================================================================

def find_all_game_paths(source):

    game_paths = []

    # To "walk" recursively through the passed source path.
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)
        break
    
    return game_paths

#=====================================================================================================================

# A simple function that checks if the target directory exists or not, and if it doesn't, then it creates it.
def create_dir(target):

    if not os.path.exists(target):
        os.mkdir(target)

#=====================================================================================================================

def get_name_from_paths(paths, to_rmv):

    new_names = []

    for path in paths:
        -, dir_name = os.path.split(path)

#=====================================================================================================================

if __name__ == "__main__":
    main()
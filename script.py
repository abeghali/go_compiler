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
    
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    args = sys.argv

    # Raise an exception if the script doesn't receive the 2 required arguments when run, source
    # and target directories, plus the name of the script itself, as it counts as a command line argument.
    if len(args) != 3:
        raise Exception("You must pass a source and target directory.")

    # Only assigning the values beginning at index 1 to disregard the name of the script itselt.
    source, target = args[1:]

#=====================================================================================================================

def find_all_game_paths(source):


#=====================================================================================================================

if __name__ == "__main__":
    main()
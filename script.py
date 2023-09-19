"""
Created on Sun Sep 3 2023

@author: Abanoub Ghali
"""

import os
import json
import shutil
from subprocess import PIPE, run
import sys

GAME_DIR_PATTERN = "_game"
GAME_CODE_EXTENSION = ".go"
GAME_FILE_COMPILE_COMMAND = ["go", "build"]

# =====================================================================================================================

def main():

    args = sys.argv

    # Raise an exception if the script doesn't receive the 2 required arguments when run, source
    # and target directories, plus the name of the script itself, as it counts as a command line argument.
    if len(args) != 3:
        raise Exception("You must pass a source and target directory.")

    # Only assigning the values beginning at index 1 to disregard the name of the script itself.
    source, target = args[1:]

    # Get current working directory, to join to path that was passed as an argument.
    # As an example, let's have cwd (the directory that this script is in) be:
    # "C:\Users\<name of user>\my_files\" or "/Users/<name of user/my_files/"
    cwd = os.getcwd()

    # Now let's assume that the folder containing all the games is called "my_games_folder", so now
    # "source_dir" will be "C:\Users\<name of user>\my_files\my_games_folder" or
    # "/Users/<name of user/my_files/my_games_folder"
    source_dir = os.path.join(cwd, source)

    # If the source directory cannot be found, exit the script.
    if not os.path.exists(source_dir):
        print("Source directory cannot be found.")
        sys.exit(1)

    # Let's assume that the "target" argument that was passed is "my_new_games_folder", now "target_dir" will be
    # "C:\Users\<name of user>\my_files\my_new_games_folder" or "/Users/<name of user/my_files/my_new_games_folder"
    target_dir = os.path.join(cwd, target)

    # Assume that the "source_dir" path contains folders that have the "GAME_DIR_PATTERN" in their names, get a list
    # of all of their paths.
    game_paths = find_all_game_paths(source_dir)

    print(game_paths)           # For testing.
    print(len(game_paths))      # For testing.

    # Create the folder that was passed as an argument, "C:\Users\<name of user>\my_files\my_new_games_folder" or
    # "/Users/<name of user/my_files/my_new_games_folder"
    create_dir(target_dir)

    # Get a list of only the game folders, without their paths or their suffixes.
    new_game_dirs = get_name_from_paths(game_paths, GAME_DIR_PATTERN)

    print(new_game_dirs)        # For testing.

    # The "zip" function pairs the elements of the passed lists according to their indices and returns them in a tuple.
    for src, dest in zip(game_paths, new_game_dirs):
        # Joins the "target_dir" and the new names of the folders.
        dest_path = os.path.join(target_dir, dest)
        # Copies all the game folders from their current location to the new location.
        copy_dirs(src, dest_path)

        # Calls the function that compiles the game code.
        compile_game_code(dest_path)

    # Creates a path for the metadata JSON file.
    metadata_file_path = os.path.join(target_dir, "metadata.json")

    # Calls the function and passes the metadata JSON file path and the new list of the game directories.
    make_json_metadata_file(metadata_file_path, new_game_dirs)

# =====================================================================================================================

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

# =====================================================================================================================

# A simple function that checks if the target directory exists or not, and if it doesn't, then it creates it.
def create_dir(target):

    if not os.path.exists(target):
        os.mkdir(target)

# =====================================================================================================================

def get_name_from_paths(paths, to_rmv):

    new_dir_names = []

    for path in paths:
        base_dir, dir_name = os.path.split(path)
        new_name = dir_name.replace(to_rmv, "")
        new_dir_names.append(new_name)

    return new_dir_names

# =====================================================================================================================

# This function recursively copies the directories from the source to the destination and overwrites any directory
# if it exists already.
def copy_dirs(source, dest):
    
    # If the destination path exists already, delete it recursively.
    if os.path.exists(dest):
        shutil.rmtree(dest)
    
    shutil.copytree(source,dest)

# =====================================================================================================================

# This function creates a file at "path" containing the names and number of game directories.
def make_json_metadata_file(path, game_dirs):

    # A dictionary of the information that will be used to create the file.
    data = {
        "gameNames": game_dirs,
        "numberOfGames": len(game_dirs)
    }

    # Create a file at path with "w" for write (and overwrite if it already exists).
    # The "with" statement cleans up and closes the file as soon as the code finishes running.
    with open(path, "w") as f:
        # "dump" (not to be confused with "dumps" for dump string) stores the object, in this case the "data"
        # dictionary, into the file.
        json.dump(data, f, indent=2)

# =====================================================================================================================

# This function compiles the game code by calling the "run_command" function.
def compile_game_code(path):

    code_file_name = None

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXTENSION):
                code_file_name = file
                break
        break

    if code_file_name is None:
        return
    
    command = GAME_FILE_COMPILE_COMMAND + [code_file_name]

    run_command(path, command)

# =====================================================================================================================

# This function runs any command that is passed to it.
def run_command(path, command):
    cwd = os.getcwd()
    
    # Changes the directory to the directory of the game's file(s).
    os.chdir(path)

    # Runs the command.
    result = run(command, stdin=PIPE, stdout=PIPE, universal_newlines=True)

    #print("The compile command result: ", result)

    # Changes the directory back to the same directory as the one in the beginning of the function.
    os.chdir(cwd)

# =====================================================================================================================

if __name__ == "__main__":
    main()

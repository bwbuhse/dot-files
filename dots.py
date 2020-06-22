#!/usr/bin/env python

import datetime
import json
import os
import shutil
import socket
import sys
from pathlib import Path
from typing import List

import git

from path_info import PathInfo

# Set to True to enable 'no git' mode
# While True, all pulling/committing/pushing to the git repo (by the script)
#   is disabled
# Used for updated this script without committing changes everytime that the
#   script is run
NO_GIT = False

# Set to True while updating this script
# This variable won't let you run the script without passing a commit message
#   but still lets you push the changes it copies
# This can be useful for making sure that the code still works but with a
#   useful commit message about the changes
EDITING_SCRIPT = False


def load_config() -> List[PathInfo]:
    if Path('config.json'):
        with open('config.json') as config:
            config = config.read()
            config = json.loads(config)

    paths: List[PathInfo] = []
    for path in config['paths']:
        path_pair = path['installed_path'], path['repo_path']
        files_to_copy = path.get('files_to_copy', [])
        dirs_to_copy = path.get('dirs_to_copy', [])
        paths.append(PathInfo(path_pair, files_to_copy, dirs_to_copy))

    return paths


# Directories to copy files from/to
HOSTNAME = 'host-' + socket.gethostname()
REPO_DIR_PATH = Path(os.path.dirname(os.path.realpath(__file__)))
REPO_HOSTNAME_PATH = Path(HOSTNAME)
PATHS: List[PathInfo] = load_config()


def pull(origin: git.Remote):
    if not NO_GIT:
        origin.pull()


def push(origin: git.Remote):
    if not NO_GIT:
        origin.push()


def add(repo: git.Repo):
    if not NO_GIT:
        repo.git.add('-A')


def commit(repo: git.Repo, message: str = None):
    if not NO_GIT:
        if message != None:
            repo.index.commit(message)
        else:
            repo.index.commit('Update files for ' + HOSTNAME +
                              ' ' + str(datetime.datetime.now()))


def save(message: str = None):
    '''
    Pulls any changes from the git repo.
    Deletes the directory in the repo for the current host then re-creates it.
    Copies all specified files to the directory for the host.
    Adds, commits, then pushes all the changes.

    If an argument is passed, it will replace the default commit message.
    '''
    os.chdir(REPO_DIR_PATH)
    repo = git.Repo(os.getcwd())
    origin = repo.remote()

    # Pull the git repo before updating anything
    pull(origin)

    # We remove the previous version so files that are no-longer there are removed
    if os.path.exists(HOSTNAME) and os.path.isdir(HOSTNAME):
        shutil.rmtree(HOSTNAME)
    REPO_HOSTNAME_PATH.mkdir()

    # Copy files/dirs from their original locations into the repo
    for path in PATHS:
        installed_path = Path.expanduser(Path(path.path_pair[0]))
        repo_path = REPO_HOSTNAME_PATH / path.path_pair[1]

        for dir_to_copy in path.dirs_to_copy:
            if (installed_path / dir_to_copy).exists():
                shutil.copytree(installed_path / dir_to_copy,
                                repo_path / dir_to_copy)

        for file_to_copy in path.files_to_copy:
            if '/' in file_to_copy:
                # We need to create any directories that don't exist already
                inner_dirs = file_to_copy[0:file_to_copy.rfind('/')]
                os.makedirs(repo_path / inner_dirs, exist_ok=True)
            if (installed_path / file_to_copy).exists():
                shutil.copy(installed_path / file_to_copy,
                            repo_path / file_to_copy)

    # We only want to make a commit if there was a change
    diff = repo.git.diff(REPO_HOSTNAME_PATH).strip()
    if len(diff) > 0:
        print('aadsfasdfadfs')
        # Commit, add, push all changes
        add(repo)
        if message != None:
            commit(repo, message)
        else:
            commit(repo)
        push(origin)


def install():
    '''
    Install dot-files from a specified host
    '''
    host_dir_paths = [x for x in REPO_DIR_PATH.iterdir(
    ) if x.is_dir() and x.name.startswith('host')]
    host_dict = {}
    for i in range(0, len(host_dir_paths)):
        host_dict[i] = host_dir_paths[i]

    if len(host_dir_paths) > 0:
        print('You have no saved hosts so there is nothing to install\n'
              'Exiting now...')

    print('Select a host to install from:')
    for index, host in host_dict.items():
        host = host.name[host.name.find('-') + 1:]
        print(f'[{index}] - {host}')

    selected_host = int(input('\n'))
    if selected_host not in host_dict:
        print(f'{selected_host} is not a valid host option.\n'
              f'Exiting now...')

    selected_host_path = host_dict[selected_host]

    # Copy files/dirs from the repo to their installed locations
    for path in PATHS:
        installed_path = Path.expanduser(Path(path.path_pair[0]))
        repo_path = selected_host_path / path.path_pair[1]

        for dir_to_copy in path.dirs_to_copy:
            if (selected_host_path / dir_to_copy).exists():
                shutil.copytree(installed_path / dir_to_copy,
                                repo_path / dir_to_copy,
                                dirs_exist_ok=True)

        for file_to_copy in path.files_to_copy:
            if '/' in file_to_copy:
                # We need to create any directories that don't exist already
                inner_dirs = file_to_copy[0:file_to_copy.rfind('/')]
                os.makedirs(installed_path / inner_dirs, exist_ok=True)
            if (selected_host_path / file_to_copy).exists():
                shutil.copy(selected_host_path / file_to_copy,
                            installed_path / file_to_copy)


def main(argv):
    if NO_GIT:
        print('Running in NO_GIT mode')
        print('Any changes to dot files will not be commited or pushed to the '
              'git repo\n')
    elif EDITING_SCRIPT and len(argv) < 3:
        print('Please enter a commit message as an argument while using '
              'EDITING_SCRIPT mode')
        print('Exiting now...')
        return

    if len(argv) <= 1:
        save()
    elif argv[1] == 'save':
        if len(argv) > 2:
            save(argv[2])
        else:
            save()
    elif argv[1] == 'install':
        install()
    else:
        print(argv[1], ' is not a valid argument for dots.py')


if __name__ == '__main__':
    main(sys.argv)

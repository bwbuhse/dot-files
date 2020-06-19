#!/usr/bin/env python

import sys
import os
import socket
import git
import shutil
import pathlib
import datetime

# Set to True to enable 'no git' mode
# While True, all pulling/committing/pushing to the git repo (by the script)
#   is disabled
# Used for updated this script without committing changes everytime that the
#   script is run
NO_GIT = True

# Set to True while updating this script
# This variable won't let you run the script without passing a commit message
#   but still lets you push the changes it copies
# This can be useful for making sure that the code still works but with a
#   useful commit message about the changes
EDITING_SCRIPT = True

# Directories to copy files from/to
HOSTNAME = 'host-' + socket.gethostname()
REPO_DIR_PATH = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
REPO_HOSTNAME_PATH = pathlib.Path(HOSTNAME)
REPO_HOSTNAME_CONFIG_PATH = REPO_HOSTNAME_PATH / '.config'
HOME_PATH = pathlib.Path.home()
HOME_DOT_CONFIG_PATH = HOME_PATH / '.config'

# Dictionaries used for matching directories
# Pairs of paths to copy from and their respective paths in the repo to copy to
PATH_PAIRS = {HOME_PATH: REPO_HOSTNAME_PATH,
              HOME_DOT_CONFIG_PATH: REPO_HOSTNAME_CONFIG_PATH}
# Files/directories to copy
FILES_TO_COPY = {HOME_PATH: ['.tmux.conf', '.zshrc', '.zprofile', '.zpreztorc'],
                 HOME_DOT_CONFIG_PATH: ['nvim/init.vim', 'nvim/coc-settings.json']}
DIRS_TO_COPY = {HOME_DOT_CONFIG_PATH: [
    'alacritty', 'sway', 'waybar', 'i3', 'polybar', 'picom']}


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
    REPO_HOSTNAME_CONFIG_PATH.mkdir()

    # Copy files/dirs from their original locations into the repo
    for installed_path, repo_path in PATH_PAIRS.items():
        dirs_to_copy = DIRS_TO_COPY.get(installed_path, {})
        files_to_copy = FILES_TO_COPY.get(installed_path, {})

        for dir_to_copy in dirs_to_copy:
            if (installed_path / dir_to_copy).exists():
                shutil.copytree(installed_path / dir_to_copy,
                                repo_path / dir_to_copy)

        for file_to_copy in files_to_copy:
            if '/' in file_to_copy:
                # We need to create any directories that don't exist already
                inner_dirs = file_to_copy[0:file_to_copy.rfind('/')]
                os.makedirs(repo_path / inner_dirs, exist_ok=True)
            if (installed_path / file_to_copy).exists():
                shutil.copy(installed_path / file_to_copy,
                            repo_path / file_to_copy)

    # Commit, add, push all changes
    add(repo)
    if message != None:
        commit(repo, message)
    else:
        commit(repo)
    push(origin)


def install():
    host_dir_paths = [x for x in REPO_DIR_PATH.iterdir(
    ) if x.is_dir() and x.name.startswith('host')]

    if len(host_dir_paths) == 0:
        print('You have no saved hosts so there is nothing to install\n'
              'Exiting now...')

    for host_dir_path in host_dir_paths:
        print(host_dir_path)


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

#!/usr/bin/env python

import sys
import os
import socket
import git
import shutil
import pathlib
import datetime

# Set to True to enable 'no git' mode
# While True, all pulling/committing/pushing to the git repo (by the script) is disabled
# Used for updated this script without committing changes everytime that the script is run
NO_GIT = False

# Set to True while updating this script
# This variable won't let you run the script without passing a commit message but still lets you push the changes it copies
# This can be useful for making sure that the code still works but with a useful commit message about the changes
EDITING_SCRIPT = True

# Directories to copy files from/to
HOSTNAME = socket.gethostname()
REPO_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
REPO_HOSTNAME_PATH = pathlib.Path(HOSTNAME)
REPO_HOSTNAME_CONFIG_PATH = REPO_HOSTNAME_PATH / '.config'
HOME_PATH = pathlib.Path.home()
HOME_DOT_CONFIG_PATH = HOME_PATH / '.config'

# Dictionaries used for matching directories
PATH_PAIRS = {HOME_PATH: REPO_HOSTNAME_PATH,
              HOME_DOT_CONFIG_PATH: REPO_HOSTNAME_CONFIG_PATH}


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
        if str != None:
            repo.index.commit(message)
        else:
            repo.index.commit('Update files for ' + HOSTNAME +
                              ' ' + str(datetime.datetime.now()))


def main(argv):
    '''
    Pulls any changes from the git repo.
    Deletes the directory in the repo for the current host then re-creates it.
    Copies all specified files to the directory for the host.
    Adds, commits, then pushes all the changes.

    If an argument is passed, it will replace the default commit message.
    '''
    if NO_GIT:
        print('Running in NO_GIT mode')
        print('Any changes to dot files will not be commited or pushed to the git repo\n')
    elif EDITING_SCRIPT and len(argv) == 1:
        print(
            'Please enter a commit message as an argument while using EDITING_SCRIPT mode')
        print('Exiting now...')
        return

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

    # Copy dot-files that are in ~/.config
    # Alacritty
    alacritty_dir_path = HOME_DOT_CONFIG_PATH / 'alacritty'
    if alacritty_dir_path.exists():
        shutil.copytree(alacritty_dir_path,
                        REPO_HOSTNAME_CONFIG_PATH / 'alacritty')

    # sway
    sway_dir_path = HOME_DOT_CONFIG_PATH / 'sway'
    if sway_dir_path.exists():
        shutil.copytree(sway_dir_path, REPO_HOSTNAME_CONFIG_PATH / 'sway')

    # waybar
    waybar_dir_path = HOME_DOT_CONFIG_PATH / 'waybar'
    if waybar_dir_path.exists():
        shutil.copytree(waybar_dir_path, REPO_HOSTNAME_CONFIG_PATH / 'waybar')

    # neovim
    neovim_dir_path = HOME_DOT_CONFIG_PATH / 'nvim'
    neovim_repo_dir_path = REPO_HOSTNAME_CONFIG_PATH / 'nvim'
    if neovim_dir_path.exists():
        if not neovim_repo_dir_path.exists():
            neovim_repo_dir_path.mkdir()
        shutil.copy(neovim_dir_path / 'init.vim',
                    neovim_repo_dir_path / 'init.vim')

        # coc.nvim configuration
        coc_dir_path = neovim_dir_path / 'coc-settings.json'
        if coc_dir_path.exists():
            shutil.copy(coc_dir_path, neovim_repo_dir_path)

    # i3
    i3_dir_path = HOME_DOT_CONFIG_PATH / 'i3'
    if i3_dir_path.exists():
        shutil.copytree(i3_dir_path, REPO_HOSTNAME_CONFIG_PATH / 'i3')

    # Polybar
    polybar_dir_path = HOME_DOT_CONFIG_PATH / 'polybar'
    if polybar_dir_path.exists():
        shutil.copytree(polybar_dir_path,
                        REPO_HOSTNAME_CONFIG_PATH / 'polybar')

    # picom
    picom_dir_path = HOME_DOT_CONFIG_PATH / 'picom'
    if picom_dir_path.exists():
        shutil.copytree(picom_dir_path, REPO_HOSTNAME_CONFIG_PATH / 'picom')

    # Copy dot-files that are directly in ~/
    # tmux
    tmux_path = HOME_PATH / '.tmux.conf'
    if tmux_path.exists():
        shutil.copy(tmux_path, REPO_HOSTNAME_PATH / '.tmux.conf')

    # zsh
    zshrc_path = HOME_PATH / '.zshrc'
    if zshrc_path.exists():
        shutil.copy(zshrc_path, REPO_HOSTNAME_PATH / '.zshrc')
        # Just assuming zprofile exists if zshrc does
        shutil.copy(HOME_PATH / '.zprofile', REPO_HOSTNAME_PATH / '.zprofile')

    # zpreztorc
    zpreztorc_path = HOME_PATH / '.zpreztorc'
    if zpreztorc_path.exists():
        shutil.copy(zpreztorc_path, REPO_HOSTNAME_PATH / '.zpreztorc')

    # Commit, add, push all changes
    add(repo)
    if len(argv) > 1:
        commit(repo, argv[1])
    else:
        commit(repo)
    push(origin)


if __name__ == '__main__':
    main(sys.argv)

#!/usr/bin/env python

import sys
import os
import socket
import git
import shutil
import pathlib
import datetime

# Set to True to enable debug mode
# While True, all pulling/committing/pushing to the git repo (by the script) is disabled
# Used for updated this script without committing changes everytime that the script is run
DEBUG = False

# Directories needed by the script
HOSTNAME = socket.gethostname()
HOSTNAME_DIR = pathlib.Path(HOSTNAME)
HOSTNAME_CONFIG_DIR = HOSTNAME_DIR / '.config'
REPO_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
HOME = pathlib.Path.home()
DOT_CONFIG = HOME / '.config'


def pull(origin: git.Remote):
    if not DEBUG:
        origin.pull()


def push(origin: git.Remote):
    if not DEBUG:
        origin.push()


def add(repo: git.Repo):
    if not DEBUG:
        repo.index.add('*')


def commit(repo: git.Repo):
    if not DEBUG:
        repo.index.commit('Update files for ' + HOSTNAME + ' ' + str(datetime.datetime.now()))


def main(argv):
    if DEBUG:
        print('Running in DEBUG mode')
        print('Any changes to dot files will not be commited or pushed to the git repo\n')

    os.chdir(REPO_DIR_PATH)
    repo = git.Repo(os.getcwd())
    origin = repo.remote()

    # Pull the git repo before updating anything
    pull(origin)

    # We remove the previous version so files that are no-longer there are removed
    if os.path.exists(HOSTNAME) and os.path.isdir(HOSTNAME):
        shutil.rmtree(HOSTNAME)
    HOSTNAME_DIR.mkdir()
    HOSTNAME_CONFIG_DIR.mkdir()

    # Copy dot-files that are in ~/.config
    # Alacritty
    alacritty_dir_path = DOT_CONFIG / 'alacritty'
    if alacritty_dir_path.exists():
        shutil.copytree(alacritty_dir_path, HOSTNAME_CONFIG_DIR / 'alacritty')

    # sway
    sway_dir_path = DOT_CONFIG / 'sway'
    if sway_dir_path.exists():
        shutil.copytree(sway_dir_path, HOSTNAME_CONFIG_DIR / 'sway')

    # waybar
    waybar_dir_path = DOT_CONFIG / 'waybar'
    if waybar_dir_path.exists():
        shutil.copytree(waybar_dir_path, HOSTNAME_CONFIG_DIR / 'waybar')

    # neovim
    neovim_dir_path = DOT_CONFIG / 'nvim'
    neovim_repo_dir_path = HOSTNAME_CONFIG_DIR / 'nvim'
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
    i3_dir_path = DOT_CONFIG / 'i3'
    if i3_dir_path.exists():
        shutil.copytree(i3_dir_path, HOSTNAME_CONFIG_DIR / 'i3')

    # Polybar
    polybar_dir_path = DOT_CONFIG / 'polybar'
    if polybar_dir_path.exists():
        shutil.copytree(polybar_dir_path, HOSTNAME_CONFIG_DIR / 'polybar')

    # picom
    picom_dir_path = DOT_CONFIG / 'picom'
    if picom_dir_path.exists():
        shutil.copytree(picom_dir_path, HOSTNAME_CONFIG_DIR / 'picom')

    # Copy dot-files that are directly in ~/
    # tmux
    tmux_path = HOME / '.tmux.conf'
    if tmux_path.exists():
        shutil.copy(tmux_path, HOSTNAME_DIR / '.tmux.conf')

    # zsh
    zshrc_path = HOME / '.zshrc'
    if zshrc_path.exists():
        shutil.copy(zshrc_path, HOSTNAME_DIR / '.zshrc')
        # Just assuming zprofile exists if zshrc does
        shutil.copy(HOME / '.zprofile', HOSTNAME_DIR / '.zprofile')

    # zpreztorc
    zpreztorc_path = HOME / '.zpreztorc'
    if zpreztorc_path.exists():
        shutil.copy(zpreztorc_path, HOSTNAME_DIR / '.zpreztorc')

    # Commit, add, push all changes
    add(repo)
    commit(repo)
    push(origin)


if __name__ == '__main__':
    main(sys.argv)

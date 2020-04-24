#!/bin/zsh

# Pull branch
git pull

##### .config stuf ####
# Alacritty
cp -r ~/.config/alacritty .config/

# sway
cp -r ~/.config/sway .config/

# waybar
cp -r ~/.config/waybar .config/

#### ~ stuff  ####
# tmux
cp ~/.tmux.conf .

# vim
cp ~/.vimrc .

# zsh stuff
cp ~/.zpreztorc .
cp ~/.zshrc .
cp ~/.zprofile .

# Commit and push
git add -A
git commit -m "Update files $(date +%Y.%m.%d-%H:%M:%S)"
git push

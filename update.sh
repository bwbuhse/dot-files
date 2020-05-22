#!/bin/zsh

# Pull branch
git pull

##### .config stuf ####
# Alacritty
cp -r /home/ben/.config/alacritty .config/

# sway
cp -r /home/ben/.config/sway .config/

# waybar
cp -r /home/ben/.config/waybar .config/

#### ~ stuff  ####
# tmux
cp /home/ben/.tmux.conf .

# vim
cp /home/ben/.vimrc .

# zsh stuff
cp /home/ben/.zpreztorc .
cp /home/ben/.zshrc .
cp /home/ben/.zprofile .

# neovim stuff
cp -r /home/ben/.config/nvim .config/

# Commit and push
git add -A
git commit -m "Update files $(date +%Y.%m.%d-%H:%M:%S)"
git push

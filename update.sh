#!/bin/zsh

# Used to determine which directory to copy into
HOST=$(uname -n)

# Pull branch
git pull

##### .config stuf ####
# Alacritty
cp -r /home/ben/.config/alacritty $HOST/.config/

# sway
cp -r /home/ben/.config/sway $HOST/.config/

# waybar
cp -r /home/ben/.config/waybar $HOST/.config/

# neovim stuff
cp /home/ben/.config/nvim/init.vim $HOST/.config/nvim/

#### ~ stuff  ####
# tmux
cp /home/ben/.tmux.conf $HOST/.

# vim
cp /home/ben/.vimrc $HOST/.

# zsh stuff
cp /home/ben/.zpreztorc $HOST/.
cp /home/ben/.zshrc $HOST/.
cp /home/ben/.zprofile $HOST.

# Commit and push
git add -A
git commit -m "Update files for $HOST $(date +%Y.%m.%d-%H:%M:%S)"
git push

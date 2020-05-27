#!/bin/bash

# Used to determine which directory to copy into
HOST=$(uname -n)
if [ ! -e $HOST ]; then
  mkdir $HOST
fi

# Pull branch
git pull

##### .config stuff ####
# Alacritty
if [ -e /home/ben/.config/alacritty ]; then
  cp -r /home/ben/.config/alacritty $HOST/.config/
fi

# sway
if [ -e /home/ben/.config/sway ]; then
    cp -r /home/ben/.config/sway $HOST/.config/
fi

# waybar
if [ -e /home/ben/.config/waybar ]; then
  cp -r /home/ben/.config/waybar $HOST/.config/
fi

# neovim stuff
if [ -e /home/ben/.config/nvim ]; then
  if [ ! -e $HOST/.config/nvim ]; then
    cp /home/ben/.config/nvim/init.vim $HOST/.config/nvim/
  fi
fi

# coc.nvim
if [ -e /home/ben/.config/coc ]; then
  cp -r /home/ben/.config/coc $HOST/.config/coc/
fi

# Polybar
if [ -e /home/ben/.config/polybar ]; then
  cp -r ~/.config/polybar $HOST/.config    
fi

# i3
if [ -e /home/ben/.config/i3 ]; then
  cp -r ~/.config/i3 $HOST/.config
fi

# picom
if [ -e /home/ben/.config/picom ]; then
  cp -r ~/.config/picom $HOST/.config
fi

#### ~ stuff  ####
# tmux
if [ -e /home/ben/.tmux.conf ]; then
  cp /home/ben/.tmux.conf $HOST/.
fi

# zsh stuff
if [ -e /home/ben/.zshrc ]; then
  cp /home/ben/.zpreztorc $HOST/.
  cp /home/ben/.zshrc $HOST/.
  cp /home/ben/.zprofile $HOST/.
fi

# Commit and push
git add -A
git commit -m "Update files for $HOST $(date +%Y.%m.%d-%H:%M:%S)"
git push

# Update prezto too!
if [ -e /home/ben/.zprezto ]; then
  (
    cd ~/.zprezto
    git pull
    git add -u
    git commit -m "Update files from $HOST $(date +%Y.%m.%d-%H:%M:%S)"
    git push
  )
fi

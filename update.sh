#!/bin/bash

cd /home/$USER/projects/dot-files/

# Used to determine which directory to copy into
HOST=$(uname -n)
if [ -e $HOST ]; then
  rm -rf $HOST
fi
mkdir $HOST

# Pull branch
git pull

##### .config stuff ####
# Alacritty
if [ -e /home/$USER/.config/alacritty ]; then
  cp -r /home/$USER/.config/alacritty $HOST/.config/
fi

# sway
if [ -e /home/$USER/.config/sway ]; then
    cp -r /home/$USER/.config/sway $HOST/.config/
fi

# waybar
if [ -e /home/$USER/.config/waybar ]; then
  cp -r /home/$USER/.config/waybar $HOST/.config/
fi

# neovim stuff
if [ -e /home/$USER/.config/nvim ]; then
  if [ ! -e $HOST/.config/nvim ]; then
    mkdir $HOST/.config/nvim
  fi
  cp /home/$USER/.config/nvim/init.vim $HOST/.config/nvim/
fi

# coc.nvim
if [ -e /home/$USER/.config/coc ]; then
  cp -r /home/$USER/.config/coc $HOST/.config/coc/
fi

# Polybar
if [ -e /home/$USER/.config/polybar ]; then
  cp -r ~/.config/polybar $HOST/.config    
fi

# i3
if [ -e /home/$USER/.config/i3 ]; then
  cp -r ~/.config/i3 $HOST/.config
fi

# picom
if [ -e /home/$USER/.config/picom ]; then
  cp -r ~/.config/picom $HOST/.config
fi

#### ~ stuff  ####
# tmux
if [ -e /home/$USER/.tmux.conf ]; then
  cp /home/$USER/.tmux.conf $HOST/.
fi

# zsh stuff
if [ -e /home/$USER/.zshrc ]; then
  cp /home/$USER/.zpreztorc $HOST/.
  cp /home/$USER/.zshrc $HOST/.
  cp /home/$USER/.zprofile $HOST/.
fi

# Commit and push
git add -A
git commit -m "Update files for $HOST $(date +%Y.%m.%d-%H:%M:%S)"
git push

# Update prezto too!
if [ -e /home/$USER/.zprezto ]; then
  (
    cd ~/.zprezto
    git pull
    git add -u
    git commit -m "Update files from $HOST $(date +%Y.%m.%d-%H:%M:%S)"
    git push
  )
fi

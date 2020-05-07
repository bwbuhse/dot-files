# The following lines were added by compinstall

zstyle ':completion:*' completer _expand _complete _ignored _correct _approximate
zstyle ':completion:*' format 'Completing %d'
zstyle ':completion:*' matcher-list '' '' '' 'r:|[._-]=** r:|=**'
zstyle :compinstall filename '/home/ben/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall
# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
setopt autocd extendedglob nomatch notify
bindkey -v
# End of lines configured by zsh-newuser-install

##############
# my zsh cfg #
##############

# Load uh... the prompt?
autoload -Uz promptinit
promptinit

# Fuzzy finder - find in file
# find-in-file - usage: fif <searchTerm>
fif() {
  if [ ! "$#" -gt 0 ]; then echo "Need a string to search for!"; return 1; fi
  rg --files-with-matches --no-messages "$1" | fzf --preview "highlight -O ansi -l {} 2> /dev/null | rg --colors 'match:bg:yellow' --ignore-case --pretty --context 10 '$1' || rg --ignore-case --pretty --context 10 '$1' {}"
}

# Detach from current tmux session and create a new one
# tmdn() { 
#   if [[ -v $1 ]]; then 
#     tmux detach -E "tmux new -A -s '$1'"; 
#   else
#     echo 'You need to give a session name';
#   fi
# }

# tmda() {
#   if [[ -v $1 ]]; then 
#     tmux detach -E "tmux attach -t '$1'"; 
#   else
#     echo 'You need to give a session name';
#   fi
# }


#########################
# update terminal title #
#########################

autoload -Uz add-zsh-hook

function xterm_title_precmd () {
	print -Pn -- '\e]2;%n@%m %~\a'
	[[ "$TERM" == 'screen'* ]] && print -Pn -- '\e_\005{g}%n\005{-}@\005{m}%m\005{-} \005{B}%~\005{-}\e\\'
}

function xterm_title_preexec () {
	print -Pn -- '\e]2;%n@%m %~ %# ' && print -n -- "${(q)1}\a"
	[[ "$TERM" == 'screen'* ]] && { print -Pn -- '\e_\005{g}%n\005{-}@\005{m}%m\005{-} \005{B}%~\005{-} %# ' && print -n -- "${(q)1}\e\\"; }
}

if [[ "$TERM" == (alacritty*|gnome*|konsole*|putty*|rxvt*|screen*|tmux*|xterm*) ]]; then
	add-zsh-hook -Uz precmd xterm_title_precmd
	add-zsh-hook -Uz preexec xterm_title_preexec
fi



##############
# my aliases #
##############

alias ll='exa -l'
alias exa='exa -l'
alias cat='bat'

alias kill-zoom='pkill -9 -f zoom'

alias pacman-deps="pacman -Qi | sed '/^Depends On/,/^Required By/{ s/^Required By.*$//; H; d }; /^Name/!d; /^Name/{ n;x;}'| sed '/^$/s//==================================================================================/'"

alias vimf='cscope -Rb && vim $(fzf)'

# Used to log into the kamek server that UT has with one command
alias kamek='ssh bbuhse@kamek.ece.utexas.edu'

# Stuff
alias pac=yay  # For convenience

# pacmatic needs to be run as root: https://github.com/keenerd/pacmatic/issues/35
alias pacmatic='sudo --preserve-env=pacman_program /usr/bin/pacmatic'

# Downgrade permissions as AUR helpers expect to be run as a non-root user. $UID is read-only in {ba,z}sh.
alias yay='pacman_program="sudo -u #$UID /usr/bin/yay --pacman powerpill" pacmatic'

alias vi='vim'


##############
# my exports #
##############

# These lines are just for ee461s
export PINTOS=/home/ben/projects/os-sp20-team-bumo

# For rust stuff ?? 
export PATH=$PATH:$PINTOS/utils:/home/ben/.cargo/bin

# Set VA-API driver
export LIBVA_DRIVER_NAME='iHD'

# Run presto
source "${ZDOTDIR:-$HOME}/.zprezto/init.zsh"

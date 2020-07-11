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

export WORKON_HOME=~/.virtualenvs
source /usr/bin/virtualenvwrapper_lazy.sh

##############
# my aliases #
##############

alias ll='exa -l'
alias exa='exa -l'
alias cat='bat'

alias pacman-deps="pacman -Qi | sed '/^Depends On/,/^Required By/{ s/^Required By.*$//; H; d }; /^Name/!d; /^Name/{ n;x;}'| sed '/^$/s//==================================================================================/'"

alias pac=yay  # For convenience

alias vi='nvim'

alias vim='nvim'

##############
# my exports #
##############

# For Rust
export PATH=$PATH:$PINTOS/utils:/home/ben/.cargo/bin

# Set VA-API driver
export LIBVA_DRIVER_NAME='vdpau'
export VDPAU_DRIVER='nvidia'

# Source prezto
source "${ZDOTDIR:-$HOME}/.zprezto/init.zsh"

# set alacritty as my default terminal
export TERMINAL='konsole'
alias config='/usr/bin/git --git-dir=/home/ben/.cfg/ --work-tree=/home/ben'

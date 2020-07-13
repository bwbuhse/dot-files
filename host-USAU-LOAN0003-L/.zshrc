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

##############
# my aliases #
##############

alias ll='exa -l'
alias exa='exa -l'

alias vimf='cscope -Rb && vim $(fzf)'

alias vi='nvim'

alias vim='nvim'

alias labvm='ssh benjaminb@tpcvm29.tplab.tippingpoint.com'

##############
# my exports #
##############

# For rust stuff ?? 
export PATH=$PATH:$PINTOS/utils:/home/ben/.cargo/bin

# Run presto
source "${ZDOTDIR:-$HOME}/.zprezto/init.zsh"


" vim-plug stuff
if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

call plug#begin()

Plug 'arcticicestudio/nord-vim'

Plug 'tpope/vim-sensible'

Plug 'sheerun/vim-polyglot'

Plug 'Valloric/YouCompleteMe', { 'do': './install.py --clang-completer --omnisharp-completer' }

Plug 'vim-syntastic/syntastic'

Plug 'dr-kino/cscope-maps'

Plug 'rdnetto/YCM-Generator', { 'branch': 'stable'}

Plug 'tpope/vim-commentary'

Plug 'junegunn/fzf'

Plug 'rust-lang/rust.vim'

call plug#end()

" general stuff
set number

set tabstop=8 softtabstop=0 expandtab shiftwidth=2 smarttab

set encoding=utf-8

syntax on

colorscheme nord

if has('cscope')
  set cscopetag cscopeverbose

  if has('quickfix')
    set cscopequickfix=s-,c-,d-,i-,t-,e-
  endif

  cnoreabbrev csa cs add
  cnoreabbrev csf cs find
  cnoreabbrev csk cs kill
  cnoreabbrev csr cs reset
  cnoreabbrev css cs show
  cnoreabbrev csh cs help

  command -nargs=0 Cscope cs add $VIMSRC/src/cscope.out $VIMSRC/src
endif

" Use clang-format when saving
function! Formatonsave()
  let l:formatdiff = 1
  py3f ~/opt/clang-format.py
endfunction
autocmd BufWritePre *.h,*.c,*.cpp call Formatonsave()

" C-k to use clang-format
map <C-K> :py3f ~/opt/clang-format.py<cr>
imap <C-K> <c-o>:py3f ~/opt/clang-format.py<cr>

" Make comments brighter ?
" hi Comment ctermfg=LightBlue

" Syntastic Reccomendations for Newbies
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 1
let g:syntastic_check_on_wq = 0
let g:syntastic_c_compiler_options = '-nostdinc -I$PINTOS/lib/ -I$PINTOS/lib/kernel/ -I$PINTOS/lib/user/'

let g:ycm_show_diagnostics_ui = 0
let g:ycm_confirm_extra_conf = 0

" Always enable preview window on the right with 60% width
let g:fzf_preview_window = 'right:60%'

" Enable rustfmt on buffer same
let g:rustfmt_autosave = 1

" Highlight active line number
let g:nord_cursor_line_number_background = 1

set nocscopeverbose

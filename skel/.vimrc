" MacOS modifier key settings: Ctrl->Opt, Opt->Ctrl, CapsLock->Ctl (avoiding chords)
" Other settings designed to help avoid over-use of left little finger.
"  for some advice, much not followed
"   https://danielmiessler.com/study/vim/  and
"   https://stevelosh.com/blog/2010/09/coming-home-to-vim/#using-the-leader
"   Ack plugin installed: git clone https://github.com/mileszs/ack.vim.git ~/.vim/bundle/ack.vim

let mapleader = ";"
" alias ;a to escape key
inoremap <leader>a <ESC>
nnoremap <leader>a <ESC>
vnoremap <leader>a <ESC>
" alias ;l to escape key
inoremap <leader>l <ESC>
nnoremap <leader>l <ESC>
vnoremap <leader>l <ESC>
" alias ;; to escape key
inoremap <leader><leader> ;
nnoremap <leader><leader> ;
vnoremap <leader><leader> ;
" re-expose ; as ;, -- maybe it should be <tab>?
"nnoremap <leader>, ;

" alias SP to : since : requres shift (a chord) for very common key
nnoremap <space> :
"        │     (nb: '│' != '|')
"        └─── mnemonic: go to "space" along full bottom of screen (or keyboard)
" nnoremap : ;

" nnoremap <leader>, ,
" plugin support
" filetype off		" need filetype off for this next line
" execute pathogen#infect()
" filetype plugin indent on
set nocompatible	" turn off vi compatibility
set modelines=0		" for security

" set clipboard=unnamedplus
" nnoremap / /\v
" vnoremap / /\v

set ignorecase
set smartcase
set gdefault		" appends g by default to s///; add g yourself to stop

set showmatch
" keep annoying search highlighting off except temporarily when I hit \
hi Search ctermbg=Brown
set nohlsearch
nnoremap \\ :set hlsearch<cr>:sleep 1<cr>:set nohlsearch<cr>
inoremap <leader><TAB> <ESC>
" these tab settings seem a wasted opportunity
nnoremap <tab> %
vnoremap <tab> %

syntax on
autocmd Filetype python setlocal expandtab tabstop=4 shiftwidth=4 softtabstop=4
set background=dark
set vb t_vb=
set spelllang=en_us
set nojoinspaces
set encoding=utf-8
set wrapmargin=1
set mouse=h
set formatoptions=ltcq1j
set ruler
set ai ic

" nnoremap <leader>f :+,$!msfold''
" rarer: [ = turn off ai,ic; ] = turn them on again
nnoremap <leader>[ :set noai noic
nnoremap <leader>] :set ai ic
" nnoremap <leader>e F<yf>Pls </hhi
" nnoremap <leader>g 70| 
" nnoremap <leader>j 76|F 
" nnoremap <leader>h 71|F 
" nnoremap <leader>n :w:nn
" like Cmd C for paste/put
nnoremap <leader>c m'"my'm''
nnoremap <leader>d "md'm
nnoremap <leader>e :e
nnoremap <leader>f :file<space>
nnoremap <leader>i "mP
nnoremap <leader>k i<C-R>=strftime("%Y.%m.%d")<CR><CR><ESC>
" for creating new NAAN registry entries
nnoremap <leader>m !/---vim_naan
nnoremap <leader>n :n
nnoremap <leader>q :quit
nnoremap <leader>r :'m,.
nnoremap <leader>t :e#
" like Cmd V for paste/put
nnoremap <leader>p "mp
nnoremap <leader>g gqj
nnoremap <leader>v "mp
nnoremap <leader>w :w
inoremap <leader>w <ESC>:w
" nnoremap <leader>w :w
" like Cmd X for paste/put
nnoremap <leader>x "md'm
" yank to buffer
nnoremap <leader>y m'"my'm''
nnoremap <leader>z :suspend
" nnoremap <leader>zz :w:suspend
" nnoremap <leader>wn :w:n
" nnoremap <leader>wq :w:q
" nnoremap <leader>nn :w:nn
" nnoremap <leader>v !/---./vim_naan
"
" nnoremap <leader>w <C-w>s<C-w>j
" trying out alternates to keep left hand from stretching with control key
"   C-j,k -> C-f,b
" Add aliases <C-j>/C-k> for forward and back, as they're less of a hand stretch and
" unlike <C-f>/<C-b>, <C-d>/<C-u> generally keep cursor position on same screen line.
nnoremap <C-j> <C-d><C-d>
nnoremap <C-k> <C-u><C-u>
" nnoremap <C-h> <C-w>h
" nnoremap <C-j> <C-w>j
" nnoremap <C-k> <C-w>k
" nnoremap <C-l> <C-w>l

" nnoremap <leader>x :e xG"mp
" nnoremap <leader>l /^........................................................................./
" nnoremap <leader>o :/^Date:/co'z:s/[^0-9]*\([^-+]*\).*/\1/:/^From:/m'z:s/$/,/J:.g/:[^<]*<\([^>]*\)>/s//: \1/
" drop these?
" nnoremap <leader>^ :,$s/^/> /''
" nnoremap <leader>& :,$s/^> \?//''
" nnoremap <leader>1 :pu s1G"spWifyi - oBcc: m/j/^Subject:

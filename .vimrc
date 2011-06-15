
set t_Co=256
colorscheme zenburn "low-res, in hall/putty
"colorscheme molokai "high-res, in hall/putty
"colorscheme robokai
set cul
filetype plugin on
filetype plugin indent on
set grepprg=grep\ -nH\ $*
let g:tex_flavor='latex'
au! fileType tex setl tw=78

set si et sc ts=2 sw=2 sts=2
map Q gq
nmap gf :tabedit <cfile><CR>
"cmap W w
"cmap Q q
" too annoying..

au! BufRead,BufNewFile *.cgi setl syn=python
autocmd BufRead,BufNewFile *.py syntax on
autocmd BufRead *.py setl cinwords=if,elif,else,for,while,with,try,except,finally,def,class
au FileType python setl et ts=4 sw=4 sts=4 omnifunc=pythoncomplete#Complete

au! BufRead,BufNewFile *.c setl et ts=4 sw=4 sts=4 "c code: 4
au! BufRead,BufNewFile *.l setl et ts=4 sw=4 sts=4 "lex code: 4
au! BufRead,BufNewFile *.y setl si et ts=4 sw=4 sts=4 "yacc code: 4
au! BufRead,BufNewFile *.h setl et ts=4 sw=4 sts=4 "c header: 4
au! BufRead,BufNewFile *.json setfiletype javascript
au! BufRead,BufNewFile *.omml setfiletype omml
au! BufRead,BufNewFile *.scm setl syn=scheme et ts=2 sw=2 sts=2 tw=78 "scheme
au! BufRead,BufNewFile *.s setl et ts=8 sw=8 sts=8

au FileType make setl ts=8 sw=8 sts=8

au FileType html setl omnifunc=htmlcomplete#CompleteTags
au FileType javascript setl omnifunc=javascriptcomplete#CompleteJS
au! BufRead,BufNewFile *.htm setl syntax=htmldjango
au FileType htmldjango setl omnifunc=htmlcomplete#CompleteTags
au FileType css setl omnifunc=csscomplete#CompleteCSS et ts=4 sw=4 sts=4
au FileType php setl omnifunc=phpcomplete#CompletePHP

au BufRead,BufNewFile *.txt setf text
au FileType text syntax off
au BufRead,BufNewFile *.raw setf rawfile
au FileType rawfile syntax off

au! BufRead,BufNewFile *.nc setfiletype nc


" Wrap text after a certain number of characters
" Python: 79 
" C: 79
au BufRead,BufNewFile *.py,*.pyw,*.c,*.h set textwidth=79

" Turn off settings in 'formatoptions' relating to comment formatting.
" - c : do not automatically insert the comment leader when wrapping based on
"    'textwidth'
" - o : do not insert the comment leader when using 'o' or 'O' from command mode
" - r : do not insert the comment leader when hitting <Enter> in insert mode
" Python: not needed
" C: prevents insertion of '*' at the beginning of every line in a comment
au BufRead,BufNewFile *.c,*.h set formatoptions-=c formatoptions-=o formatoptions-=r

" Use UNIX (\n) line endings.
" Only used for new files so as to not force existing files to change their
" line endings.
" Python: yes
" C: yes
au BufNewFile *.py,*.pyw,*.c,*.h set fileformat=unix


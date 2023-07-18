set nocompatible

filetype on

" syntax highlighting
syntax on

set statusline+=%y             " Filetype
set statusline+=\ %f           " Filename
set statusline+=\ %m           " Modified flag, text is [+] or [-]
set statusline+=\ %r           " Readonly flag, text is [RO]
set statusline+=%=             " Left to Right seperator
set statusline+=\ line:\ %l/%L " Row out of Rows
set statusline+=\ col:\ %c     " Column

set laststatus=2               " Status on the second to last line

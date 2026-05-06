" ===============================================================
" Spectral Light
" Warm paper with burnt-amber signature and balanced accents.
" Maintainer:   iain
" License:      MIT
" GENERATED FILE — edit tools/palette.py and regenerate.
" ===============================================================

hi clear
if exists('syntax_on')
  syntax reset
endif

set background=light
let g:colors_name = 'spectral-light'

let s:amber = {'gui': '#9D6300', 'cterm': '130'}

call spectral#apply({
  \ 'bg':        {'gui': '#FEF4DF', 'cterm': '230'},
  \ 'bg_alt':    {'gui': '#F6EAD1', 'cterm': '224'},
  \ 'bg_alt2':   {'gui': '#E7D9BD', 'cterm': '187'},
  \ 'fg_dark':   {'gui': '#6E6249', 'cterm': '59'},
  \ 'fg_darker': {'gui': '#5D5139', 'cterm': '59'},
  \ 'fg_alt':    {'gui': '#463C28', 'cterm': '58'},
  \ 'fg_light':  {'gui': '#171105', 'cterm': '233'},
  \ 'fg':        {'gui': '#2B2313', 'cterm': '234'},
  \ 'white':     {'gui': '#FFFFFF', 'cterm': '231'},
  \ 'red':       {'gui': '#AC1A1C', 'cterm': '124'},
  \ 'orange':    {'gui': '#9C4700', 'cterm': '130'},
  \ 'yellow':    {'gui': '#906B00', 'cterm': '94'},
  \ 'green':     {'gui': '#357426', 'cterm': '64'},
  \ 'cyan':      {'gui': '#00707E', 'cterm': '24'},
  \ 'purple':    {'gui': '#65389F', 'cterm': '61'},
  \ 'black':     {'gui': '#000000', 'cterm': '16'},
  \ 'tab_bg':    {'gui': '#EFE3CB', 'cterm': '224'},
  \ })

" Amber accents: anchor the palette on a few high-frequency elements so
" the signature color keeps its presence without dominating body text.
let s:fg = 'guifg=' . s:amber.gui . ' ctermfg=' . s:amber.cterm
exe 'hi Directory     ' . s:fg
exe 'hi netrwDir      ' . s:fg
exe 'hi netrwDirSlash ' . s:fg
exe 'hi netrwClassify ' . s:fg
exe 'hi rubySymbol    ' . s:fg

" vim: set sw=2 ts=2 sts=2 et tw=80 ft=vim:

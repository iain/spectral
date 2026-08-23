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

let s:amber = {'gui': '#A76C01', 'cterm': '130'}

call spectral#apply({
  \ 'bg':        {'gui': '#FFFAEE', 'cterm': '231'},
  \ 'bg_alt':    {'gui': '#F6EAD1', 'cterm': '224'},
  \ 'bg_alt2':   {'gui': '#E7D9BD', 'cterm': '187'},
  \ 'fg_dark':   {'gui': '#6E6249', 'cterm': '59'},
  \ 'fg_darker': {'gui': '#5D5139', 'cterm': '59'},
  \ 'fg_alt':    {'gui': '#463C28', 'cterm': '58'},
  \ 'fg_light':  {'gui': '#171105', 'cterm': '233'},
  \ 'fg':        {'gui': '#2B2313', 'cterm': '234'},
  \ 'white':     {'gui': '#FFFFFF', 'cterm': '231'},
  \ 'red':       {'gui': '#BB0916', 'cterm': '124'},
  \ 'orange':    {'gui': '#C83E01', 'cterm': '166'},
  \ 'yellow':    {'gui': '#AD8600', 'cterm': '136'},
  \ 'green':     {'gui': '#1A7F11', 'cterm': '28'},
  \ 'cyan':      {'gui': '#007A85', 'cterm': '30'},
  \ 'blue':      {'gui': '#0053A4', 'cterm': '25'},
  \ 'purple':    {'gui': '#791DC7', 'cterm': '92'},
  \ 'black':     {'gui': '#000000', 'cterm': '16'},
  \ 'tab_bg':    {'gui': '#EFE3CB', 'cterm': '224'},
  \ 'amber':     {'gui': '#A76C01', 'cterm': '130'},
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

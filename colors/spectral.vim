" ===============================================================
" Spectral
" A Vim colorscheme based on Monokai Pro Spectrum
" Maintainer:   iain
" License:      MIT
" ===============================================================

hi clear
if exists('syntax_on')
  syntax reset
endif

set background=dark
let g:colors_name = 'spectral'

call spectral#apply({
  \ 'bg':        {'gui': '#181818', 'cterm': '234'},
  \ 'bg_alt':    {'gui': '#363537', 'cterm': '236'},
  \ 'bg_alt2':   {'gui': '#525053', 'cterm': '239'},
  \ 'fg_dark':   {'gui': '#69676c', 'cterm': '242'},
  \ 'fg_darker': {'gui': '#8b888f', 'cterm': '245'},
  \ 'fg_alt':    {'gui': '#bab6bf', 'cterm': '250'},
  \ 'fg_light':  {'gui': '#f7f1ff', 'cterm': '255'},
  \ 'fg':        {'gui': '#fbf8ff', 'cterm': '231'},
  \ 'white':     {'gui': '#ffffff', 'cterm': '231'},
  \ 'red':       {'gui': '#fc618d', 'cterm': '204'},
  \ 'orange':    {'gui': '#fd9353', 'cterm': '209'},
  \ 'yellow':    {'gui': '#fce566', 'cterm': '227'},
  \ 'green':     {'gui': '#7bd88f', 'cterm': '114'},
  \ 'cyan':      {'gui': '#5ad4e6', 'cterm': '81'},
  \ 'purple':    {'gui': '#948ae3', 'cterm': '141'},
  \ 'black':     {'gui': '#000000', 'cterm': '16'},
  \ 'tab_bg':    {'gui': '#000000', 'cterm': '16'},
  \ })

" vim: set sw=2 ts=2 sts=2 et tw=80 ft=vim:

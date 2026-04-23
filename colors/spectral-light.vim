" ===============================================================
" Spectral Light
" A Vim colorscheme based on Monokai Pro Light
" Maintainer:   iain
" License:      MIT
" ===============================================================

hi clear
if exists('syntax_on')
  syntax reset
endif

set background=light
let g:colors_name = 'spectral-light'

call spectral#apply({
  \ 'bg':        {'gui': '#fafafa', 'cterm': '231'},
  \ 'bg_alt':    {'gui': '#eff0eb', 'cterm': '255'},
  \ 'bg_alt2':   {'gui': '#d9dbd2', 'cterm': '252'},
  \ 'fg_dark':   {'gui': '#a29fa0', 'cterm': '247'},
  \ 'fg_darker': {'gui': '#797575', 'cterm': '243'},
  \ 'fg_alt':    {'gui': '#626262', 'cterm': '241'},
  \ 'fg_light':  {'gui': '#404040', 'cterm': '238'},
  \ 'fg':        {'gui': '#373431', 'cterm': '237'},
  \ 'white':     {'gui': '#ffffff', 'cterm': '231'},
  \ 'red':       {'gui': '#c33c67', 'cterm': '161'},
  \ 'orange':    {'gui': '#c36a2d', 'cterm': '166'},
  \ 'yellow':    {'gui': '#8c8a00', 'cterm': '100'},
  \ 'green':     {'gui': '#259338', 'cterm': '29'},
  \ 'cyan':      {'gui': '#0089a1', 'cterm': '31'},
  \ 'purple':    {'gui': '#6251b3', 'cterm': '61'},
  \ 'black':     {'gui': '#000000', 'cterm': '16'},
  \ 'tab_bg':    {'gui': '#f0f0f0', 'cterm': '255'},
  \ })

" vim: set sw=2 ts=2 sts=2 et tw=80 ft=vim:

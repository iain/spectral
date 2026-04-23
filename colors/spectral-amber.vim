" ===============================================================
" Spectral Amber
" Amber CRT phosphor on OLED black, with cool accents for balance.
" Maintainer:   iain
" License:      MIT
" ===============================================================

hi clear
if exists('syntax_on')
  syntax reset
endif

set background=dark
let g:colors_name = 'spectral-amber'

call spectral#apply({
  \ 'bg':        {'gui': '#000000', 'cterm': '16'},
  \ 'bg_alt':    {'gui': '#1F1208', 'cterm': '234'},
  \ 'bg_alt2':   {'gui': '#3D2817', 'cterm': '236'},
  \ 'fg_dark':   {'gui': '#5C4410', 'cterm': '58'},
  \ 'fg_darker': {'gui': '#8B6914', 'cterm': '94'},
  \ 'fg_alt':    {'gui': '#CC8800', 'cterm': '172'},
  \ 'fg_light':  {'gui': '#FFD180', 'cterm': '222'},
  \ 'fg':        {'gui': '#FFB000', 'cterm': '214'},
  \ 'white':     {'gui': '#FFFFFF', 'cterm': '231'},
  \ 'red':       {'gui': '#FF3B30', 'cterm': '203'},
  \ 'orange':    {'gui': '#FF7A1C', 'cterm': '208'},
  \ 'yellow':    {'gui': '#FFD60A', 'cterm': '220'},
  \ 'green':     {'gui': '#B5E853', 'cterm': '149'},
  \ 'cyan':      {'gui': '#30D5C8', 'cterm': '80'},
  \ 'purple':    {'gui': '#C678DD', 'cterm': '176'},
  \ 'black':     {'gui': '#000000', 'cterm': '16'},
  \ 'tab_bg':    {'gui': '#140A05', 'cterm': '232'},
  \ })

" vim: set sw=2 ts=2 sts=2 et tw=80 ft=vim:

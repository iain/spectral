" ===============================================================
" Spectral Light
" Warm paper with burnt-amber signature and balanced accents.
" Maintainer:   iain
" License:      MIT
" ===============================================================

hi clear
if exists('syntax_on')
  syntax reset
endif

set background=light
let g:colors_name = 'spectral-light'

let s:amber = {'gui': '#A35F00', 'cterm': '130'}

call spectral#apply({
  \ 'bg':        {'gui': '#FAF6EC', 'cterm': '230'},
  \ 'bg_alt':    {'gui': '#F1EBD9', 'cterm': '254'},
  \ 'bg_alt2':   {'gui': '#E2D8C0', 'cterm': '187'},
  \ 'fg_dark':   {'gui': '#756648', 'cterm': '102'},
  \ 'fg_darker': {'gui': '#6B5E45', 'cterm': '240'},
  \ 'fg_alt':    {'gui': '#4F4534', 'cterm': '238'},
  \ 'fg_light':  {'gui': '#1F1A12', 'cterm': '234'},
  \ 'fg':        {'gui': '#2A241B', 'cterm': '235'},
  \ 'white':     {'gui': '#FFFFFF', 'cterm': '231'},
  \ 'red':       {'gui': '#C42828', 'cterm': '160'},
  \ 'orange':    {'gui': '#B45418', 'cterm': '166'},
  \ 'yellow':    {'gui': '#7D6700', 'cterm': '100'},
  \ 'green':     {'gui': '#1F6B25', 'cterm': '28'},
  \ 'cyan':      {'gui': '#006978', 'cterm': '23'},
  \ 'purple':    {'gui': '#6A3DAA', 'cterm': '61'},
  \ 'black':     {'gui': '#000000', 'cterm': '16'},
  \ 'tab_bg':    {'gui': '#EBE3CE', 'cterm': '187'},
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

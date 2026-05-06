" ===============================================================
" Spectral Dark
" Amber CRT phosphor on OLED black, with cool accents for balance.
" Maintainer:   iain
" License:      MIT
" GENERATED FILE — edit tools/palette.py and regenerate.
" ===============================================================

hi clear
if exists('syntax_on')
  syntax reset
endif

set background=dark
let g:colors_name = 'spectral-dark'

let s:amber = {'gui': '#F9AD26', 'cterm': '214'}

call spectral#apply({
  \ 'bg':        {'gui': '#1B1810', 'cterm': '233'},
  \ 'bg_alt':    {'gui': '#2A261C', 'cterm': '235'},
  \ 'bg_alt2':   {'gui': '#423C30', 'cterm': '237'},
  \ 'fg_dark':   {'gui': '#5E574A', 'cterm': '240'},
  \ 'fg_darker': {'gui': '#7B7463', 'cterm': '242'},
  \ 'fg_alt':    {'gui': '#A19784', 'cterm': '138'},
  \ 'fg_light':  {'gui': '#F4E6CA', 'cterm': '224'},
  \ 'fg':        {'gui': '#DCD0B5', 'cterm': '187'},
  \ 'white':     {'gui': '#FFFFFF', 'cterm': '231'},
  \ 'red':       {'gui': '#FF544C', 'cterm': '203'},
  \ 'orange':    {'gui': '#FF8432', 'cterm': '209'},
  \ 'yellow':    {'gui': '#F8D700', 'cterm': '220'},
  \ 'green':     {'gui': '#8DEF46', 'cterm': '119'},
  \ 'cyan':      {'gui': '#2AD7D7', 'cterm': '44'},
  \ 'purple':    {'gui': '#CC77DF', 'cterm': '176'},
  \ 'black':     {'gui': '#000000', 'cterm': '16'},
  \ 'tab_bg':    {'gui': '#070502', 'cterm': '232'},
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

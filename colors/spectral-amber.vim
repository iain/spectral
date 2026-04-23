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

let s:amber = {'gui': '#FFB000', 'cterm': '214'}

call spectral#apply({
  \ 'bg':        {'gui': '#181818', 'cterm': '234'},
  \ 'bg_alt':    {'gui': '#262626', 'cterm': '235'},
  \ 'bg_alt2':   {'gui': '#3D3D3D', 'cterm': '237'},
  \ 'fg_dark':   {'gui': '#5C5C5C', 'cterm': '240'},
  \ 'fg_darker': {'gui': '#7A7A7A', 'cterm': '243'},
  \ 'fg_alt':    {'gui': '#9A9A9A', 'cterm': '247'},
  \ 'fg_light':  {'gui': '#FFD180', 'cterm': '222'},
  \ 'fg':        {'gui': '#D8D4CC', 'cterm': '252'},
  \ 'white':     {'gui': '#FFFFFF', 'cterm': '231'},
  \ 'red':       {'gui': '#FF3B30', 'cterm': '203'},
  \ 'orange':    {'gui': '#FF7A1C', 'cterm': '208'},
  \ 'yellow':    {'gui': '#FFD60A', 'cterm': '220'},
  \ 'green':     {'gui': '#B5E853', 'cterm': '149'},
  \ 'cyan':      {'gui': '#30D5C8', 'cterm': '80'},
  \ 'purple':    {'gui': '#C678DD', 'cterm': '176'},
  \ 'black':     {'gui': '#000000', 'cterm': '16'},
  \ 'tab_bg':    {'gui': '#0D0D0D', 'cterm': '232'},
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

" ===============================================================
" Spectral — lightline.vim theme
" Statusline palette matching the editor colorscheme. Branches on
" &background, so `let g:lightline.colorscheme = 'spectral'` tracks
" whichever variant is active.
" Maintainer:   iain
" License:      MIT
" GENERATED FILE — edit tools/palette.py and regenerate.
" ===============================================================

let s:p = {'normal': {}, 'inactive': {}, 'insert': {}, 'replace': {}, 'visual': {}, 'tabline': {}}

if &background ==# 'light'
  let s:bg = ['#FFFAEE', 231]
  let s:amber = ['#9D6300', 130]
  let s:fg_light = ['#171105', 233]
  let s:bg_alt2 = ['#E7D9BD', 187]
  let s:fg_alt = ['#463C28', 58]
  let s:bg_alt = ['#F6EAD1', 224]
  let s:fg_darker = ['#5D5139', 59]
  let s:red = ['#AC1A1C', 124]
  let s:yellow = ['#A98D00', 136]
  let s:fg_dark = ['#6E6249', 59]
  let s:green = ['#357426', 64]
  let s:purple = ['#65389F', 61]
  let s:tab_bg = ['#EFE3CB', 224]
else
  let s:bg = ['#1A1815', 234]
  let s:amber = ['#F9AD26', 214]
  let s:fg_light = ['#F4E6CA', 224]
  let s:bg_alt2 = ['#403D36', 237]
  let s:fg_alt = ['#A19784', 138]
  let s:bg_alt = ['#282622', 235]
  let s:fg_darker = ['#7B7463', 242]
  let s:red = ['#FF544C', 203]
  let s:yellow = ['#F8D700', 220]
  let s:fg_dark = ['#5E574A', 240]
  let s:green = ['#8DEF46', 119]
  let s:purple = ['#CC77DF', 176]
  let s:tab_bg = ['#060604', 232]
endif

let s:p.normal.left = [ [s:bg, s:amber], [s:fg_light, s:bg_alt2] ]
let s:p.normal.right = [ [s:fg_light, s:bg_alt2], [s:fg_alt, s:bg_alt] ]
let s:p.normal.middle = [ [s:fg_darker, s:bg_alt] ]
let s:p.normal.error = [ [s:bg, s:red] ]
let s:p.normal.warning = [ [s:bg, s:yellow] ]
let s:p.inactive.left = [ [s:fg_dark, s:bg_alt], [s:fg_dark, s:bg] ]
let s:p.inactive.right = [ [s:fg_dark, s:bg_alt], [s:fg_dark, s:bg] ]
let s:p.inactive.middle = [ [s:fg_dark, s:bg] ]
let s:p.insert.left = [ [s:bg, s:green], [s:fg_light, s:bg_alt2] ]
let s:p.replace.left = [ [s:bg, s:red], [s:fg_light, s:bg_alt2] ]
let s:p.visual.left = [ [s:bg, s:purple], [s:fg_light, s:bg_alt2] ]
let s:p.tabline.left = [ [s:fg_alt, s:tab_bg] ]
let s:p.tabline.tabsel = [ [s:fg_light, s:bg] ]
let s:p.tabline.middle = [ [s:fg_dark, s:tab_bg] ]
let s:p.tabline.right = [ [s:fg_alt, s:tab_bg] ]

let g:lightline#colorscheme#spectral#palette = lightline#colorscheme#flatten(s:p)

" vim: set sw=2 ts=2 sts=2 et tw=80 ft=vim:

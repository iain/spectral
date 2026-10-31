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
  let s:amber = ['#A76C01', 130]
  let s:fg_strong = ['#171105', 233]
  let s:bg_selected = ['#E7D9BD', 187]
  let s:fg_muted = ['#463C28', 58]
  let s:bg_highlight = ['#F6EAD1', 224]
  let s:fg_subtle = ['#5D5139', 59]
  let s:red = ['#BB0916', 124]
  let s:yellow = ['#AD8600', 136]
  let s:fg_faint = ['#6E6249', 59]
  let s:green = ['#1A7F11', 28]
  let s:purple = ['#791DC7', 92]
  let s:bg_chrome = ['#FFFDFA', 231]
else
  let s:bg = ['#110F0C', 233]
  let s:amber = ['#F9AD26', 214]
  let s:fg_strong = ['#F4E6CA', 224]
  let s:bg_selected = ['#403D36', 237]
  let s:fg_muted = ['#A19784', 138]
  let s:bg_highlight = ['#282622', 235]
  let s:fg_subtle = ['#7B7463', 242]
  let s:red = ['#FF544C', 203]
  let s:yellow = ['#F8D700', 220]
  let s:fg_faint = ['#5E574A', 240]
  let s:green = ['#8DEF46', 119]
  let s:purple = ['#CC77DF', 176]
  let s:bg_chrome = ['#040302', 16]
endif

let s:p.normal.left = [ [s:bg, s:amber], [s:fg_strong, s:bg_selected] ]
let s:p.normal.right = [ [s:fg_strong, s:bg_selected], [s:fg_muted, s:bg_highlight] ]
let s:p.normal.middle = [ [s:fg_subtle, s:bg_highlight] ]
let s:p.normal.error = [ [s:bg, s:red] ]
let s:p.normal.warning = [ [s:bg, s:yellow] ]
let s:p.inactive.left = [ [s:fg_faint, s:bg_highlight], [s:fg_faint, s:bg] ]
let s:p.inactive.right = [ [s:fg_faint, s:bg_highlight], [s:fg_faint, s:bg] ]
let s:p.inactive.middle = [ [s:fg_faint, s:bg] ]
let s:p.insert.left = [ [s:bg, s:green], [s:fg_strong, s:bg_selected] ]
let s:p.replace.left = [ [s:bg, s:red], [s:fg_strong, s:bg_selected] ]
let s:p.visual.left = [ [s:bg, s:purple], [s:fg_strong, s:bg_selected] ]
let s:p.tabline.left = [ [s:fg_muted, s:bg_chrome] ]
let s:p.tabline.tabsel = [ [s:fg_strong, s:bg] ]
let s:p.tabline.middle = [ [s:fg_faint, s:bg_chrome] ]
let s:p.tabline.right = [ [s:fg_muted, s:bg_chrome] ]

let g:lightline#colorscheme#spectral#palette = lightline#colorscheme#flatten(s:p)

" vim: set sw=2 ts=2 sts=2 et tw=80 ft=vim:

" ===============================================================
" Spectral
" Dispatches to spectral-dark or spectral-light based on &background.
" Maintainer:   iain
" License:      MIT
" ===============================================================

if &background ==# 'light'
  runtime colors/spectral-light.vim
else
  runtime colors/spectral-dark.vim
endif

" vim: set sw=2 ts=2 sts=2 et tw=80 ft=vim:

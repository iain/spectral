" Go composite literal keys for Spectral colorscheme
" Go's syntax file has no group for the Name in User{Name: "x"}, so this adds
" one for the colorscheme to give the amber signature.

if exists('g:loaded_spectral_go')
  finish
endif
let g:loaded_spectral_go = 1

function! s:SetupGoSyntax()
  if &filetype !=# 'go'
    return
  endif

  " A key opens a line or follows { or , and is followed by ': value'. That
  " leaves out labels (nothing after the colon), case clauses (preceded by
  " 'case') and slice bounds (preceded by '[').
  syn match goLiteralKey "\%(^\s*\|[{,]\s*\)\@<=\h\w*\ze:\s\+\S"
endfunction

augroup SpectralGo
  autocmd!
  autocmd Syntax go call s:SetupGoSyntax()
augroup END

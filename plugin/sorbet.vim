" Sorbet syntax highlighting plugin for Spectral colorscheme
" This adds syntax patterns for Sorbet type annotations in Ruby

if exists('g:loaded_spectral_sorbet')
  finish
endif
let g:loaded_spectral_sorbet = 1

function! s:SetupSorbetSyntax()
  if &filetype !=# 'ruby'
    return
  endif

  " Match 'extend T::Sig'
  syn match rubySorbetExtend "\<extend\s\+T::Sig\>"

  " Single-line sig blocks: mute the entire sig { ... } line
  syn match rubySorbetSigBlock "^\s*sig\s*{[^}]*}"

  " Multi-line sig blocks: sig do ... end
  " matchgroup ensures delimiters are highlighted as part of the block
  syn region rubySorbetSigBlock matchgroup=rubySorbetSigBlock start="^\s*sig\s\+do\s*$" end="^\s*end\s*$"

  " Sorbet type annotations outside sig blocks (T::, T.)
  syn match rubySorbetTypes "\<T::\w\+"
  syn match rubySorbetTypes "\<T\.\w\+"
endfunction

augroup SpectralSorbet
  autocmd!
  autocmd FileType ruby call s:SetupSorbetSyntax()
  autocmd Syntax ruby call s:SetupSorbetSyntax()
augroup END

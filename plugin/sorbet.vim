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

  " Match 'sig' keyword (both with blocks and do..end)
  syn match rubySorbetSig "\<sig\>\s*{"me=e-1
  syn match rubySorbetSig "\<sig\>\s*do"me=e-2

  " Match sig blocks
  syn region rubySorbetSigBlock start="\<sig\>\s*{" end="}" contains=rubySorbetKeywords,rubySorbetTypes,rubySymbol,rubyString,rubyConstant,rubyBoolean,rubyInteger,rubyFloat,rubyInterpolation
  syn region rubySorbetSigBlock start="\<sig\>\s*do" end="\<end\>" contains=rubySorbetKeywords,rubySorbetTypes,rubySymbol,rubyString,rubyConstant,rubyBoolean,rubyInteger,rubyFloat,rubyInterpolation

  " Sorbet method keywords
  syn keyword rubySorbetKeywords params returns void abstract override type_parameters contained

  " Sorbet type annotations (T::, T.)
  syn match rubySorbetTypes "\<T::\w\+"
  syn match rubySorbetTypes "\<T\.\w\+"

  " Additional Sorbet-specific patterns
  syn match rubySorbetTypes "\<T\.nilable"
  syn match rubySorbetTypes "\<T\.any"
  syn match rubySorbetTypes "\<T\.all"
  syn match rubySorbetTypes "\<T\.untyped"
  syn match rubySorbetTypes "\<T\.noreturn"
  syn match rubySorbetTypes "\<T\.self_type"
  syn match rubySorbetTypes "\<T\.attached_class"
  syn match rubySorbetTypes "\<T\.class_of"
  syn match rubySorbetTypes "\<T\.enum"
endfunction

augroup SpectralSorbet
  autocmd!
  autocmd FileType ruby call s:SetupSorbetSyntax()
  autocmd Syntax ruby call s:SetupSorbetSyntax()
augroup END

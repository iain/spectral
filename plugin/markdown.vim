" Markdown H1 delimiter for Spectral colorscheme
" vim-polyglot draws the # of every heading with one group, mkdHeading, so the
" # of an H1 could not join the amber field behind its text. This redefines
" the H1 region with a delimiter group of its own.

if exists('g:loaded_spectral_markdown')
  finish
endif
let g:loaded_spectral_markdown = 1

function! s:SetupMarkdownSyntax()
  if get(b:, 'current_syntax', '') !=# 'mkd'
    return
  endif

  " Defined last, this region wins over polyglot's own H1 and, at the same
  " position, over H2-H6 too, so it must not match a second #.
  syn region htmlH1 matchgroup=spectralMkdH1Delimiter start="^\s*##\@!" end="$" contains=mkdLink,mkdInlineURL,@Spell
endfunction

augroup SpectralMarkdown
  autocmd!
  autocmd Syntax markdown call s:SetupMarkdownSyntax()
augroup END

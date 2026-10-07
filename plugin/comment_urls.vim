" URLs in comments for Spectral colorscheme
" Syntax files leave a URL in a comment as plain comment text; this marks it
" so the colorscheme can show it as a link, in every language.

if exists('g:loaded_spectral_comment_urls')
  finish
endif
let g:loaded_spectral_comment_urls = 1

function! s:SetupCommentUrlSyntax()
  " The URL stops before punctuation that usually closes the sentence or the
  " parentheses around it rather than belonging to the address.
  syn match spectralCommentUrl "\vhttps?://\S*[^[:space:].,;:!?'\")\]}>]"
        \ contained containedin=.*Comment
endfunction

augroup SpectralCommentUrls
  autocmd!
  autocmd Syntax * call s:SetupCommentUrlSyntax()
augroup END

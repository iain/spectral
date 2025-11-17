" ===============================================================
" Spectral
" A Vim colorscheme based on Monokai Pro Spectrum
" Maintainer:   iain
" License:      MIT
" ===============================================================

" Setup {{{
" ===============================================================

" Reset highlighting
hi clear
if exists('syntax_on')
  syntax reset
endif

set background=dark
let g:colors_name = 'spectral'

" Check for 24-bit color support
if has('termguicolors')
  set termguicolors
  if has('nvim')
    let $NVIM_TUI_ENABLE_TRUE_COLOR = 1
  endif
endif

" }}}
" Color Palette {{{
" ===============================================================

" Background & Foreground
let s:bg         = {'gui': '#222222', 'cterm': '234'}
let s:bg_alt     = {'gui': '#363537', 'cterm': '236'}
let s:bg_alt2    = {'gui': '#525053', 'cterm': '239'}
let s:fg_dark    = {'gui': '#69676c', 'cterm': '242'}
let s:fg_darker  = {'gui': '#8b888f', 'cterm': '245'}
let s:fg_alt     = {'gui': '#bab6bf', 'cterm': '250'}
let s:fg_light   = {'gui': '#f7f1ff', 'cterm': '255'}
let s:fg         = {'gui': '#fbf8ff', 'cterm': '231'}

" Accent Colors
let s:white      = {'gui': '#ffffff', 'cterm': '231'}
let s:red        = {'gui': '#fc618d', 'cterm': '204'}
let s:orange     = {'gui': '#fd9353', 'cterm': '209'}
let s:yellow     = {'gui': '#fce566', 'cterm': '227'}
let s:green      = {'gui': '#7bd88f', 'cterm': '114'}
let s:cyan       = {'gui': '#5ad4e6', 'cterm': '81'}
let s:purple     = {'gui': '#948ae3', 'cterm': '141'}

" Special
let s:none       = {'gui': 'NONE', 'cterm': 'NONE'}

" }}}
" Highlighting Function {{{
" ===============================================================

function! s:HL(group, fg, bg, attr)
  let l:cmd = 'highlight ' . a:group

  if a:fg != s:none
    let l:cmd .= ' guifg=' . a:fg.gui . ' ctermfg=' . a:fg.cterm
  else
    let l:cmd .= ' guifg=NONE ctermfg=NONE'
  endif

  if a:bg != s:none
    let l:cmd .= ' guibg=' . a:bg.gui . ' ctermbg=' . a:bg.cterm
  else
    let l:cmd .= ' guibg=NONE ctermbg=NONE'
  endif

  if a:attr != ''
    let l:cmd .= ' gui=' . a:attr . ' cterm=' . a:attr
  else
    let l:cmd .= ' gui=NONE cterm=NONE'
  endif

  execute l:cmd
endfunction

" }}}
" Editor UI {{{
" ===============================================================

call s:HL('Normal',          s:fg,         s:bg,         '')
call s:HL('NormalFloat',     s:fg,         s:bg_alt,     '')
call s:HL('NormalNC',        s:fg_alt,     s:bg,         '')

" Cursor
call s:HL('Cursor',          s:bg,         s:fg,         '')
call s:HL('CursorLine',      s:none,       s:bg_alt,     'NONE')
call s:HL('CursorLineNr',    s:fg_light,   s:bg_alt,     'bold')
call s:HL('CursorColumn',    s:none,       s:bg_alt,     '')

" Line Numbers
call s:HL('LineNr',          s:fg_dark,    s:bg,         '')
call s:HL('SignColumn',      s:fg_dark,    s:bg,         '')
call s:HL('FoldColumn',      s:fg_darker,  s:bg,         '')

" Statusline
call s:HL('StatusLine',      s:fg,         s:bg_alt2,    'NONE')
call s:HL('StatusLineNC',    s:fg_darker,  s:bg_alt,     'NONE')
call s:HL('StatusLineTerm',  s:fg,         s:bg_alt2,    'NONE')
call s:HL('StatusLineTermNC',s:fg_darker,  s:bg_alt,     'NONE')

" Tabline
call s:HL('TabLine',         s:fg_alt,     s:bg_alt,     'NONE')
call s:HL('TabLineFill',     s:fg_dark,    s:bg_alt,     'NONE')
call s:HL('TabLineSel',      s:fg_light,   s:bg_alt2,    'bold')

" Vertical Split
call s:HL('VertSplit',       s:bg_alt2,    s:bg,         'NONE')

" Visual Selection
call s:HL('Visual',          s:none,       s:bg_alt2,    '')
call s:HL('VisualNOS',       s:none,       s:bg_alt2,    '')

" Search
call s:HL('Search',          s:bg,         s:yellow,     '')
call s:HL('IncSearch',       s:bg,         s:orange,     '')
call s:HL('Substitute',      s:bg,         s:orange,     '')

" Messages
call s:HL('ErrorMsg',        s:red,        s:bg,         'bold')
call s:HL('WarningMsg',      s:orange,     s:bg,         'bold')
call s:HL('ModeMsg',         s:fg,         s:bg,         'bold')
call s:HL('MoreMsg',         s:green,      s:bg,         'bold')
call s:HL('Question',        s:cyan,       s:bg,         'bold')

" Menu/Popup
call s:HL('Pmenu',           s:fg,         s:bg_alt,     '')
call s:HL('PmenuSel',        s:bg,         s:cyan,       'bold')
call s:HL('PmenuSbar',       s:none,       s:bg_alt2,    '')
call s:HL('PmenuThumb',      s:none,       s:fg_darker,  '')

" Diff
call s:HL('DiffAdd',         s:green,      s:bg_alt,     '')
call s:HL('DiffChange',      s:yellow,     s:bg_alt,     '')
call s:HL('DiffDelete',      s:red,        s:bg_alt,     '')
call s:HL('DiffText',        s:cyan,       s:bg_alt2,    'bold')

" Spelling
call s:HL('SpellBad',        s:red,        s:none,       'underline')
call s:HL('SpellCap',        s:yellow,     s:none,       'underline')
call s:HL('SpellLocal',      s:orange,     s:none,       'underline')
call s:HL('SpellRare',       s:cyan,       s:none,       'underline')

" Misc
call s:HL('ColorColumn',     s:none,       s:bg_alt,     '')
call s:HL('Conceal',         s:fg_dark,    s:none,       '')
call s:HL('Directory',       s:cyan,       s:none,       'bold')
call s:HL('Folded',          s:fg_darker,  s:bg_alt,     '')
call s:HL('MatchParen',      s:yellow,     s:bg_alt2,    'bold')
call s:HL('NonText',         s:fg_dark,    s:none,       '')
call s:HL('SpecialKey',      s:fg_dark,    s:none,       '')
call s:HL('Title',           s:purple,     s:none,       'bold')
call s:HL('WildMenu',        s:bg,         s:cyan,       'bold')

" }}}
" Syntax Highlighting {{{
" ===============================================================

" General
call s:HL('Comment',         s:fg_dark,    s:none,       'italic')
call s:HL('Constant',        s:purple,     s:none,       '')
call s:HL('String',          s:yellow,     s:none,       '')
call s:HL('Character',       s:yellow,     s:none,       '')
call s:HL('Number',          s:purple,     s:none,       '')
call s:HL('Boolean',         s:purple,     s:none,       '')
call s:HL('Float',           s:purple,     s:none,       '')

call s:HL('Identifier',      s:fg,         s:none,       '')
call s:HL('Function',        s:green,      s:none,       '')

call s:HL('Statement',       s:red,        s:none,       '')
call s:HL('Conditional',     s:red,        s:none,       '')
call s:HL('Repeat',          s:red,        s:none,       '')
call s:HL('Label',           s:red,        s:none,       '')
call s:HL('Operator',        s:red,        s:none,       '')
call s:HL('Keyword',         s:red,        s:none,       '')
call s:HL('Exception',       s:red,        s:none,       '')

call s:HL('PreProc',         s:red,        s:none,       '')
call s:HL('Include',         s:red,        s:none,       '')
call s:HL('Define',          s:red,        s:none,       '')
call s:HL('Macro',           s:cyan,       s:none,       '')
call s:HL('PreCondit',       s:red,        s:none,       '')

call s:HL('Type',            s:cyan,       s:none,       '')
call s:HL('StorageClass',    s:red,        s:none,       '')
call s:HL('Structure',       s:cyan,       s:none,       '')
call s:HL('Typedef',         s:cyan,       s:none,       '')

call s:HL('Special',         s:cyan,       s:none,       '')
call s:HL('SpecialChar',     s:orange,     s:none,       '')
call s:HL('Tag',             s:red,        s:none,       '')
call s:HL('Delimiter',       s:fg,         s:none,       '')
call s:HL('SpecialComment',  s:fg_darker,  s:none,       'italic')
call s:HL('Debug',           s:orange,     s:none,       '')

call s:HL('Underlined',      s:cyan,       s:none,       'underline')
call s:HL('Ignore',          s:fg_dark,    s:none,       '')
call s:HL('Error',           s:red,        s:bg,         'bold')
call s:HL('Todo',            s:orange,     s:bg,         'bold')

" }}}
" Language-Specific {{{
" ===============================================================

" HTML
call s:HL('htmlTag',         s:fg_alt,     s:none,       '')
call s:HL('htmlEndTag',      s:fg_alt,     s:none,       '')
call s:HL('htmlTagName',     s:red,        s:none,       '')
call s:HL('htmlArg',         s:green,      s:none,       '')
call s:HL('htmlSpecialChar', s:purple,     s:none,       '')
call s:HL('htmlTitle',       s:fg,         s:none,       '')
call s:HL('htmlH1',          s:fg,         s:none,       'bold')

" XML
call s:HL('xmlTag',          s:red,        s:none,       '')
call s:HL('xmlEndTag',       s:red,        s:none,       '')
call s:HL('xmlTagName',      s:red,        s:none,       '')
call s:HL('xmlAttrib',       s:green,      s:none,       '')

" CSS
call s:HL('cssBraces',       s:fg,         s:none,       '')
call s:HL('cssClassName',    s:cyan,       s:none,       '')
call s:HL('cssClassNameDot', s:cyan,       s:none,       '')
call s:HL('cssProp',         s:fg,         s:none,       '')
call s:HL('cssAttr',         s:purple,     s:none,       '')
call s:HL('cssColor',        s:purple,     s:none,       '')
call s:HL('cssValueLength',  s:purple,     s:none,       '')
call s:HL('cssValueNumber',  s:purple,     s:none,       '')
call s:HL('cssImportant',    s:red,        s:none,       'bold')

" JavaScript
call s:HL('javaScriptBraces',     s:fg,    s:none,       '')
call s:HL('javaScriptFunction',   s:red,   s:none,       '')
call s:HL('javaScriptIdentifier', s:red,   s:none,       '')
call s:HL('javaScriptNull',       s:purple,s:none,       '')
call s:HL('javaScriptNumber',     s:purple,s:none,       '')
call s:HL('javaScriptRequire',    s:cyan,  s:none,       '')
call s:HL('javaScriptReserved',   s:red,   s:none,       '')

" TypeScript
call s:HL('typescriptBraces',           s:fg,    s:none,  '')
call s:HL('typescriptImport',           s:red,   s:none,  '')
call s:HL('typescriptExport',           s:red,   s:none,  '')
call s:HL('typescriptIdentifier',       s:cyan,  s:none,  '')
call s:HL('typescriptVariable',         s:red,   s:none,  '')
call s:HL('typescriptType',             s:cyan,  s:none,  '')
call s:HL('typescriptArrowFunc',        s:red,   s:none,  '')

" Python
call s:HL('pythonBuiltin',       s:cyan,   s:none,       '')
call s:HL('pythonBuiltinObj',    s:cyan,   s:none,       '')
call s:HL('pythonBuiltinFunc',   s:green,  s:none,       '')
call s:HL('pythonFunction',      s:green,  s:none,       '')
call s:HL('pythonDecorator',     s:orange, s:none,       '')
call s:HL('pythonInclude',       s:red,    s:none,       '')
call s:HL('pythonImport',        s:red,    s:none,       '')
call s:HL('pythonRun',           s:cyan,   s:none,       '')
call s:HL('pythonCoding',        s:fg_dark,s:none,       '')
call s:HL('pythonOperator',      s:red,    s:none,       '')
call s:HL('pythonException',     s:red,    s:none,       '')
call s:HL('pythonExceptions',    s:cyan,   s:none,       '')
call s:HL('pythonBoolean',       s:purple, s:none,       '')
call s:HL('pythonDot',           s:fg_alt, s:none,       '')
call s:HL('pythonConditional',   s:red,    s:none,       '')
call s:HL('pythonRepeat',        s:red,    s:none,       '')
call s:HL('pythonDottedName',    s:green,  s:none,       '')

" Ruby
call s:HL('rubyBlockParameter',        s:orange, s:none, '')
call s:HL('rubyBlockParameterList',    s:orange, s:none, '')
call s:HL('rubyClass',                 s:red,    s:none, '')
call s:HL('rubyConstant',              s:cyan,   s:none, '')
call s:HL('rubyControl',               s:red,    s:none, '')
call s:HL('rubyEscape',                s:orange, s:none, '')
call s:HL('rubyFunction',              s:green,  s:none, '')
call s:HL('rubyGlobalVariable',        s:orange, s:none, '')
call s:HL('rubyInclude',               s:red,    s:none, '')
call s:HL('rubyInstanceVariable',      s:orange, s:none, '')
call s:HL('rubyInterpolation',         s:cyan,   s:none, '')
call s:HL('rubyInterpolationDelimiter',s:orange, s:none, '')
call s:HL('rubyRegexp',                s:cyan,   s:none, '')
call s:HL('rubyRegexpDelimiter',       s:cyan,   s:none, '')
call s:HL('rubyStringDelimiter',       s:yellow, s:none, '')
call s:HL('rubySymbol',                s:purple, s:none, '')

" Go
call s:HL('goDeclaration',       s:red,    s:none,       '')
call s:HL('goBuiltins',          s:cyan,   s:none,       '')
call s:HL('goFunctionCall',      s:green,  s:none,       '')
call s:HL('goVarArgs',           s:orange, s:none,       '')
call s:HL('goVarDefs',           s:orange, s:none,       '')
call s:HL('goConstants',         s:purple, s:none,       '')

" Markdown
call s:HL('markdownH1',                s:red,    s:none,  'bold')
call s:HL('markdownH2',                s:orange, s:none,  'bold')
call s:HL('markdownH3',                s:yellow, s:none,  'bold')
call s:HL('markdownH4',                s:green,  s:none,  'bold')
call s:HL('markdownH5',                s:cyan,   s:none,  'bold')
call s:HL('markdownH6',                s:purple, s:none,  'bold')
call s:HL('markdownHeadingDelimiter',  s:red,    s:none,  'bold')
call s:HL('markdownHeadingRule',       s:fg_dark,s:none,  '')
call s:HL('markdownBold',              s:orange, s:none,  'bold')
call s:HL('markdownItalic',            s:purple, s:none,  'italic')
call s:HL('markdownBoldItalic',        s:orange, s:none,  'bold,italic')
call s:HL('markdownCode',              s:green,  s:none,  '')
call s:HL('markdownCodeBlock',         s:green,  s:none,  '')
call s:HL('markdownCodeDelimiter',     s:green,  s:none,  '')
call s:HL('markdownUrl',               s:cyan,   s:none,  'underline')
call s:HL('markdownLinkText',          s:purple, s:none,  '')
call s:HL('markdownLinkDelimiter',     s:fg_alt, s:none,  '')
call s:HL('markdownLinkTextDelimiter', s:fg_alt, s:none,  '')
call s:HL('markdownListMarker',        s:red,    s:none,  '')
call s:HL('markdownOrderedListMarker', s:red,    s:none,  '')

" JSON
call s:HL('jsonKeyword',         s:cyan,   s:none,       '')
call s:HL('jsonQuote',           s:fg_alt, s:none,       '')
call s:HL('jsonBraces',          s:fg,     s:none,       '')
call s:HL('jsonString',          s:yellow, s:none,       '')

" YAML
call s:HL('yamlKey',             s:cyan,   s:none,       '')
call s:HL('yamlConstant',        s:purple, s:none,       '')
call s:HL('yamlBlockMappingKey', s:cyan,   s:none,       '')

" TOML
call s:HL('tomlTable',           s:purple, s:none,       'bold')
call s:HL('tomlKey',             s:cyan,   s:none,       '')

" Vim
call s:HL('vimCommand',          s:red,    s:none,       '')
call s:HL('vimLet',              s:red,    s:none,       '')
call s:HL('vimFunction',         s:green,  s:none,       '')
call s:HL('vimIsCommand',        s:fg,     s:none,       '')
call s:HL('vimUserFunc',         s:green,  s:none,       '')
call s:HL('vimFuncName',         s:green,  s:none,       '')

" }}}
" Plugin Support {{{
" ===============================================================

" GitGutter
call s:HL('GitGutterAdd',        s:green,  s:bg,         '')
call s:HL('GitGutterChange',     s:yellow, s:bg,         '')
call s:HL('GitGutterDelete',     s:red,    s:bg,         '')
call s:HL('GitGutterChangeDelete', s:orange, s:bg,       '')

" Signify
call s:HL('SignifySignAdd',      s:green,  s:bg,         '')
call s:HL('SignifySignChange',   s:yellow, s:bg,         '')
call s:HL('SignifySignDelete',   s:red,    s:bg,         '')

" fugitive
call s:HL('diffAdded',           s:green,  s:none,       '')
call s:HL('diffRemoved',         s:red,    s:none,       '')
call s:HL('diffChanged',         s:yellow, s:none,       '')
call s:HL('diffLine',            s:cyan,   s:none,       '')
call s:HL('diffFile',            s:orange, s:none,       '')
call s:HL('diffNewFile',         s:green,  s:none,       '')

" NERDTree
call s:HL('NERDTreeDir',         s:cyan,   s:none,       'bold')
call s:HL('NERDTreeDirSlash',    s:cyan,   s:none,       '')
call s:HL('NERDTreeFile',        s:fg,     s:none,       '')
call s:HL('NERDTreeExecFile',    s:green,  s:none,       '')
call s:HL('NERDTreeOpenable',    s:fg_alt, s:none,       '')
call s:HL('NERDTreeClosable',    s:fg_alt, s:none,       '')
call s:HL('NERDTreeCWD',         s:purple, s:none,       'bold')
call s:HL('NERDTreeUp',          s:fg_darker, s:none,    '')
call s:HL('NERDTreeFlags',       s:purple, s:none,       '')

" ALE (Asynchronous Lint Engine)
call s:HL('ALEError',            s:red,    s:none,       'underline')
call s:HL('ALEWarning',          s:yellow, s:none,       'underline')
call s:HL('ALEInfo',             s:cyan,   s:none,       'underline')
call s:HL('ALEErrorSign',        s:red,    s:bg,         'bold')
call s:HL('ALEWarningSign',      s:yellow, s:bg,         'bold')
call s:HL('ALEInfoSign',         s:cyan,   s:bg,         'bold')

" CoC (Conquer of Completion)
call s:HL('CocErrorSign',        s:red,    s:bg,         'bold')
call s:HL('CocWarningSign',      s:yellow, s:bg,         'bold')
call s:HL('CocInfoSign',         s:cyan,   s:bg,         'bold')
call s:HL('CocHintSign',         s:purple, s:bg,         'bold')
call s:HL('CocErrorFloat',       s:red,    s:bg_alt,     '')
call s:HL('CocWarningFloat',     s:yellow, s:bg_alt,     '')
call s:HL('CocInfoFloat',        s:cyan,   s:bg_alt,     '')
call s:HL('CocHintFloat',        s:purple, s:bg_alt,     '')

" CtrlP
call s:HL('CtrlPMatch',          s:cyan,   s:none,       'bold')
call s:HL('CtrlPNoEntries',      s:red,    s:none,       '')
call s:HL('CtrlPPrtBase',        s:fg_dark,s:none,       '')
call s:HL('CtrlPPrtCursor',      s:cyan,   s:none,       '')
call s:HL('CtrlPLinePre',        s:fg_dark,s:none,       '')
call s:HL('CtrlPMode1',          s:fg,     s:bg_alt,     'bold')
call s:HL('CtrlPMode2',          s:fg,     s:bg_alt2,    'bold')

" fzf
call s:HL('fzf1',                s:cyan,   s:bg_alt,     '')
call s:HL('fzf2',                s:cyan,   s:bg_alt,     '')
call s:HL('fzf3',                s:cyan,   s:bg_alt,     '')

" Startify
call s:HL('StartifyBracket',     s:fg_alt, s:none,       '')
call s:HL('StartifyFile',        s:cyan,   s:none,       '')
call s:HL('StartifyFooter',      s:fg_dark,s:none,       '')
call s:HL('StartifyHeader',      s:purple, s:none,       '')
call s:HL('StartifyNumber',      s:orange, s:none,       '')
call s:HL('StartifyPath',        s:fg_alt, s:none,       '')
call s:HL('StartifySection',     s:red,    s:none,       'bold')
call s:HL('StartifySelect',      s:green,  s:none,       '')
call s:HL('StartifySlash',       s:fg_alt, s:none,       '')
call s:HL('StartifySpecial',     s:fg_dark,s:none,       '')

" vim-which-key
call s:HL('WhichKey',            s:cyan,   s:none,       'bold')
call s:HL('WhichKeySeperator',   s:fg_darker, s:none,    '')
call s:HL('WhichKeyGroup',       s:purple, s:none,       'bold')
call s:HL('WhichKeyDesc',        s:fg,     s:none,       '')

" Telescope
call s:HL('TelescopeBorder',     s:fg_alt, s:bg,         '')
call s:HL('TelescopePromptBorder', s:cyan, s:bg,         '')
call s:HL('TelescopeResultsBorder', s:fg_alt, s:bg,      '')
call s:HL('TelescopePreviewBorder', s:fg_alt, s:bg,      '')
call s:HL('TelescopeSelection',  s:fg,     s:bg_alt,     'bold')
call s:HL('TelescopeSelectionCaret', s:cyan, s:bg_alt,   'bold')
call s:HL('TelescopeMultiSelection', s:purple, s:bg_alt, '')
call s:HL('TelescopeMatching',   s:cyan,   s:none,       'bold')

" }}}
" Terminal Colors {{{
" ===============================================================

if has('nvim')
  let g:terminal_color_0  = s:bg.gui
  let g:terminal_color_1  = s:red.gui
  let g:terminal_color_2  = s:green.gui
  let g:terminal_color_3  = s:yellow.gui
  let g:terminal_color_4  = s:cyan.gui
  let g:terminal_color_5  = s:purple.gui
  let g:terminal_color_6  = s:cyan.gui
  let g:terminal_color_7  = s:fg.gui
  let g:terminal_color_8  = s:fg_dark.gui
  let g:terminal_color_9  = s:red.gui
  let g:terminal_color_10 = s:green.gui
  let g:terminal_color_11 = s:yellow.gui
  let g:terminal_color_12 = s:cyan.gui
  let g:terminal_color_13 = s:purple.gui
  let g:terminal_color_14 = s:cyan.gui
  let g:terminal_color_15 = s:white.gui
elseif has('terminal')
  let g:terminal_ansi_colors = [
    \ s:bg.gui,
    \ s:red.gui,
    \ s:green.gui,
    \ s:yellow.gui,
    \ s:cyan.gui,
    \ s:purple.gui,
    \ s:cyan.gui,
    \ s:fg.gui,
    \ s:fg_dark.gui,
    \ s:red.gui,
    \ s:green.gui,
    \ s:yellow.gui,
    \ s:cyan.gui,
    \ s:purple.gui,
    \ s:cyan.gui,
    \ s:white.gui
    \ ]
endif

" }}}
" Additional Treesitter Support (for Neovim) {{{
" ===============================================================

" Treesitter highlighting groups
if has('nvim-0.8')
  call s:HL('@comment',            s:fg_dark,    s:none, 'italic')
  call s:HL('@error',              s:red,        s:none, '')
  call s:HL('@none',               s:none,       s:none, '')
  call s:HL('@preproc',            s:red,        s:none, '')
  call s:HL('@define',             s:red,        s:none, '')
  call s:HL('@operator',           s:red,        s:none, '')

  " Punctuation
  call s:HL('@punctuation.delimiter', s:fg_alt,  s:none, '')
  call s:HL('@punctuation.bracket',   s:fg_alt,  s:none, '')
  call s:HL('@punctuation.special',   s:orange,  s:none, '')

  " Literals
  call s:HL('@string',             s:yellow,     s:none, '')
  call s:HL('@string.regex',       s:orange,     s:none, '')
  call s:HL('@string.escape',      s:orange,     s:none, '')
  call s:HL('@string.special',     s:orange,     s:none, '')
  call s:HL('@character',          s:yellow,     s:none, '')
  call s:HL('@character.special',  s:orange,     s:none, '')
  call s:HL('@boolean',            s:purple,     s:none, '')
  call s:HL('@number',             s:purple,     s:none, '')
  call s:HL('@float',              s:purple,     s:none, '')

  " Functions
  call s:HL('@function',           s:green,      s:none, '')
  call s:HL('@function.call',      s:green,      s:none, '')
  call s:HL('@function.builtin',   s:cyan,       s:none, '')
  call s:HL('@function.macro',     s:cyan,       s:none, '')
  call s:HL('@method',             s:green,      s:none, '')
  call s:HL('@method.call',        s:green,      s:none, '')
  call s:HL('@constructor',        s:cyan,       s:none, '')
  call s:HL('@parameter',          s:orange,     s:none, '')

  " Keywords
  call s:HL('@keyword',            s:red,        s:none, '')
  call s:HL('@keyword.function',   s:red,        s:none, '')
  call s:HL('@keyword.operator',   s:red,        s:none, '')
  call s:HL('@keyword.return',     s:red,        s:none, '')
  call s:HL('@conditional',        s:red,        s:none, '')
  call s:HL('@repeat',             s:red,        s:none, '')
  call s:HL('@debug',              s:orange,     s:none, '')
  call s:HL('@label',              s:red,        s:none, '')
  call s:HL('@include',            s:red,        s:none, '')
  call s:HL('@exception',          s:red,        s:none, '')

  " Types
  call s:HL('@type',               s:cyan,       s:none, '')
  call s:HL('@type.builtin',       s:cyan,       s:none, '')
  call s:HL('@type.definition',    s:cyan,       s:none, '')
  call s:HL('@type.qualifier',     s:red,        s:none, '')
  call s:HL('@storageclass',       s:red,        s:none, '')
  call s:HL('@attribute',          s:purple,     s:none, '')
  call s:HL('@field',              s:fg,         s:none, '')
  call s:HL('@property',           s:fg,         s:none, '')

  " Identifiers
  call s:HL('@variable',           s:fg,         s:none, '')
  call s:HL('@variable.builtin',   s:orange,     s:none, '')
  call s:HL('@constant',           s:purple,     s:none, '')
  call s:HL('@constant.builtin',   s:purple,     s:none, '')
  call s:HL('@constant.macro',     s:purple,     s:none, '')
  call s:HL('@namespace',          s:cyan,       s:none, '')
  call s:HL('@symbol',             s:purple,     s:none, '')

  " Text
  call s:HL('@text',               s:fg,         s:none, '')
  call s:HL('@text.strong',        s:orange,     s:none, 'bold')
  call s:HL('@text.emphasis',      s:purple,     s:none, 'italic')
  call s:HL('@text.underline',     s:fg,         s:none, 'underline')
  call s:HL('@text.strike',        s:fg_dark,    s:none, 'strikethrough')
  call s:HL('@text.title',         s:red,        s:none, 'bold')
  call s:HL('@text.literal',       s:green,      s:none, '')
  call s:HL('@text.uri',           s:cyan,       s:none, 'underline')
  call s:HL('@text.math',          s:purple,     s:none, '')
  call s:HL('@text.reference',     s:purple,     s:none, '')
  call s:HL('@text.environment',   s:purple,     s:none, '')
  call s:HL('@text.environment.name', s:cyan,    s:none, '')
  call s:HL('@text.note',          s:fg_dark,    s:none, 'italic')
  call s:HL('@text.warning',       s:orange,     s:none, 'bold')
  call s:HL('@text.danger',        s:red,        s:none, 'bold')

  " Tags
  call s:HL('@tag',                s:red,        s:none, '')
  call s:HL('@tag.attribute',      s:green,      s:none, '')
  call s:HL('@tag.delimiter',      s:fg_alt,     s:none, '')
endif

" }}}
" LSP Support {{{
" ===============================================================

if has('nvim-0.5')
  " LSP Diagnostic
  call s:HL('DiagnosticError',     s:red,        s:none, '')
  call s:HL('DiagnosticWarn',      s:yellow,     s:none, '')
  call s:HL('DiagnosticInfo',      s:cyan,       s:none, '')
  call s:HL('DiagnosticHint',      s:purple,     s:none, '')

  call s:HL('DiagnosticSignError', s:red,        s:bg,   'bold')
  call s:HL('DiagnosticSignWarn',  s:yellow,     s:bg,   'bold')
  call s:HL('DiagnosticSignInfo',  s:cyan,       s:bg,   'bold')
  call s:HL('DiagnosticSignHint',  s:purple,     s:bg,   'bold')

  call s:HL('DiagnosticUnderlineError', s:none,  s:none, 'underline')
  call s:HL('DiagnosticUnderlineWarn',  s:none,  s:none, 'underline')
  call s:HL('DiagnosticUnderlineInfo',  s:none,  s:none, 'underline')
  call s:HL('DiagnosticUnderlineHint',  s:none,  s:none, 'underline')

  call s:HL('DiagnosticVirtualTextError', s:red,    s:none, '')
  call s:HL('DiagnosticVirtualTextWarn',  s:yellow, s:none, '')
  call s:HL('DiagnosticVirtualTextInfo',  s:cyan,   s:none, '')
  call s:HL('DiagnosticVirtualTextHint',  s:purple, s:none, '')

  " LSP References
  call s:HL('LspReferenceText',    s:none,       s:bg_alt2, '')
  call s:HL('LspReferenceRead',    s:none,       s:bg_alt2, '')
  call s:HL('LspReferenceWrite',   s:none,       s:bg_alt2, '')

  " LSP Code Lens
  call s:HL('LspCodeLens',         s:fg_dark,    s:none, 'italic')
  call s:HL('LspCodeLensSeparator',s:fg_dark,    s:none, 'italic')
endif

" }}}

" vim: set sw=2 ts=2 sts=2 et tw=80 ft=vim fdm=marker:

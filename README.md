# Spectral

A Vim/Neovim colorscheme based on Monokai Pro. Available in dark and light variants with true color (24-bit) and 256-color terminal support.

## Variants

- **Spectral** (dark) - Based on Monokai Pro Spectrum
- **Spectral Light** - Based on Monokai Pro Light

## Installation

### vim-plug

```vim
Plug 'iain/spectral'
```

### Pathogen

```bash
cd ~/.vim/bundle
git clone https://github.com/iain/spectral.git
```

### Manual

Copy the files from `colors/` to `~/.vim/colors/` (Vim) or `~/.config/nvim/colors/` (Neovim).

## Usage

Add to your `.vimrc` or `init.vim`:

```vim
set termguicolors
colorscheme spectral
" or
colorscheme spectral-light
```

## Features

### Language Support

Syntax highlighting for:

- Ruby (including Sorbet type annotations)
- Python
- JavaScript / TypeScript
- Go
- HTML / CSS
- Markdown (per-level heading colors, formatting, links, code blocks)
- JSON / YAML / TOML
- XML
- Vim script

### Plugin Support

- GitGutter / Signify
- fugitive
- NERDTree
- netrw
- ALE
- CoC
- fzf / CtrlP
- Telescope
- Startify
- vim-which-key

### Neovim Support

- Treesitter highlighting (Neovim 0.8+)
- LSP diagnostics, references, code lens, inlay hints, and signature help (Neovim 0.5+)
- LSP semantic tokens (Neovim 0.9+)
- Floating windows, WinBar, WinSeparator

### Ruby Sorbet

Sorbet type annotations (`sig` blocks, `T::` types, `extend T::Sig`) are rendered in a muted color to visually separate type signatures from application code. This is handled by `plugin/sorbet.vim` which loads automatically for Ruby files.

## Color Palette

### Dark Variant

| Color  | Hex       | Usage                              |
|--------|-----------|------------------------------------|
| Red    | `#fc618d` | Keywords, control flow             |
| Orange | `#fd9353` | Parameters, special characters     |
| Yellow | `#fce566` | Strings                            |
| Green  | `#7bd88f` | Functions, methods                 |
| Cyan   | `#5ad4e6` | Types, built-in functions          |
| Purple | `#948ae3` | Constants, numbers, booleans       |

Background: `#181818` / Foreground: `#fbf8ff`

### Light Variant

| Color  | Hex       | Usage                              |
|--------|-----------|------------------------------------|
| Red    | `#c33c67` | Keywords, control flow             |
| Orange | `#c36a2d` | Parameters, special characters     |
| Yellow | `#8c8a00` | Strings                            |
| Green  | `#259338` | Functions, methods                 |
| Cyan   | `#0089a1` | Types, built-in functions          |
| Purple | `#6251b3` | Constants, numbers, booleans       |

Background: `#fafafa` / Foreground: `#373431`

## Requirements

- Vim 7.4+ or Neovim 0.5+
- True color terminal support (recommended)

## Credits

Based on [Monokai Pro](https://monokai.pro/) by Monokai.

## License

MIT

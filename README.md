# Spectral

A warm, high-contrast colorscheme for Vim and Neovim with an amber-CRT signature. Available in dark and light variants with true color (24-bit) and 256-color terminal support.

## Variants

- **Spectral Dark** — amber phosphor on OLED black, with cool accents for balance
- **Spectral Light** — warm cream paper with the same amber signature

`:colorscheme spectral` picks the variant matching `&background`, so toggling between dark and light is just `set background=light \| colorscheme spectral` (or `dark`).

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
colorscheme spectral        " auto-picks dark or light from &background
" or force a variant explicitly:
colorscheme spectral-dark
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

### Spectral (dark)

| Color             | Hex       | Usage                              |
|-------------------|-----------|------------------------------------|
| Amber (signature) | `#FFB000` | Directories, Ruby symbols          |
| Red               | `#FF3B30` | Keywords, control flow             |
| Orange            | `#FF7A1C` | Parameters, special characters     |
| Yellow            | `#FFD60A` | Strings                            |
| Green             | `#B5E853` | Functions, methods                 |
| Cyan              | `#30D5C8` | Types, built-in functions          |
| Purple            | `#C678DD` | Constants, numbers, booleans       |

Background: `#181818` / Foreground: `#D8D4CC`

### Spectral Light

| Color             | Hex       | Usage                              |
|-------------------|-----------|------------------------------------|
| Amber (signature) | `#A35F00` | Directories, Ruby symbols          |
| Red               | `#C42828` | Keywords, control flow             |
| Orange            | `#B45418` | Parameters, special characters     |
| Yellow            | `#7D6700` | Strings                            |
| Green             | `#1F6B25` | Functions, methods                 |
| Cyan              | `#006978` | Types, built-in functions          |
| Purple            | `#6A3DAA` | Constants, numbers, booleans       |

Background: `#FAF6EC` / Foreground: `#2A241B`

## Terminal config

Matching terminal themes are included:

- **Ghostty** — `ghostty/spectral-dark`. Copy or symlink it into Ghostty's themes directory and reference it from your config.
- **iTerm2** — `iterm2/Spectral Dark.itermcolors` and `iterm2/Spectral Light.itermcolors`. Import via Settings → Profiles → Colors → Color Presets → Import. To apply both variants to a profile so iTerm2's automatic dark/light switching works, run `iterm2/sync.py <path-to-com.googlecode.iterm2.plist> [profile-name]` (default profile name is `Default`); the script writes the dark preset to the unsuffixed and `(Dark)` color keys and the light preset to the `(Light)` keys.

## Requirements

- Vim 7.4+ or Neovim 0.5+
- True color terminal support (recommended)

## License

MIT

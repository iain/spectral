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

## Editing the palette

The palette is defined in OKLCH (perceptually uniform) in `tools/palette.py` and emitted into the per-app files. To tweak a color, edit the `PALETTES` dict in that file and run `tools/palette.py` — it regenerates the two `colors/spectral-*.vim` files, the two `ghostty/spectral-*` files, and the two `iterm2/*.itermcolors` presets in one pass. After regenerating the iTerm2 presets, run `iterm2/sync.py <plist>` to push them to your iTerm2 plist. The `colors/` and `ghostty/` files are generated; do not hand-edit them.

## Color Palette

### Spectral Dark

| Color             | Hex       | Usage                              |
|-------------------|-----------|------------------------------------|
| Amber (signature) | `#F9AD26` | Directories, Ruby symbols          |
| Red               | `#FF544C` | Keywords, control flow             |
| Orange            | `#FF8432` | Parameters, special characters     |
| Yellow            | `#F8D700` | Strings                            |
| Green             | `#8DEF46` | Functions, methods                 |
| Cyan              | `#2AD7D7` | Types, built-in functions          |
| Purple            | `#CC77DF` | Constants, numbers, booleans       |

Background: `#1B1810` / Foreground: `#DCD0B5`

### Spectral Light

| Color             | Hex       | Usage                              |
|-------------------|-----------|------------------------------------|
| Amber (signature) | `#9D6300` | Directories, Ruby symbols          |
| Red               | `#AC1A1C` | Keywords, control flow             |
| Orange            | `#9C4700` | Parameters, special characters     |
| Yellow            | `#906B00` | Strings                            |
| Green             | `#357426` | Functions, methods                 |
| Cyan              | `#00707E` | Types, built-in functions          |
| Purple            | `#65389F` | Constants, numbers, booleans       |

Background: `#FEF4DF` / Foreground: `#2B2313`

## Terminal config

Matching terminal themes are included:

- **Ghostty** — `ghostty/spectral-dark`. Copy or symlink it into Ghostty's themes directory and reference it from your config.
- **iTerm2** — `iterm2/Spectral Dark.itermcolors` and `iterm2/Spectral Light.itermcolors`. Import via Settings → Profiles → Colors → Color Presets → Import. To apply both variants to a profile so iTerm2's automatic dark/light switching works, run `iterm2/sync.py <path-to-com.googlecode.iterm2.plist> [profile-name]` (default profile name is `Default`); the script writes the dark preset to the unsuffixed and `(Dark)` color keys and the light preset to the `(Light)` keys.

## Requirements

- Vim 7.4+ or Neovim 0.5+
- True color terminal support (recommended)

## License

MIT

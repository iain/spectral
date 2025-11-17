# Spectral

A beautiful dark Vim colorscheme based on Monokai Pro Spectrum, designed for comfortable long coding sessions with vibrant, carefully balanced colors.

## Features

- **True color support** - Full 24-bit color support for modern terminals
- **Comprehensive syntax highlighting** - Optimized for multiple languages including:
  - JavaScript/TypeScript
  - Python
  - Ruby
  - Go
  - HTML/CSS
  - Markdown
  - JSON/YAML/TOML
  - And many more
- **Plugin integration** - Built-in support for popular plugins:
  - GitGutter, Signify, fugitive
  - NERDTree and netrw (built-in file browser)
  - ALE, CoC
  - fzf, CtrlP
  - Telescope
  - vim-which-key
  - And more
- **Treesitter and LSP support** - Native support for modern Neovim features
- **Carefully crafted UI** - Thoughtfully designed interface elements for better readability

## Installation

### vim-plug

Add the following to your `.vimrc` or `init.vim`:

```vim
Plug 'iain/spectral'
```

Then run:

```vim
:PlugInstall
```

### Vundle

Add the following to your `.vimrc`:

```vim
Plugin 'iain/spectral'
```

Then run:

```vim
:PluginInstall
```

### Pathogen

Run the following in your terminal:

```bash
cd ~/.vim/bundle
git clone https://github.com/iain/spectral.git
```

### Manual Installation

1. Download the `spectral.vim` file
2. Create the colors directory if it doesn't exist:
   ```bash
   mkdir -p ~/.vim/colors
   ```
3. Copy the file to your colors directory:
   ```bash
   cp spectral.vim ~/.vim/colors/
   ```

For Neovim:
```bash
mkdir -p ~/.config/nvim/colors
cp spectral.vim ~/.config/nvim/colors/
```

## Usage

Add the following to your `.vimrc` or `init.vim`:

```vim
colorscheme spectral
```

### Recommended Terminal Settings

For the best experience, ensure your terminal supports 24-bit true colors and has the following settings enabled:

**For Vim:**
```vim
set termguicolors
```

**For Neovim:**
```vim
set termguicolors
```

## Requirements

- Vim 7.4+ or Neovim 0.5+
- Terminal with true color support (recommended)
- A font with good glyph coverage (optional, for plugin icons)

## Color Palette

Spectral uses a carefully selected color palette based on Monokai Pro Spectrum:

- Background: `#222222`
- Foreground: `#fbf8ff`
- Red: `#fc618d`
- Orange: `#fd9353`
- Yellow: `#fce566`
- Green: `#7bd88f`
- Cyan: `#5ad4e6`
- Purple: `#948ae3`

## Screenshots

*Coming soon*

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

MIT License - See LICENSE file for details

## Credits

Inspired by [Monokai Pro Spectrum](https://monokai.pro/) by Monokai.

---

Made with care for developers who spend hours in their editor.

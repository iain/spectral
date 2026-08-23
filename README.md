# Spectral

A warm, high-contrast colorscheme for Vim and Neovim with an amber-CRT signature. Available in dark and light variants with true color (24-bit) and 256-color terminal support. Matching themes ship for VS Code, Ghostty, iTerm2, and Mattermost.

## Variants

- **Spectral Dark** — amber phosphor on OLED black, with cool accents for balance
- **Spectral Light** — warm cream paper with the same amber signature

`:colorscheme spectral` picks the variant matching `&background`, so toggling between dark and light is just `set background=light \| colorscheme spectral` (or `dark`).

## Screenshots

Spectral Dark — note the Sorbet `sig` blocks, muted so type signatures recede
behind the code they annotate:

![Spectral Dark rendering a Ruby file with Sorbet type signatures](screenshots/billing-dark.svg)

Spectral Light, same file:

![Spectral Light rendering the same Ruby file](screenshots/billing-light.svg)

Python renderings of both variants are in [`screenshots/`](screenshots/).

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

### Statusline (lightline.vim)

Spectral ships a matching [lightline.vim](https://github.com/itchyny/lightline.vim) theme. Once spectral is on your runtimepath, point lightline at it:

```vim
let g:lightline = { 'colorscheme': 'spectral' }
```

The theme branches on `&background`, so it follows the editor variant — toggling `set background=light` (or `dark`) keeps the statusline in step after lightline reloads.

### Neovim Support

- Treesitter highlighting (Neovim 0.8+)
- LSP diagnostics, references, code lens, inlay hints, and signature help (Neovim 0.5+)
- LSP semantic tokens (Neovim 0.9+)
- Floating windows, WinBar, WinSeparator

### Ruby Sorbet

Sorbet type annotations (`sig` blocks, `T::` types, `extend T::Sig`) are rendered in a muted color to visually separate type signatures from application code. This is handled by `plugin/sorbet.vim` which loads automatically for Ruby files.

## Editing the palette

The palette is defined in OKLCH (perceptually uniform) in `tools/palette.py` and emitted into the per-app files. To tweak a color, edit the `PALETTES` dict in that file and run `tools/palette.py` — it regenerates the two `colors/spectral-*.vim` files, the two `ghostty/spectral-*` files, the two `iterm2/*.itermcolors` presets, the two `mattermost/spectral-*.json` files, the two `vscode/themes/spectral-*.json` themes, the `vscode/icon.png` marketplace icon, and the `autoload/lightline/colorscheme/spectral.vim` theme in one pass. After regenerating the iTerm2 presets, run `iterm2/sync.py <plist>` to push them to your iTerm2 plist. The `colors/`, `ghostty/`, `mattermost/`, `vscode/themes/`, `vscode/icon.png`, and `autoload/lightline/` files are generated; do not hand-edit them.

`tools/test_palette.py` asserts invariants on the generated output — valid hex everywhere, no TextMate scope claimed by two entries, and a contrast floor so nothing disappears into the background. Run it with `python3 -m unittest discover -s tools`; CI runs it alongside the drift check.

## Regenerating the screenshots

`tools/screenshots.py` renders every file in `tools/samples/` through a real
headless Vim and writes SVGs to `screenshots/`:

```bash
python3 tools/screenshots.py            # every sample, both variants
python3 tools/screenshots.py billing    # only samples matching a stem
```

The colors are not re-derived from `tools/palette.py` — they come from Vim's
own `:TOhtml`, which reports what the loaded colorscheme actually resolved each
syntax group to. A screenshot therefore cannot flatter the theme: if the
colorscheme breaks, the screenshot breaks identically.

Requires `vim` on `PATH`. Unlike the other generated files this is *not* part
of the CI drift check — `:TOhtml` markup shifts between Vim versions, so
regenerating on a different Vim would produce spurious diffs. Rerun it by hand
when the palette changes.

## Color Palette

Each variant is defined in OKLCH (L = lightness 0–1, C = chroma, H = hue in degrees) so the accents sit in a roughly equiluminant band — equal-feeling brightness across hues — and the neutrals share a single warm hue (yellow-orange at low chroma) for a coherent paper/phosphor character. Where requested chroma falls outside the sRGB gamut, the generator reduces it by bisection while preserving L and H; the displayed hex is therefore the closest representable color rather than always exactly the requested chroma.

### Spectral Dark

| Color             | OKLCH              | Hex       | Usage                              |
|-------------------|--------------------|-----------|------------------------------------|
| Amber (signature) | `0.80 / 0.16 / 75°`  | `#F9AD26` | Directories, Ruby symbols          |
| Red               | `0.68 / 0.22 / 27°`  | `#FF544C` | Keywords, control flow             |
| Orange            | `0.74 / 0.20 / 50°`  | `#FF8432` | Parameters, special characters     |
| Yellow            | `0.88 / 0.20 / 98°`  | `#F8D700` | Strings                            |
| Green             | `0.86 / 0.22 / 135°` | `#8DEF46` | Functions, methods                 |
| Cyan              | `0.80 / 0.13 / 195°` | `#2AD7D7` | Types, built-in functions          |
| Purple            | `0.70 / 0.17 / 320°` | `#CC77DF` | Constants, numbers, booleans       |

Background: `0.21 / 0.006 / 85°` → `#1A1815` / Foreground: `0.86 / 0.038 / 85°` → `#DCD0B5`

### Spectral Light

| Color             | OKLCH              | Hex       | Usage                              |
|-------------------|--------------------|-----------|------------------------------------|
| Amber (signature) | `0.55 / 0.13 / 70°`  | `#9D6300` | Directories, Ruby symbols          |
| Red               | `0.48 / 0.18 / 27°`  | `#AC1A1C` | Keywords, control flow             |
| Orange            | `0.50 / 0.15 / 50°`  | `#9C4700` | Parameters, special characters     |
| Yellow            | `0.65 / 0.15 / 95°`  | `#A98D00` | Strings                            |
| Green             | `0.50 / 0.13 / 140°` | `#357426` | Functions, methods                 |
| Cyan              | `0.50 / 0.10 / 210°` | `#00707E` | Types, built-in functions          |
| Purple            | `0.45 / 0.16 / 300°` | `#65389F` | Constants, numbers, booleans       |

Background: `0.985 / 0.020 / 85°` → `#FFFAEE` / Foreground: `0.26 / 0.030 / 85°` → `#2B2313`

## VS Code

The `vscode/` directory is a self-contained extension. The themes themselves —
`vscode/themes/spectral-dark.json` and `spectral-light.json` — are generated
from the same palette as everything else, and cover the workbench, the
integrated terminal's ANSI palette, TextMate scopes, and LSP semantic tokens.
So is `vscode/icon.png`, the Marketplace artwork — a miniature of the theme,
drawn straight from the dark palette with the stdlib alone, so it can never
drift from the colors it advertises.

To use it without publishing, symlink or copy `vscode/` into your extensions
directory and reload:

```bash
ln -s "$PWD/vscode" ~/.vscode/extensions/spectral
```

To build a `.vsix`:

```bash
cd vscode && npx @vscode/vsce package
```

Two places where the VS Code mapping deliberately departs from the Vim theme,
both because the Vim theme is internally inconsistent there:

- **Punctuation** is `fg_alt`, following the treesitter captures rather than
  the brighter per-language groups (`jsonBraces`, `cssBraces`).
- **Regular expressions** follow the richer `rubyRegexp*` treatment — cyan
  body, orange escapes, purple character classes — rather than the flat orange
  of `@string.regex`.

Sorbet type signatures are not dimmed in VS Code. That effect relies on the
custom syntax regions in `plugin/sorbet.vim`, which have no TextMate scope to
hook.

## Terminal config

Matching terminal themes are included:

- **Ghostty** — `ghostty/spectral-dark` and `ghostty/spectral-light`. Run `ghostty/install.sh` to symlink them into `${XDG_CONFIG_HOME:-~/.config}/ghostty/themes/`; your config can then reference them by name, e.g. `theme = dark:spectral-dark,light:spectral-light`. Pass `--force` to replace existing files at the destination.
- **iTerm2** — `iterm2/Spectral Dark.itermcolors` and `iterm2/Spectral Light.itermcolors`. Import via Settings → Profiles → Colors → Color Presets → Import. To apply both variants to a profile so iTerm2's automatic dark/light switching works, run `iterm2/sync.py <path-to-com.googlecode.iterm2.plist> [profile-name]` (default profile name is `Default`); the script writes the dark preset to the unsuffixed and `(Dark)` color keys and the light preset to the `(Light)` keys.

## Mattermost

`mattermost/spectral-dark.json` and `mattermost/spectral-light.json` are custom themes for Mattermost. Open Settings → Display → Theme → Custom Theme, expand "Copy/Paste Theme Colors", and paste the contents of the desired file. The amber signature anchors mentions, buttons, and the active-channel border; the team rail is the darkest neutral so the leftmost column reads as an anchor.

## Requirements

- Vim 7.4+ or Neovim 0.5+
- True color terminal support (recommended)

## License

MIT

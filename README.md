# Spectral

A warm, high-contrast colorscheme with an amber-CRT signature, in dark and
light variants.

- **Spectral Dark** — amber phosphor on OLED black, with cool accents for balance
- **Spectral Light** — warm cream paper with the same amber signature

Every target is generated from a single palette definition, so the colors match
exactly across your editor, your terminal, and everything else.

![Spectral Dark rendering a Ruby file with Sorbet type signatures](screenshots/billing-dark.svg)

Spectral Light, the same file:

![Spectral Light rendering the same Ruby file](screenshots/billing-light.svg)

Markdown, showing the per-level heading colors:

![Spectral Dark rendering a Markdown file with headings and links](screenshots/notes-dark.svg)

Python and light-variant renderings are in [`screenshots/`](screenshots/).

## Where it runs

| Application  | What ships                                                |
|--------------|-----------------------------------------------------------|
| Vim / Neovim | colorscheme, lightline theme, Sorbet syntax plugin        |
| VS Code      | extension — workbench, TextMate scopes, semantic tokens   |
| Ghostty      | two themes, plus an install script                         |
| iTerm2       | two presets, plus a profile sync script                    |
| Mattermost   | two custom themes                                          |

## Vim and Neovim

With [vim-plug](https://github.com/junegunn/vim-plug):

```vim
Plug 'iain/spectral'
```

With Pathogen, clone into `~/.vim/bundle`. Manually, copy `colors/` into
`~/.vim/colors` (Vim) or `~/.config/nvim/colors` (Neovim).

Then add to your `.vimrc` or `init.vim`:

```vim
set termguicolors
colorscheme spectral        " picks the variant matching &background
```

`spectral` follows `&background`, so `set background=light | colorscheme
spectral` switches variants. `spectral-dark` and `spectral-light` force one.

Requires Vim 7.4+ or Neovim 0.5+, and a true-color terminal.

**Languages** — Ruby (including Sorbet), Python, JavaScript, TypeScript, Go,
HTML, CSS, Markdown, JSON, YAML, TOML, XML, and Vim script.

**Plugins** — GitGutter, Signify, fugitive, NERDTree, netrw, ALE, CoC, fzf,
CtrlP, Telescope, Startify, and vim-which-key.

**Neovim** — Treesitter (0.8+), LSP diagnostics, references, code lens, inlay
hints and signature help (0.5+), semantic tokens (0.9+), floating windows,
WinBar and WinSeparator.

### Statusline

A matching [lightline.vim](https://github.com/itchyny/lightline.vim) theme
ships with the colorscheme. Once Spectral is on your runtimepath:

```vim
let g:lightline = { 'colorscheme': 'spectral' }
```

It branches on `&background`, so it follows the editor variant once lightline
reloads.

### Sorbet type signatures

Sorbet annotations — `sig` blocks, `T::` types, `extend T::Sig` — are rendered
in a muted color so type signatures recede behind the code they annotate.
`plugin/sorbet.vim` loads automatically for Ruby files.

## VS Code

`vscode/` is a self-contained extension covering the workbench, the integrated
terminal's ANSI palette, TextMate scopes, and LSP semantic tokens.

To use it without publishing, link it into your extensions directory and
reload:

```bash
ln -s "$PWD/vscode" ~/.vscode/extensions/spectral
```

To build a `.vsix`:

```bash
cd vscode && npx @vscode/vsce package
```

Two places where the VS Code mapping departs from the Vim theme, both because
the Vim theme is internally inconsistent there:

- **Punctuation** is `fg_alt`, following the Treesitter captures rather than
  the brighter per-language groups (`jsonBraces`, `cssBraces`).
- **Regular expressions** follow the richer `rubyRegexp*` treatment — cyan
  body, orange escapes, purple character classes — rather than the flat orange
  of `@string.regex`.

Sorbet signatures are not dimmed here: that effect relies on the custom syntax
regions in `plugin/sorbet.vim`, which have no TextMate scope to hook.

## Ghostty

`ghostty/spectral-dark` and `ghostty/spectral-light`. Run `ghostty/install.sh`
to symlink them into `${XDG_CONFIG_HOME:-~/.config}/ghostty/themes/`, then
reference them by name:

```
theme = dark:spectral-dark,light:spectral-light
```

Pass `--force` to replace existing files at the destination.

## iTerm2

`iterm2/Spectral Dark.itermcolors` and `iterm2/Spectral Light.itermcolors`.
Import via Settings → Profiles → Colors → Color Presets → Import.

To wire both variants into one profile so iTerm2's automatic dark/light
switching works:

```bash
iterm2/sync.py <path-to-com.googlecode.iterm2.plist> [profile-name]
```

The profile name defaults to `Default`. The script writes the dark preset to
the unsuffixed and `(Dark)` color keys, and the light preset to the `(Light)`
keys.

## Mattermost

`mattermost/spectral-dark.json` and `mattermost/spectral-light.json`. Open
Settings → Display → Theme → Custom Theme, expand "Copy/Paste Theme Colors",
and paste the contents of either file. The amber signature anchors mentions,
buttons, and the active-channel border; the team rail is the darkest neutral so
the leftmost column reads as an anchor.

## The palette

Each variant is defined in OKLCH — L = lightness 0–1, C = chroma, H = hue in
degrees — so the accents sit in a roughly equiluminant band, equal-feeling in
brightness across hues, and the neutrals all share one warm hue at low chroma
for a coherent paper/phosphor character.

![Spectral Dark palette — accents and the warm neutral ramp](screenshots/palette-dark.svg)

![Spectral Light palette — accents and the warm neutral ramp](screenshots/palette-light.svg)

### Spectral Dark

| Color             | OKLCH                | Hex       | Usage                          |
|-------------------|----------------------|-----------|--------------------------------|
| Amber (signature) | `0.80 / 0.16 / 75°`  | `#F9AD26` | Directories, Ruby symbols      |
| Red               | `0.68 / 0.22 / 27°`  | `#FF544C` | Keywords, control flow         |
| Orange            | `0.74 / 0.20 / 50°`  | `#FF8432` | Parameters, special characters |
| Yellow            | `0.88 / 0.20 / 98°`  | `#F8D700` | Strings                        |
| Green             | `0.86 / 0.22 / 135°` | `#8DEF46` | Functions, methods             |
| Cyan              | `0.80 / 0.13 / 195°` | `#2AD7D7` | Types, built-in functions      |
| Blue              | `0.72 / 0.18 / 255°` | `#60A7FF` | Links, namespaces              |
| Purple            | `0.70 / 0.17 / 320°` | `#CC77DF` | Constants, numbers, booleans   |

Background `0.21 / 0.006 / 85°` → `#1A1815` · Foreground `0.86 / 0.038 / 85°` → `#DCD0B5`

### Spectral Light

| Color             | OKLCH                 | Hex       | Usage                          |
|-------------------|-----------------------|-----------|--------------------------------|
| Amber (signature) | `0.58 / 0.124 / 72°`  | `#A76C01` | Directories, Ruby symbols      |
| Red               | `0.50 / 0.200 / 27°`  | `#BB0916` | Keywords, control flow         |
| Orange            | `0.56 / 0.183 / 38°`  | `#C83E01` | Parameters, special characters |
| Yellow            | `0.64 / 0.131 / 88°`  | `#AD8600` | Strings                        |
| Green             | `0.52 / 0.166 / 142°` | `#1A7F11` | Functions, methods             |
| Cyan              | `0.53 / 0.091 / 205°` | `#007A85` | Types, built-in functions      |
| Blue              | `0.45 / 0.148 / 255°` | `#0053A4` | Links, namespaces              |
| Purple            | `0.48 / 0.233 / 302°` | `#791DC7` | Constants, numbers, booleans   |

Background `0.985 / 0.020 / 85°` → `#FFFAEE` · Foreground `0.26 / 0.030 / 85°` → `#2B2313`

Two caveats on the tables. Where a requested chroma falls outside the sRGB
gamut the generator reduces it by bisection, preserving L and H, so each hex is
the closest representable color rather than exactly the requested chroma. And
some distinctions depend on what the editor can resolve — namespaces separate
from types only where Treesitter, LSP or semantic tokens are available, and
fall back to cyan under Vim's regex syntax.

## Working on the theme

The palette is the single source of truth. Edit the `PALETTES` dict in
`tools/palette.py` and run it to regenerate every target in one pass:

```bash
python3 tools/palette.py
```

That writes `colors/spectral-*.vim`, `ghostty/spectral-*`,
`iterm2/*.itermcolors`, `mattermost/spectral-*.json`,
`vscode/themes/spectral-*.json`, `vscode/icon.png`,
`screenshots/palette-*.svg`, and
`autoload/lightline/colorscheme/spectral.vim`. All of those are generated —
do not hand-edit them. After regenerating the iTerm2 presets, run
`iterm2/sync.py <plist>` to push them into your own plist.

### Tests

```bash
python3 -m unittest discover -s tools
```

These assert invariants on the generated output: valid hex everywhere, no
TextMate scope claimed by two entries, and a contrast floor so no token
disappears into the background. CI runs them alongside a check that the
generated files match the palette.

### Screenshots

```bash
python3 tools/screenshots.py            # every sample, both variants
python3 tools/screenshots.py billing    # only samples matching a stem
```

`tools/screenshots.py` renders each file in `tools/samples/` through a real
headless Vim and writes SVGs to `screenshots/`. The colors are not re-derived
from the palette — they come from Vim's own `:TOhtml`, which reports what the
loaded colorscheme actually resolved each syntax group to. A screenshot
therefore cannot flatter the theme: if the colorscheme breaks, the screenshot
breaks identically.

This needs `vim` on `PATH`, and unlike everything else it is *not* part of the
CI drift check — `:TOhtml` markup shifts between Vim versions, so regenerating
on a different Vim would produce spurious diffs. Rerun it by hand when the
palette changes. The `palette-*.svg` cards in the same directory are the
exception: they come from `tools/palette.py`, need no Vim, and are
drift-checked like every other generated file.

## License

MIT

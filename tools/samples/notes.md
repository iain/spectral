# Spectral

A warm, high-contrast colorscheme with an amber-CRT signature.

## Installation

Point your plugin manager at [the repository](https://github.com/iain/spectral),
or clone it directly into `~/.vim/bundle`. See <https://vimhelp.org/> if you
have not used a plugin manager before.

### Requirements

- Vim 7.4+ or Neovim 0.5+
- A **true colour** terminal (`set termguicolors`)
- Optionally *lightline*, for a matching statusline

#### Editing the palette

The palette lives in `tools/palette.py` and is defined in OKLCH:

```python
"amber": (0.80, 0.16, 75)
```

> Regenerate every port in one pass; the files under `colors/` are
> generated and should never be hand-edited.

1. Edit the `PALETTES` dict
2. Run `python3 tools/palette.py`
3. Commit the regenerated output

| Variant | Background | Signature |
|---------|-----------|-----------|
| Dark    | `#1A1815` | `#F9AD26` |
| Light   | `#FFFAEE` | `#A76C01` |

~~Terminal-only~~ Blue now carries links and namespaces too.

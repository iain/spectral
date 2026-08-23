# Spectral for VS Code

A warm, high-contrast colorscheme with an amber-CRT signature, in dark and
light variants.

- **Spectral Dark** — amber phosphor on OLED black, with cool accents for balance
- **Spectral Light** — warm cream paper with the same amber signature

Pick one from **Preferences → Theme → Color Theme** (`Ctrl+K Ctrl+T`).

## Design

The palette is defined in [OKLCH](https://bottosson.github.io/posts/oklab/), so
the accents sit in a roughly equiluminant band — no single hue jumps out as
brighter than the rest — and every neutral shares one warm yellow-orange hue at
low chroma. The result reads as amber phosphor rather than as a set of colors
that happen to be near each other.

| Role                        | Color   |
|-----------------------------|---------|
| Keywords, control flow      | Red     |
| Strings                     | Yellow  |
| Functions and methods       | Green   |
| Types, classes, namespaces  | Cyan    |
| Parameters, escapes         | Orange  |
| Constants, numbers, booleans| Purple  |
| Comments                    | Dimmed, italic |

Amber is reserved for the things the eye returns to constantly rather than for
body text: the cursor, badges, the active tab's top edge, the current
breadcrumb segment, buttons, and Ruby symbols.

## What's covered

- Workbench chrome — activity bar, side bar, tabs, status bar, panels, menus,
  notifications, quick input, peek view, diff editor
- Integrated terminal ANSI palette, matched to the Ghostty and iTerm2 presets
  so a terminal inside the editor matches one outside it
- TextMate scopes for the languages the Vim theme targets
- LSP semantic tokens, including modifiers (`readonly`, `deprecated`,
  `defaultLibrary`, `async`)
- Bracket pair colorization

## Also available for

Vim/Neovim, Ghostty, iTerm2, and Mattermost — see the
[main repository](https://github.com/iain/spectral).

## License

MIT

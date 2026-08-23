# Spectral for Zed

A warm, high-contrast colorscheme with an amber-CRT signature, in dark and
light variants.

- **Spectral Dark** — amber phosphor on OLED black, with cool accents for balance
- **Spectral Light** — warm cream paper with the same amber signature

Both ship in one theme family, so `"mode": "system"` switches between them:

```json
{
  "theme": {
    "mode": "system",
    "light": "Spectral Light",
    "dark": "Spectral Dark"
  }
}
```

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
| Types and classes           | Cyan    |
| Namespaces, links           | Blue    |
| Symbols, decorators, keys   | Amber   |
| Parameters, escapes         | Orange  |
| Constants, numbers, booleans| Purple  |
| Comments                    | Dimmed, italic |

Amber is the signature. In syntax it lands on whatever gives a language its
texture — Ruby symbols, Python decorators, JSON keys, Markdown list markers. In
the workbench it is reserved for what the eye returns to constantly rather than
for body text: the cursor, matched characters in the file finder and command
palette, and accent icons.

## What's covered

- Workbench chrome — title bar, tabs, panels, status bar, scrollbars, the git
  panel and the diff gutter
- Terminal ANSI palette, matched to the Ghostty and iTerm2 presets so a
  terminal inside the editor matches one outside it
- Syntax captures for the languages the Vim theme targets
- Collaboration cursors, drawn from the accent wheel

## Two departures from the Vim theme

- **Keys** are amber in Vim for JSON, YAML, TOML and CSS. Zed's grammars use
  one `property` capture for the key in a key/value pair *and* for member
  access on an object, so amber there would paint every `obj.field` amber too.
  JSON keys have a capture of their own and keep the signature; the rest follow
  body text.
- **Markdown headings** are one color rather than a ladder of six: Zed captures
  every heading level as `title`.

Zed's `theme_overrides` setting flips `property` back to amber if you would
rather have the keys and take the member access with them.

Sorbet signatures are not dimmed here either; that relies on the syntax regions
in `plugin/sorbet.vim`, which have no Zed equivalent.

## Also available for

Vim/Neovim, VS Code, Ghostty, iTerm2, and Mattermost — see the
[main repository](https://github.com/iain/spectral).

## License

MIT

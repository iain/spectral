#!/usr/bin/env python3
"""
Spectral palette generator.

Single source of truth for the colorscheme. Edit the PALETTES dict below in
OKLCH (perceptually uniform), then run this script to regenerate every
downstream file:

  colors/spectral-dark.vim
  colors/spectral-light.vim
  ghostty/spectral-dark
  ghostty/spectral-light
  iterm2/Spectral Dark.itermcolors
  iterm2/Spectral Light.itermcolors
  mattermost/spectral-dark.json
  mattermost/spectral-light.json
  vscode/themes/spectral-dark.json
  vscode/themes/spectral-light.json
  vscode/icon.png
  screenshots/palette-dark.svg
  screenshots/palette-light.svg

After regenerating, run iterm2/sync.py to push the iTerm2 presets to a
target plist.

Invariants for the generated output live in tools/test_palette.py:
  python3 -m unittest discover -s tools

OKLCH triples are (L, C, H):
  L  lightness, 0=black 1=white. Perceptually uniform.
  C  chroma, 0=gray; the sRGB gamut peaks around 0.3 in mid lightness, less
     near black or white. Out-of-gamut chroma is reduced by bisection (L and
     H are preserved; the color stays the same hue but desaturates as needed).
  H  hue in degrees: 0=pink/red, 30=orange, 90=yellow-green, 150=green,
     210=cyan, 270=blue, 330=magenta.
"""
from __future__ import annotations

import json
import math
import plistlib
import struct
import zlib
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Warm-tinted neutrals — yellow-orange hue at very low chroma so the bg/fg
# ramp echoes the amber signature without looking colored.
NEUTRAL_HUE = 85.0

PALETTES: dict[str, dict[str, tuple[float, float, float]]] = {
    "dark": {
        # Backgrounds — warm dark. Chroma stays low: real amber CRTs have
        # near-black off-pixels, the warmth comes from the lit phosphor, not
        # the field. Just enough tint to keep the neutrals from reading cool.
        "bg":        (0.21, 0.006, NEUTRAL_HUE),
        "bg_alt":    (0.27, 0.008, NEUTRAL_HUE),
        "bg_alt2":   (0.36, 0.012, NEUTRAL_HUE),
        # Foregrounds
        "fg_dark":   (0.46, 0.022, NEUTRAL_HUE),
        "fg_darker": (0.56, 0.026, NEUTRAL_HUE),
        "fg_alt":    (0.68, 0.030, NEUTRAL_HUE),
        "fg":        (0.86, 0.038, NEUTRAL_HUE),
        "fg_light":  (0.93, 0.040, NEUTRAL_HUE),
        # Accents — equi-L band centered ~0.78 so the wheel looks balanced.
        # Yellow/green sit slightly higher because the eye reads them dimmer
        # at equal L; pulling them down would make them feel muddy.
        "red":       (0.68, 0.22, 27),
        "orange":    (0.74, 0.20, 50),
        "yellow":    (0.88, 0.20, 98),
        "green":     (0.86, 0.22, 135),
        "cyan":      (0.80, 0.13, 195),
        "blue":      (0.72, 0.18, 255),
        "purple":    (0.70, 0.17, 320),
        # Constants
        "white":     (1.00, 0.00, 0),
        "black":     (0.00, 0.00, 0),
        "tab_bg":    (0.12, 0.005, NEUTRAL_HUE),
        # Signature — overrides Directory/netrwDir/rubySymbol
        "amber":     (0.80, 0.16, 75),
    },
    "light": {
        "bg":        (0.985, 0.020, NEUTRAL_HUE),
        "bg_alt":    (0.94, 0.035, NEUTRAL_HUE),
        "bg_alt2":   (0.89, 0.040, NEUTRAL_HUE),
        "fg_dark":   (0.50, 0.040, NEUTRAL_HUE),
        "fg_darker": (0.44, 0.040, NEUTRAL_HUE),
        "fg_alt":    (0.36, 0.035, NEUTRAL_HUE),
        "fg":        (0.26, 0.030, NEUTRAL_HUE),
        "fg_light":  (0.18, 0.025, NEUTRAL_HUE),
        # Accents — equi-L band ~0.48 for legible contrast on cream paper.
        "red":       (0.48, 0.18, 27),
        "orange":    (0.50, 0.15, 50),
        "yellow":    (0.65, 0.15, 95),
        "green":     (0.50, 0.13, 140),
        "cyan":      (0.50, 0.10, 210),
        "blue":      (0.42, 0.15, 255),
        "purple":    (0.45, 0.16, 300),
        "white":     (1.00, 0.00, 0),
        "black":     (0.00, 0.00, 0),
        "tab_bg":    (0.92, 0.035, NEUTRAL_HUE),
        "amber":     (0.55, 0.13, 70),
    },
}


# --------------------------------------------------------------------------
# OKLCH → sRGB (Björn Ottosson, https://bottosson.github.io/posts/oklab/)
# --------------------------------------------------------------------------

def oklab_to_linear_srgb(L: float, a: float, b: float) -> tuple[float, float, float]:
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (
        +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


def linear_to_srgb(c: float) -> float:
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def in_gamut(rgb_linear: tuple[float, float, float]) -> bool:
    return all(-1e-6 <= c <= 1 + 1e-6 for c in rgb_linear)


def oklch_to_rgb(L: float, C: float, H: float) -> tuple[int, int, int]:
    """OKLCH → 8-bit sRGB. Reduces chroma by bisection if out of gamut."""
    h_rad = math.radians(H)

    def at(c: float) -> tuple[float, float, float]:
        return oklab_to_linear_srgb(L, c * math.cos(h_rad), c * math.sin(h_rad))

    chroma = C
    if not in_gamut(at(chroma)):
        lo, hi = 0.0, C
        for _ in range(24):
            mid = (lo + hi) / 2
            if in_gamut(at(mid)):
                lo = mid
            else:
                hi = mid
        chroma = lo

    r, g, b = (max(0.0, min(1.0, c)) for c in at(chroma))
    return (
        round(linear_to_srgb(r) * 255),
        round(linear_to_srgb(g) * 255),
        round(linear_to_srgb(b) * 255),
    )


# --------------------------------------------------------------------------
# 256-color (xterm) cterm fallback — nearest neighbor in RGB
# --------------------------------------------------------------------------

def _xterm256_table() -> list[tuple[int, tuple[int, int, int]]]:
    table = []
    levels = [0, 95, 135, 175, 215, 255]
    for r in range(6):
        for g in range(6):
            for b in range(6):
                table.append((16 + 36 * r + 6 * g + b, (levels[r], levels[g], levels[b])))
    for i in range(24):
        v = 8 + 10 * i
        table.append((232 + i, (v, v, v)))
    return table


_XTERM256 = _xterm256_table()


def cterm_for(rgb: tuple[int, int, int]) -> int:
    r, g, b = rgb
    chroma = max(rgb) - min(rgb)
    # For saturated inputs, exclude the grayscale ramp — it often beats the
    # cube on naive RGB distance for darker hues but reads as gray in the
    # terminal, which is worse than any color match.
    pool = [e for e in _XTERM256 if e[0] < 232] if chroma > 25 else _XTERM256
    return min(pool, key=lambda e: (e[1][0]-r)**2 + (e[1][1]-g)**2 + (e[1][2]-b)**2)[0]


# --------------------------------------------------------------------------
# Resolve OKLCH spec → {slot: {gui: hex, cterm: int, rgb: (r,g,b)}}
# --------------------------------------------------------------------------

def resolve(spec: dict) -> dict:
    out = {}
    for name, (L, C, H) in spec.items():
        rgb = oklch_to_rgb(L, C, H)
        out[name] = {
            "gui": f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}",
            "cterm": cterm_for(rgb),
            "rgb": rgb,
        }
    return out


# --------------------------------------------------------------------------
# Vim emitter
# --------------------------------------------------------------------------

VIM_PALETTE_KEYS = [
    "bg", "bg_alt", "bg_alt2",
    "fg_dark", "fg_darker", "fg_alt", "fg_light", "fg",
    "white",
    "red", "orange", "yellow", "green", "cyan", "purple",
    "black", "tab_bg",
]

VIM_DESC = {
    "dark":  "Amber CRT phosphor on OLED black, with cool accents for balance.",
    "light": "Warm paper with burnt-amber signature and balanced accents.",
}


def emit_vim(variant: str, palette: dict) -> str:
    title = "Spectral " + ("Dark" if variant == "dark" else "Light")
    lines = [
        '" ===============================================================',
        f'" {title}',
        f'" {VIM_DESC[variant]}',
        '" Maintainer:   iain',
        '" License:      MIT',
        '" GENERATED FILE — edit tools/palette.py and regenerate.',
        '" ===============================================================',
        '',
        'hi clear',
        "if exists('syntax_on')",
        '  syntax reset',
        'endif',
        '',
        f'set background={variant}',
        f"let g:colors_name = 'spectral-{variant}'",
        '',
        f"let s:amber = {{'gui': '#{palette['amber']['gui']}', 'cterm': '{palette['amber']['cterm']}'}}",
        '',
        'call spectral#apply({',
    ]
    for k in VIM_PALETTE_KEYS:
        s = palette[k]
        key = f"'{k}':"
        lines.append(f"  \\ {key:<13}{{'gui': '#{s['gui']}', 'cterm': '{s['cterm']}'}},")
    lines.append('  \\ })')
    lines.append('')
    lines.append('" Amber accents: anchor the palette on a few high-frequency elements so')
    lines.append('" the signature color keeps its presence without dominating body text.')
    lines.append("let s:fg = 'guifg=' . s:amber.gui . ' ctermfg=' . s:amber.cterm")
    for group in ("Directory", "netrwDir", "netrwDirSlash", "netrwClassify", "rubySymbol"):
        lines.append(f"exe 'hi {group:<13} ' . s:fg")
    lines.append('')
    lines.append('" vim: set sw=2 ts=2 sts=2 et tw=80 ft=vim:')
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# lightline.vim emitter
# --------------------------------------------------------------------------

# Statusline palette, mapped to colorscheme slots. Each cell is [fg, bg];
# lightline#colorscheme#flatten() merges the [gui, cterm] primitives into the
# [guifg, guibg, ctermfg, ctermbg] form lightline expects. The mode block (the
# first cell of every *.left) carries the signature accent — amber in normal,
# the conventional green/red/purple for insert/replace/visual. Subkeys mirror
# the set lightline's bundled themes define; missing modes fall back to normal.
LIGHTLINE_SECTIONS: list[tuple[str, str, list[list[str]]]] = [
    ("normal",   "left",    [["bg", "amber"], ["fg_light", "bg_alt2"]]),
    ("normal",   "right",   [["fg_light", "bg_alt2"], ["fg_alt", "bg_alt"]]),
    ("normal",   "middle",  [["fg_darker", "bg_alt"]]),
    ("normal",   "error",   [["bg", "red"]]),
    ("normal",   "warning", [["bg", "yellow"]]),
    ("inactive", "left",    [["fg_dark", "bg_alt"], ["fg_dark", "bg"]]),
    ("inactive", "right",   [["fg_dark", "bg_alt"], ["fg_dark", "bg"]]),
    ("inactive", "middle",  [["fg_dark", "bg"]]),
    ("insert",   "left",    [["bg", "green"], ["fg_light", "bg_alt2"]]),
    ("replace",  "left",    [["bg", "red"], ["fg_light", "bg_alt2"]]),
    ("visual",   "left",    [["bg", "purple"], ["fg_light", "bg_alt2"]]),
    ("tabline",  "left",    [["fg_alt", "tab_bg"]]),
    ("tabline",  "tabsel",  [["fg_light", "bg"]]),
    ("tabline",  "middle",  [["fg_dark", "tab_bg"]]),
    ("tabline",  "right",   [["fg_alt", "tab_bg"]]),
]


def emit_lightline(palettes: dict[str, dict]) -> str:
    # Slots referenced by the sections, in first-seen order.
    slots: list[str] = []
    for _, _, cells in LIGHTLINE_SECTIONS:
        for cell in cells:
            for slot in cell:
                if slot not in slots:
                    slots.append(slot)

    def primitives(variant: str) -> list[str]:
        return [
            f"  let s:{slot} = ['#{palettes[variant][slot]['gui']}', "
            f"{palettes[variant][slot]['cterm']}]"
            for slot in slots
        ]

    lines = [
        '" ===============================================================',
        '" Spectral — lightline.vim theme',
        '" Statusline palette matching the editor colorscheme. Branches on',
        '" &background, so `let g:lightline.colorscheme = \'spectral\'` tracks',
        '" whichever variant is active.',
        '" Maintainer:   iain',
        '" License:      MIT',
        '" GENERATED FILE — edit tools/palette.py and regenerate.',
        '" ===============================================================',
        '',
        "let s:p = {'normal': {}, 'inactive': {}, 'insert': {}, "
        "'replace': {}, 'visual': {}, 'tabline': {}}",
        '',
        "if &background ==# 'light'",
        *primitives("light"),
        'else',
        *primitives("dark"),
        'endif',
        '',
    ]
    for mode, sub, cells in LIGHTLINE_SECTIONS:
        rendered = ", ".join(
            "[" + ", ".join(f"s:{slot}" for slot in cell) + "]" for cell in cells
        )
        lines.append(f"let s:p.{mode}.{sub} = [ {rendered} ]")
    lines.append('')
    lines.append(
        "let g:lightline#colorscheme#spectral#palette = "
        "lightline#colorscheme#flatten(s:p)"
    )
    lines.append('')
    lines.append('" vim: set sw=2 ts=2 sts=2 et tw=80 ft=vim:')
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# Ghostty emitter
# --------------------------------------------------------------------------

# ANSI palette mapping for the terminal: indexes 0-7 standard, 8-15 bright.
# Terminal ANSI doesn't have a clean 1:1 with the colorscheme palette — it
# needs a blue (which the editor palette doesn't carry). Map deliberately:
GHOSTTY_ANSI = {
    "dark": {
        0: "bg_alt",  1: "red",     2: "green",   3: "yellow",
        4: "blue",    5: "purple",  6: "cyan",    7: "fg",
        # Brights are the same hues, slightly lifted (we use the palette's
        # naturally lighter slots where possible; otherwise reuse the base).
        8: "fg_dark",
    },
    "light": {
        0: "fg_alt",  1: "red",     2: "green",   3: "yellow",
        4: "blue",    5: "purple",  6: "cyan",    7: "bg_alt2",
        8: "fg_dark",
    },
}


def _bright(palette_oklch: dict, slot: str, variant: str) -> tuple[float, float, float]:
    """Derive a 'bright' version of an accent.

    On dark variants 'bright' means closer to white; on light variants it
    means closer to black (more emphatic on a light bg). Hue and chroma are
    preserved — only L moves.
    """
    L, C, H = palette_oklch[slot]
    delta = +0.07 if variant == "dark" else -0.10
    return max(0.0, min(1.0, L + delta)), C, H


def emit_ghostty(variant: str, palette: dict, palette_oklch: dict) -> str:
    title = "Spectral " + ("Dark" if variant == "dark" else "Light")
    cursor_text = palette["bg"]["gui"]
    lines = [
        f"# {title} — generated from tools/palette.py",
        "",
        f"background = {palette['bg']['gui']}",
        f"foreground = {palette['fg']['gui']}",
        "",
        f"cursor-color = {palette['amber']['gui']}",
        f"cursor-text = {cursor_text}",
        "",
        f"selection-background = {palette['bg_alt2']['gui']}",
        f"selection-foreground = {palette['fg']['gui']}",
        "",
        "# ANSI palette",
    ]
    base_map = GHOSTTY_ANSI[variant]
    for i in range(8):
        slot = base_map[i]
        lines.append(f"palette = {i}=#{palette[slot]['gui']}")
    lines.append("")
    lines.append("# Bright")
    for i in range(8, 16):
        slot = base_map.get(i, base_map[i - 8])
        # Derive bright variant via _bright() on the OKLCH spec
        if i == 8:
            bright_rgb = oklch_to_rgb(*palette_oklch[slot])
        elif i == 15:
            bright_rgb = oklch_to_rgb(*palette_oklch["white"])
        else:
            bright_rgb = oklch_to_rgb(*_bright(palette_oklch, base_map[i - 8], variant))
        lines.append(f"palette = {i}=#{bright_rgb[0]:02X}{bright_rgb[1]:02X}{bright_rgb[2]:02X}")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# iTerm2 .itermcolors emitter
# --------------------------------------------------------------------------

def _color_dict(rgb: tuple[int, int, int]) -> dict:
    return {
        "Alpha Component": 1.0,
        "Color Space": "sRGB",
        "Red Component":   rgb[0] / 255.0,
        "Green Component": rgb[1] / 255.0,
        "Blue Component":  rgb[2] / 255.0,
    }


def emit_itermcolors(variant: str, palette: dict, palette_oklch: dict) -> dict:
    base_map = GHOSTTY_ANSI[variant]
    out = {}
    for i in range(8):
        out[f"Ansi {i} Color"] = _color_dict(palette[base_map[i]]["rgb"])
    for i in range(8, 16):
        if i == 8:
            rgb = palette[base_map[8]]["rgb"]
        elif i == 15:
            rgb = palette["white"]["rgb"]
        else:
            rgb = oklch_to_rgb(*_bright(palette_oklch, base_map[i - 8], variant))
        out[f"Ansi {i} Color"] = _color_dict(rgb)

    out["Background Color"]    = _color_dict(palette["bg"]["rgb"])
    out["Foreground Color"]    = _color_dict(palette["fg"]["rgb"])
    out["Bold Color"]          = _color_dict(palette["fg_light"]["rgb"])
    out["Link Color"]          = _color_dict(palette["cyan"]["rgb"])
    out["Selection Color"]     = _color_dict(palette["bg_alt2"]["rgb"])
    out["Selected Text Color"] = _color_dict(palette["fg"]["rgb"])
    out["Cursor Color"]        = _color_dict(palette["amber"]["rgb"])
    out["Cursor Text Color"]   = _color_dict(palette["bg"]["rgb"])
    out["Cursor Guide Color"]  = _color_dict(palette["bg_alt"]["rgb"])
    out["Badge Color"]         = _color_dict(palette["red"]["rgb"])
    return out


# --------------------------------------------------------------------------
# Mattermost custom theme emitter
# --------------------------------------------------------------------------

# Map Mattermost theme keys to palette slots. Order matches Mattermost's
# documented theme element order so the generated JSON is legible top-to-bottom.
MATTERMOST_KEYS: dict[str, dict[str, str]] = {
    "dark": {
        "sidebarBg":               "tab_bg",
        "sidebarText":             "fg_alt",
        "sidebarUnreadText":       "fg_light",
        "sidebarTextHoverBg":      "bg_alt",
        "sidebarTextActiveBorder": "amber",
        "sidebarTextActiveColor":  "fg_light",
        "sidebarHeaderBg":         "tab_bg",
        "sidebarHeaderTextColor":  "amber",
        "sidebarTeamBarBg":        "tab_bg",
        "onlineIndicator":         "green",
        "awayIndicator":           "yellow",
        "dndIndicator":            "red",
        "mentionBg":               "amber",
        "mentionColor":            "bg",
        "centerChannelBg":         "bg",
        "centerChannelColor":      "fg",
        "newMessageSeparator":     "red",
        "errorTextColor":          "red",
        "mentionHighlightLink":    "cyan",
        "linkColor":               "cyan",
        "buttonBg":                "amber",
        "buttonColor":             "bg",
    },
    "light": {
        "sidebarBg":               "bg_alt2",
        "sidebarText":             "fg_alt",
        "sidebarUnreadText":       "fg_light",
        "sidebarTextHoverBg":      "bg_alt",
        "sidebarTextActiveBorder": "amber",
        "sidebarTextActiveColor":  "fg_light",
        "sidebarHeaderBg":         "bg_alt2",
        "sidebarHeaderTextColor":  "amber",
        "sidebarTeamBarBg":        "bg_alt2",
        "onlineIndicator":         "green",
        "awayIndicator":           "yellow",
        "dndIndicator":            "red",
        "mentionBg":               "amber",
        "mentionColor":            "bg",
        "centerChannelBg":         "bg",
        "centerChannelColor":      "fg",
        "newMessageSeparator":     "red",
        "errorTextColor":          "red",
        "mentionHighlightLink":    "cyan",
        "linkColor":               "cyan",
        "buttonBg":                "amber",
        "buttonColor":             "bg",
    },
}

MATTERMOST_CODE_THEME = {"dark": "monokai", "light": "github"}


def _mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    """Linear mix in sRGB. t=0 returns a, t=1 returns b."""
    return tuple(round(a[i] * (1 - t) + b[i] * t) for i in range(3))  # type: ignore[return-value]


def emit_mattermost(variant: str, palette: dict) -> str:
    # mentionHighlightBg is a faint amber wash over the channel background —
    # subtle enough that quoted/highlighted text stays readable.
    highlight_rgb = _mix(palette["bg"]["rgb"], palette["amber"]["rgb"], 0.28)
    highlight_hex = f"#{highlight_rgb[0]:02X}{highlight_rgb[1]:02X}{highlight_rgb[2]:02X}"

    out: dict[str, str] = {"type": "custom"}
    for key, slot in MATTERMOST_KEYS[variant].items():
        out[key] = f"#{palette[slot]['gui']}"
        if key == "errorTextColor":
            out["mentionHighlightBg"] = highlight_hex
    out["codeTheme"] = MATTERMOST_CODE_THEME[variant]
    return json.dumps(out, indent=2) + "\n"


# --------------------------------------------------------------------------
# VS Code emitter
# --------------------------------------------------------------------------

# Values in the maps below are one of:
#   "slot"                     — the palette slot, opaque
#   ("alpha", "slot", a)       — the slot at alpha a (VS Code takes #RRGGBBAA)
#   ("mix", "a", "b", t)       — a blended t of the way toward b, opaque
#
# Blends exist because VS Code paints some states as a background wash over
# live text (find matches, diff lines) where a solid accent would swallow it.

def _vsc(palette: dict, value) -> str:
    if isinstance(value, str):
        return f"#{palette[value]['gui']}"
    kind = value[0]
    if kind == "alpha":
        _, slot, a = value
        return f"#{palette[slot]['gui']}{round(a * 255):02X}"
    if kind == "mix":
        _, a_slot, b_slot, t = value
        rgb = _mix(palette[a_slot]["rgb"], palette[b_slot]["rgb"], t)
        return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"
    raise ValueError(f"unknown color spec: {value!r}")


# Workbench colors. Slots are semantic (bg is "the editor field", fg is "body
# text"), so one map serves both variants — the palette flips underneath it.
#
# The amber signature is placed the way it is in the vim theme and Mattermost:
# on the things the eye returns to constantly rather than on body text — the
# cursor, badges, the active tab's top edge, the breadcrumb leaf, and buttons.
VSCODE_UI: dict[str, object] = {
    # Base
    "focusBorder":                        "cyan",
    "foreground":                         "fg",
    "disabledForeground":                 "fg_dark",
    "descriptionForeground":              "fg_darker",
    "errorForeground":                    "red",
    "widget.border":                      "bg_alt2",
    "widget.shadow":                      ("alpha", "tab_bg", 0.50),
    "selection.background":               "bg_alt2",
    "icon.foreground":                    "fg_alt",
    "sash.hoverBorder":                   "amber",

    # Text (rendered markdown in hovers, walkthroughs, release notes)
    "textLink.foreground":                "cyan",
    "textLink.activeForeground":          "amber",
    "textBlockQuote.background":          "bg_alt",
    "textBlockQuote.border":              "fg_dark",
    "textCodeBlock.background":           "bg_alt",
    "textPreformat.foreground":           "green",
    "textSeparator.foreground":           "fg_dark",

    # Buttons
    "button.background":                  "amber",
    "button.foreground":                  "bg",
    "button.hoverBackground":             ("mix", "amber", "fg_light", 0.20),
    "button.secondaryBackground":         "bg_alt2",
    "button.secondaryForeground":         "fg",
    "button.secondaryHoverBackground":    "fg_dark",
    "badge.background":                   "amber",
    "badge.foreground":                   "bg",
    "progressBar.background":             "amber",

    # Lists and trees
    "list.activeSelectionBackground":     "bg_alt2",
    "list.activeSelectionForeground":     "fg_light",
    "list.inactiveSelectionBackground":   "bg_alt",
    "list.inactiveSelectionForeground":   "fg",
    "list.hoverBackground":               "bg_alt",
    "list.hoverForeground":               "fg_light",
    "list.focusBackground":               "bg_alt2",
    "list.focusForeground":               "fg_light",
    # Fuzzy-match highlight — the vim theme's amber lands on Directory, which
    # has no VS Code equivalent; the quick-open match is where a file list
    # picks up the signature instead.
    "list.highlightForeground":           "amber",
    "list.focusHighlightForeground":      "amber",
    "list.errorForeground":               "red",
    "list.warningForeground":             "yellow",
    "list.dropBackground":                "bg_alt2",
    "listFilterWidget.background":        "bg_alt",
    "listFilterWidget.outline":           "amber",
    "listFilterWidget.noMatchesOutline":  "red",
    "tree.indentGuidesStroke":            "fg_dark",
    "tree.inactiveIndentGuidesStroke":    "bg_alt2",

    # Activity bar — the darkest neutral, so the leftmost rail anchors the
    # window (same reasoning as the Mattermost team rail).
    "activityBar.background":             "tab_bg",
    "activityBar.foreground":             "fg_light",
    # A step up from fg_dark: these icons are click targets, not chrome.
    "activityBar.inactiveForeground":     "fg_darker",
    "activityBar.border":                 "bg_alt",
    "activityBar.activeBorder":           "amber",
    "activityBarBadge.background":        "amber",
    "activityBarBadge.foreground":        "bg",

    # Side bar
    "sideBar.background":                 "bg_alt",
    "sideBar.foreground":                 "fg_alt",
    "sideBar.border":                     "bg_alt2",
    "sideBarTitle.foreground":            "fg_darker",
    "sideBarSectionHeader.background":    "bg_alt2",
    "sideBarSectionHeader.foreground":    "fg",
    "sideBarSectionHeader.border":        "bg_alt2",

    # Editor groups and tabs
    "editorGroup.border":                 "bg_alt2",
    "editorGroup.dropBackground":         ("alpha", "bg_alt2", 0.60),
    "editorGroupHeader.tabsBackground":   "tab_bg",
    "editorGroupHeader.tabsBorder":       "bg_alt",
    "editorGroupHeader.noTabsBackground": "tab_bg",
    "tab.activeBackground":               "bg",
    "tab.activeForeground":               "fg_light",
    "tab.activeBorderTop":                "amber",
    "tab.inactiveBackground":             "tab_bg",
    "tab.inactiveForeground":             "fg_alt",
    "tab.hoverBackground":                "bg_alt",
    "tab.hoverForeground":                "fg",
    "tab.border":                         "tab_bg",
    "tab.unfocusedActiveForeground":      "fg_alt",
    "tab.unfocusedInactiveForeground":    "fg_dark",
    "tab.lastPinnedBorder":               "bg_alt2",

    # Editor
    "editor.background":                  "bg",
    "editor.foreground":                  "fg",
    "editorLineNumber.foreground":        "fg_dark",
    "editorLineNumber.activeForeground":  "fg_light",
    "editorCursor.foreground":            "amber",
    "editorCursor.background":            "bg",
    "editor.selectionBackground":         "bg_alt2",
    "editor.selectionHighlightBackground": ("alpha", "bg_alt2", 0.60),
    "editor.inactiveSelectionBackground": "bg_alt",
    "editor.wordHighlightBackground":     ("alpha", "bg_alt2", 0.70),
    "editor.wordHighlightStrongBackground": "bg_alt2",
    "editor.lineHighlightBackground":     "bg_alt",
    "editor.rangeHighlightBackground":    "bg_alt",
    "editor.hoverHighlightBackground":    "bg_alt2",
    # Search: yellow for the field of matches, orange for the one you are on —
    # mirrors Search/IncSearch in the vim theme, washed so text stays legible.
    "editor.findMatchBackground":         ("mix", "bg", "orange", 0.42),
    "editor.findMatchHighlightBackground": ("mix", "bg", "yellow", 0.22),
    "editor.findRangeHighlightBackground": "bg_alt",
    "editorLink.activeForeground":        "cyan",
    "editorWhitespace.foreground":        "fg_dark",
    "editorIndentGuide.background1":      "bg_alt2",
    "editorIndentGuide.activeBackground1": "fg_dark",
    "editorRuler.foreground":             "bg_alt2",
    "editorCodeLens.foreground":          "fg_dark",
    "editorInlayHint.foreground":         "fg_dark",
    "editorInlayHint.background":         "bg_alt",
    "editorBracketMatch.background":      "bg_alt2",
    "editorBracketMatch.border":          "yellow",
    "editorBracketHighlight.foreground1": "fg_alt",
    "editorBracketHighlight.foreground2": "purple",
    "editorBracketHighlight.foreground3": "cyan",
    "editorBracketHighlight.foreground4": "green",
    "editorBracketHighlight.foreground5": "orange",
    "editorBracketHighlight.foreground6": "amber",
    "editorBracketHighlight.unexpectedBracket.foreground": "red",

    # Diagnostics
    "editorError.foreground":             "red",
    "editorWarning.foreground":           "yellow",
    "editorInfo.foreground":              "cyan",
    "editorHint.foreground":              "purple",
    "problemsErrorIcon.foreground":       "red",
    "problemsWarningIcon.foreground":     "yellow",
    "problemsInfoIcon.foreground":        "cyan",

    # Gutter
    "editorGutter.background":            "bg",
    "editorGutter.addedBackground":       "green",
    "editorGutter.modifiedBackground":    "yellow",
    "editorGutter.deletedBackground":     "red",

    # Overview ruler
    "editorOverviewRuler.border":         "bg_alt",
    "editorOverviewRuler.findMatchForeground":  "yellow",
    "editorOverviewRuler.errorForeground":      "red",
    "editorOverviewRuler.warningForeground":    "yellow",
    "editorOverviewRuler.infoForeground":       "cyan",
    "editorOverviewRuler.addedForeground":      "green",
    "editorOverviewRuler.modifiedForeground":   "yellow",
    "editorOverviewRuler.deletedForeground":    "red",
    "editorOverviewRuler.selectionHighlightForeground": "fg_dark",
    "editorOverviewRuler.wordHighlightForeground":      "fg_darker",

    # Diff
    "diffEditor.insertedTextBackground":  ("mix", "bg", "green", 0.16),
    "diffEditor.removedTextBackground":   ("mix", "bg", "red", 0.16),
    "diffEditor.insertedLineBackground":  ("mix", "bg", "green", 0.10),
    "diffEditor.removedLineBackground":   ("mix", "bg", "red", 0.10),
    "diffEditor.border":                  "bg_alt2",

    # Widgets
    "editorWidget.background":            "bg_alt",
    "editorWidget.foreground":            "fg",
    "editorWidget.border":                "bg_alt2",
    "editorWidget.resizeBorder":          "amber",
    "editorSuggestWidget.background":     "bg_alt",
    "editorSuggestWidget.border":         "bg_alt2",
    "editorSuggestWidget.foreground":     "fg",
    "editorSuggestWidget.highlightForeground":      "cyan",
    "editorSuggestWidget.focusHighlightForeground": "cyan",
    "editorSuggestWidget.selectedBackground":       "bg_alt2",
    "editorSuggestWidget.selectedForeground":       "fg_light",
    "editorHoverWidget.background":       "bg_alt",
    "editorHoverWidget.foreground":       "fg",
    "editorHoverWidget.border":           "bg_alt2",
    "editorGhostText.foreground":         "fg_dark",

    # Peek view
    "peekView.border":                    "cyan",
    "peekViewEditor.background":          "bg_alt",
    "peekViewEditor.matchHighlightBackground": ("mix", "bg_alt", "yellow", 0.28),
    "peekViewResult.background":          "bg_alt",
    "peekViewResult.selectionBackground": "bg_alt2",
    "peekViewResult.selectionForeground": "fg_light",
    "peekViewResult.lineForeground":      "fg",
    "peekViewResult.fileForeground":      "fg_light",
    "peekViewResult.matchHighlightBackground": ("mix", "bg_alt", "yellow", 0.28),
    "peekViewTitle.background":           "bg_alt2",
    "peekViewTitleLabel.foreground":      "fg_light",
    "peekViewTitleDescription.foreground": "fg_darker",

    # Panel and terminal
    "panel.background":                   "bg",
    "panel.border":                       "bg_alt2",
    "panelTitle.activeForeground":        "fg_light",
    "panelTitle.activeBorder":            "amber",
    "panelTitle.inactiveForeground":      "fg_dark",
    "panelSection.border":                "bg_alt2",
    "terminal.background":                "bg",
    "terminal.foreground":                "fg",
    "terminal.selectionBackground":       "bg_alt2",
    "terminalCursor.foreground":          "amber",
    "terminalCursor.background":          "bg",

    # Status bar
    "statusBar.background":               "tab_bg",
    "statusBar.foreground":               "fg_darker",
    "statusBar.border":                   "bg_alt",
    "statusBar.noFolderBackground":       "tab_bg",
    "statusBar.noFolderForeground":       "fg_dark",
    "statusBar.debuggingBackground":      "orange",
    "statusBar.debuggingForeground":      "bg",
    "statusBarItem.hoverBackground":      "bg_alt2",
    "statusBarItem.activeBackground":     "bg_alt2",
    "statusBarItem.remoteBackground":     "amber",
    "statusBarItem.remoteForeground":     "bg",
    "statusBarItem.errorBackground":      "red",
    "statusBarItem.errorForeground":      "bg",
    "statusBarItem.warningBackground":    "yellow",
    "statusBarItem.warningForeground":    "bg",
    "statusBarItem.prominentBackground":  "bg_alt2",
    "statusBarItem.prominentForeground":  "fg_light",

    # Title bar
    "titleBar.activeBackground":          "tab_bg",
    "titleBar.activeForeground":          "fg_alt",
    "titleBar.inactiveBackground":        "tab_bg",
    "titleBar.inactiveForeground":        "fg_dark",
    "titleBar.border":                    "bg_alt",

    # Menus
    "menu.background":                    "bg_alt",
    "menu.foreground":                    "fg",
    "menu.selectionBackground":           "bg_alt2",
    "menu.selectionForeground":           "fg_light",
    "menu.separatorBackground":           "bg_alt2",
    "menu.border":                        "bg_alt2",
    "menubar.selectionBackground":        "bg_alt2",
    "menubar.selectionForeground":        "fg_light",

    # Inputs
    "input.background":                   "bg_alt",
    "input.foreground":                   "fg",
    "input.border":                       "bg_alt2",
    "input.placeholderForeground":        "fg_darker",
    "inputOption.activeBorder":           "amber",
    "inputOption.activeForeground":       "fg_light",
    "inputOption.activeBackground":       ("alpha", "amber", 0.20),
    "inputValidation.errorBackground":    "bg_alt",
    "inputValidation.errorForeground":    "red",
    "inputValidation.errorBorder":        "red",
    "inputValidation.warningBackground":  "bg_alt",
    "inputValidation.warningForeground":  "yellow",
    "inputValidation.warningBorder":      "yellow",
    "inputValidation.infoBackground":     "bg_alt",
    "inputValidation.infoForeground":     "cyan",
    "inputValidation.infoBorder":         "cyan",
    "dropdown.background":                "bg_alt",
    "dropdown.listBackground":            "bg_alt",
    "dropdown.foreground":                "fg",
    "dropdown.border":                    "bg_alt2",

    # Scrollbars — translucent, they sit over live text.
    "scrollbar.shadow":                   ("alpha", "tab_bg", 0.60),
    "scrollbarSlider.background":         ("alpha", "bg_alt2", 0.60),
    "scrollbarSlider.hoverBackground":    ("alpha", "fg_dark", 0.60),
    "scrollbarSlider.activeBackground":   ("alpha", "fg_darker", 0.70),
    "minimapSlider.background":           ("alpha", "bg_alt2", 0.40),
    "minimapSlider.hoverBackground":      ("alpha", "bg_alt2", 0.60),
    "minimapSlider.activeBackground":     ("alpha", "fg_dark", 0.60),
    "minimap.findMatchHighlight":         "yellow",
    "minimap.errorHighlight":             "red",
    "minimap.warningHighlight":           "yellow",

    # Git decorations
    "gitDecoration.addedResourceForeground":       "green",
    "gitDecoration.modifiedResourceForeground":    "yellow",
    "gitDecoration.deletedResourceForeground":     "red",
    "gitDecoration.untrackedResourceForeground":   "cyan",
    "gitDecoration.ignoredResourceForeground":     "fg_dark",
    "gitDecoration.conflictingResourceForeground": "orange",
    "gitDecoration.stageModifiedResourceForeground": "yellow",
    "gitDecoration.stageDeletedResourceForeground":  "red",
    "gitDecoration.submoduleResourceForeground":   "purple",

    # Notifications
    "notifications.background":           "bg_alt",
    "notifications.foreground":           "fg",
    "notifications.border":               "bg_alt2",
    "notificationCenterHeader.background": "bg_alt2",
    "notificationCenterHeader.foreground": "fg_alt",
    "notificationLink.foreground":        "cyan",
    "notificationsErrorIcon.foreground":  "red",
    "notificationsWarningIcon.foreground": "yellow",
    "notificationsInfoIcon.foreground":   "cyan",

    # Breadcrumbs — the leaf segment is the closest analogue to the vim
    # theme's amber Directory.
    "breadcrumb.background":              "bg",
    "breadcrumb.foreground":              "fg_dark",
    "breadcrumb.focusForeground":         "fg",
    "breadcrumb.activeSelectionForeground": "amber",
    "breadcrumbPicker.background":        "bg_alt",

    # Quick input / command palette
    "quickInput.background":              "bg_alt",
    "quickInput.foreground":              "fg",
    "quickInputTitle.background":         "bg_alt2",
    "pickerGroup.border":                 "bg_alt2",
    "pickerGroup.foreground":             "amber",
    "keybindingLabel.background":         "bg_alt2",
    "keybindingLabel.foreground":         "fg",
    "keybindingLabel.border":             "bg_alt2",
    "keybindingLabel.bottomBorder":       "bg_alt2",

    # Debug
    "debugToolBar.background":            "bg_alt",
    "debugToolBar.border":                "bg_alt2",
    "debugIcon.breakpointForeground":     "red",
    "debugIcon.breakpointDisabledForeground": "fg_dark",
    "debugConsoleInputIcon.foreground":   "amber",
    "editor.stackFrameHighlightBackground":        ("mix", "bg", "yellow", 0.18),
    "editor.focusedStackFrameHighlightBackground": ("mix", "bg", "green", 0.18),

    # Testing
    "testing.iconFailed":                 "red",
    "testing.iconErrored":                "orange",
    "testing.iconPassed":                 "green",
    "testing.iconQueued":                 "yellow",
    "testing.iconSkipped":                "fg_dark",

    # Settings
    "settings.headerForeground":          "fg_light",
    "settings.modifiedItemIndicator":     "amber",

    # Symbol icons (outline, suggest widget) — follow the syntax mapping so
    # the completion list reads the same way the buffer does.
    "symbolIcon.classForeground":            "cyan",
    "symbolIcon.interfaceForeground":        "cyan",
    "symbolIcon.structForeground":           "cyan",
    "symbolIcon.enumeratorForeground":       "cyan",
    "symbolIcon.moduleForeground":           "cyan",
    "symbolIcon.namespaceForeground":        "cyan",
    "symbolIcon.typeParameterForeground":    "cyan",
    "symbolIcon.functionForeground":         "green",
    "symbolIcon.methodForeground":           "green",
    "symbolIcon.constructorForeground":      "cyan",
    "symbolIcon.variableForeground":         "fg",
    "symbolIcon.propertyForeground":         "fg",
    "symbolIcon.fieldForeground":            "fg",
    "symbolIcon.constantForeground":         "purple",
    "symbolIcon.enumeratorMemberForeground": "purple",
    "symbolIcon.numberForeground":           "purple",
    "symbolIcon.booleanForeground":          "purple",
    "symbolIcon.keywordForeground":          "red",
    "symbolIcon.operatorForeground":         "red",
    "symbolIcon.stringForeground":           "yellow",
    "symbolIcon.snippetForeground":          "fg_alt",
}

# TextMate scopes, as (name, slot, font_style, [scopes]). Mirrors the group
# assignments in autoload/spectral.vim — the two must agree or a file looks
# different in vim and VS Code.
#
# Two places where the vim theme is internally inconsistent and this map had
# to pick a side:
#   punctuation — per-language groups (jsonBraces, cssBraces) use fg, while
#     the treesitter captures use fg_alt. fg_alt wins: dimmer punctuation is
#     the more deliberate of the two and reads better in dense code.
#   regexp — @string.regex is orange but the richer rubyRegexp* family paints
#     the body cyan with orange escapes and purple char classes. The Ruby
#     treatment wins because TextMate scopes are granular enough to express it.
VSCODE_TOKENS: list[tuple[str, str, str, list[str]]] = [
    ("Comment", "fg_dark", "italic", [
        "comment",
        "punctuation.definition.comment",
        "string.comment",
    ]),
    ("Keyword", "red", "", [
        "keyword",
        "keyword.control",
        "keyword.operator",
        "keyword.other",
        "storage",
        "storage.type",
        "storage.modifier",
        "meta.preprocessor",
        "punctuation.definition.keyword",
    ]),
    ("Tag", "red", "", [
        "entity.name.tag",
        "meta.tag.sgml",
    ]),
    ("String", "yellow", "", [
        "string",
        "string.quoted",
        "punctuation.definition.string",
        "meta.string",
    ]),
    # Ruby symbols carry the amber signature, as they do in the vim theme.
    ("Ruby symbol", "amber", "", [
        "constant.other.symbol",
    ]),
    ("Regular expression", "cyan", "", [
        "string.regexp",
        "punctuation.definition.string.regexp",
    ]),
    ("Regexp character class", "purple", "", [
        "constant.other.character-class.regexp",
        "constant.other.character-class.set.regexp",
    ]),
    ("Escape and special character", "orange", "", [
        "constant.character.escape",
        "constant.other.character-class.escape",
        "punctuation.definition.template-expression",
        "punctuation.section.embedded",
    ]),
    ("Function", "green", "", [
        "entity.name.function",
        "meta.function-call",
        "variable.function",
        "entity.name.method",
        "meta.function-call.generic",
    ]),
    ("Built-in function", "cyan", "", [
        "support.function",
        "support.macro",
    ]),
    ("Type", "cyan", "", [
        "entity.name.type",
        "entity.name.class",
        "entity.name.namespace",
        "entity.other.inherited-class",
        "support.type",
        "support.class",
        "storage.type.annotation",
        "entity.name.scope-resolution",
    ]),
    ("Parameter", "orange", "", [
        "variable.parameter",
        "meta.parameter",
    ]),
    ("Built-in variable", "orange", "", [
        "variable.language",
        "variable.other.global",
        "variable.other.readwrite.instance",
        "variable.other.readwrite.class",
    ]),
    ("Decorator", "orange", "", [
        "meta.decorator",
        "entity.name.function.decorator",
        "punctuation.decorator",
    ]),
    ("Constant", "purple", "", [
        "constant",
        "constant.numeric",
        "constant.language",
        "constant.other",
        "support.constant",
        "variable.other.constant",
        "entity.name.constant",
    ]),
    ("Variable", "fg", "", [
        "variable",
        "variable.other",
        "meta.definition.variable",
    ]),
    ("Property", "fg", "", [
        "variable.other.property",
        "support.variable.property",
        "meta.object-literal.key",
    ]),
    # Data-format keys read as types, matching jsonKeyword/yamlKey/tomlKey.
    ("Data key", "cyan", "", [
        "support.type.property-name.json",
        "support.type.property-name.toml",
        "entity.name.tag.yaml",
    ]),
    ("Attribute name", "green", "", [
        "entity.other.attribute-name",
    ]),
    ("CSS class", "cyan", "", [
        "entity.other.attribute-name.class.css",
        "entity.other.attribute-name.id.css",
    ]),
    ("Punctuation", "fg_alt", "", [
        "punctuation",
        "punctuation.separator",
        "punctuation.terminator",
        "punctuation.definition.tag",
        "meta.brace",
    ]),
    ("Markdown heading 1", "red", "bold", [
        "markup.heading.1",
        "markup.heading.setext.1",
    ]),
    ("Markdown heading 2", "orange", "bold", [
        "markup.heading.2",
        "markup.heading.setext.2",
    ]),
    ("Markdown heading 3", "yellow", "bold", ["markup.heading.3"]),
    ("Markdown heading 4", "green",  "bold", ["markup.heading.4"]),
    ("Markdown heading 5", "cyan",   "bold", ["markup.heading.5"]),
    ("Markdown heading 6", "purple", "bold", ["markup.heading.6"]),
    ("Markdown bold", "orange", "bold", ["markup.bold"]),
    ("Markdown italic", "purple", "italic", ["markup.italic"]),
    ("Markdown strikethrough", "fg_darker", "strikethrough", [
        "markup.strikethrough",
    ]),
    ("Markdown code", "green", "", [
        "markup.inline.raw",
        "markup.fenced_code",
        "markup.raw",
    ]),
    ("Markdown link", "cyan", "underline", [
        "markup.underline.link",
        "string.other.link",
    ]),
    ("Markdown link text", "purple", "", [
        "string.other.link.title",
        "string.other.link.description",
    ]),
    ("Markdown list marker", "red", "", [
        "punctuation.definition.list.begin",
        "markup.list",
    ]),
    ("Markdown quote", "fg_dark", "italic", ["markup.quote"]),
    ("Markdown separator", "fg_darker", "", [
        "meta.separator",
        "punctuation.definition.heading",
    ]),
    ("Diff inserted", "green", "", ["markup.inserted"]),
    ("Diff deleted", "red", "", ["markup.deleted"]),
    ("Diff changed", "yellow", "", ["markup.changed"]),
    ("Invalid", "red", "", ["invalid", "invalid.illegal"]),
    ("Deprecated", "fg_dark", "strikethrough", ["invalid.deprecated"]),
]

# LSP semantic tokens, mirroring the @lsp.type.* / @lsp.mod.* groups.
VSCODE_SEMANTIC: dict[str, tuple[str, str]] = {
    "class":                        ("cyan", ""),
    "interface":                    ("cyan", ""),
    "struct":                       ("cyan", ""),
    "enum":                         ("cyan", ""),
    "type":                         ("cyan", ""),
    "typeParameter":                ("cyan", ""),
    "namespace":                    ("cyan", ""),
    "macro":                        ("cyan", ""),
    "decorator":                    ("orange", ""),
    "enumMember":                   ("purple", ""),
    "function":                     ("green", ""),
    "method":                       ("green", ""),
    "parameter":                    ("orange", ""),
    "property":                     ("fg", ""),
    "variable":                     ("fg", ""),
    "comment":                      ("fg_dark", "italic"),
    "keyword":                      ("red", ""),
    "operator":                     ("red", ""),
    "string":                       ("yellow", ""),
    "number":                       ("purple", ""),
    "*.readonly":                   ("purple", ""),
    "*.deprecated":                 ("fg_dark", "strikethrough"),
    "*.abstract":                   ("cyan", "italic"),
    "*.async":                      ("red", "italic"),
    "variable.defaultLibrary":      ("purple", ""),
    "function.defaultLibrary":      ("cyan", ""),
    "method.defaultLibrary":        ("cyan", ""),
    "variable.global":              ("orange", ""),
}

VSCODE_NAMES = {"dark": "Spectral Dark", "light": "Spectral Light"}


def _font_style(style: str) -> dict:
    # VS Code treats an absent fontStyle as "inherit" and "" as "reset to
    # plain"; emit "" so nothing leaks in from a base grammar.
    return {"fontStyle": style}


def emit_vscode(variant: str, palette: dict, palette_oklch: dict) -> str:
    colors = {key: _vsc(palette, value) for key, value in VSCODE_UI.items()}

    # Integrated terminal ANSI — same mapping and same "bright" derivation the
    # Ghostty and iTerm2 presets use, so a terminal inside VS Code matches one
    # outside it.
    ansi_names = [
        "Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White",
    ]
    base_map = GHOSTTY_ANSI[variant]
    for i, name in enumerate(ansi_names):
        colors[f"terminal.ansi{name}"] = f"#{palette[base_map[i]]['gui']}"
    for i, name in enumerate(ansi_names):
        idx = i + 8
        if idx == 8:
            rgb = palette[base_map[8]]["rgb"]
        elif idx == 15:
            rgb = palette["white"]["rgb"]
        else:
            rgb = oklch_to_rgb(*_bright(palette_oklch, base_map[i], variant))
        colors[f"terminal.ansiBright{name}"] = f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

    token_colors = [
        {
            "name": name,
            "scope": scopes,
            "settings": {
                "foreground": f"#{palette[slot]['gui']}",
                **_font_style(style),
            },
        }
        for name, slot, style, scopes in VSCODE_TOKENS
    ]

    semantic = {
        token: {
            "foreground": f"#{palette[slot]['gui']}",
            **_font_style(style),
        }
        for token, (slot, style) in VSCODE_SEMANTIC.items()
    }

    theme = {
        "$schema": "vscode://schemas/color-theme",
        "name": VSCODE_NAMES[variant],
        "type": variant,
        "semanticHighlighting": True,
        "colors": colors,
        "semanticTokenColors": semantic,
        "tokenColors": token_colors,
    }
    return json.dumps(theme, indent=2) + "\n"


# --------------------------------------------------------------------------
# Marketplace icon emitter
# --------------------------------------------------------------------------

# The icon is a miniature of the theme itself: chunky "code lines" in the
# accent colors with the amber block cursor closing the last line. Drawn from
# the dark palette, so changing a color here changes the listing artwork too.
#
# PNG is written by hand rather than via Pillow to keep the generator runnable
# with a bare python3 — the same reason CI can regenerate without installing
# anything.

ICON_SIZE = 256
ICON_CURSOR = "__cursor__"

# (indent, [(slot, width)]) in a 256-unit design space.
ICON_LINES: list[tuple[int, list[tuple[str, int]]]] = [
    (0,  [("red", 50), ("cyan", 64), ("fg_alt", 40)]),
    (26, [("green", 44), ("yellow", 58), ("purple", 26)]),
    (26, [("purple", 56), ("fg_alt", 34), ("green", 28)]),
    (0,  [("red", 46), ("yellow", 58), (ICON_CURSOR, 26)]),
]

ICON_PAD_L, ICON_TOP, ICON_LINE_H, ICON_BAR_H, ICON_GAP = 38, 62, 38, 15, 13


def _png(width: int, height: int, rows: list[bytearray]) -> bytes:
    """Minimal 8-bit RGBA PNG. Every scanline uses filter type 0."""
    def chunk(tag: bytes, data: bytes) -> bytes:
        body = tag + data
        return (struct.pack(">I", len(data)) + body
                + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF))

    raw = b"".join(b"\x00" + bytes(row) for row in rows)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def _rrect_sdf(px: float, py: float, x0: float, y0: float,
               x1: float, y1: float, r: float) -> float:
    """Signed distance to a rounded rectangle: negative inside, positive out."""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    hw, hh = (x1 - x0) / 2, (y1 - y0) / 2
    qx, qy = abs(px - cx) - (hw - r), abs(py - cy) - (hh - r)
    return math.hypot(max(qx, 0.0), max(qy, 0.0)) + min(max(qx, qy), 0.0) - r


def _coverage(distance: float) -> float:
    """One-pixel analytic antialiasing from a signed distance."""
    return min(1.0, max(0.0, 0.5 - distance))


def _over(dst: list[float], src: list[float], alpha: float) -> list[float]:
    return [dst[i] * (1 - alpha) + src[i] * alpha for i in range(3)]


def emit_icon(palette: dict, size: int = ICON_SIZE) -> bytes:
    unit = size / 256.0
    chan = lambda slot: [c / 255 for c in palette[slot]["rgb"]]
    bg, amber = chan("bg"), chan("amber")

    # Flatten the line layout into drawable bars, in design units.
    bars: list[tuple[list[float], float, float, float, float, float, bool]] = []
    for i, (indent, segments) in enumerate(ICON_LINES):
        x = ICON_PAD_L + indent
        y = ICON_TOP + i * ICON_LINE_H
        for slot, width in segments:
            if slot == ICON_CURSOR:
                # Taller than the text bars and squarer, so it reads as a
                # cursor rather than one more token.
                bars.append((amber, x, y - 6, x + width, y + ICON_BAR_H + 6, 4, True))
            else:
                bars.append((chan(slot), x, y, x + width, y + ICON_BAR_H, 5, False))
            x += width + ICON_GAP

    rows: list[bytearray] = []
    for py in range(size):
        row = bytearray()
        for px in range(size):
            fx, fy = px + 0.5, py + 0.5
            tile = _coverage(_rrect_sdf(
                fx, fy, 3 * unit, 3 * unit,
                size - 3 * unit, size - 3 * unit, 52 * unit,
            ))
            color = list(bg)
            # Scanlines — a hair of CRT texture, invisible as banding.
            if int(py / (2 * unit)) % 2 == 0:
                color = [c * 0.93 for c in color]
            for bar_color, x0, y0, x1, y1, radius, glows in bars:
                d = _rrect_sdf(fx, fy, x0 * unit, y0 * unit,
                               x1 * unit, y1 * unit, radius * unit)
                if glows and d > 0:
                    color = _over(color, amber, math.exp(-d / (15 * unit)) * 0.45)
                hit = _coverage(d)
                if hit > 0:
                    color = _over(color, bar_color, hit)
            row += bytes(int(max(0.0, min(1.0, c)) * 255 + 0.5) for c in color)
            row += bytes([int(tile * 255 + 0.5)])
        rows.append(row)

    return _png(size, size, rows)


# --------------------------------------------------------------------------
# Palette card emitter
# --------------------------------------------------------------------------

# A swatch card per variant, painted on that variant's own background — the
# accents read differently on cream than on near-black, so showing both on a
# neutral white would misrepresent each of them.
#
# The neutral ramp gets equal billing with the accents: the warm-tinted
# greys are the distinctive part of this palette and a table of hex codes
# hides that completely.

CARD_ACCENTS = ["amber", "red", "orange", "yellow", "green", "cyan", "blue", "purple"]
CARD_NEUTRALS = ["bg", "bg_alt", "bg_alt2", "fg_dark", "fg_darker", "fg_alt", "fg", "fg_light"]

CARD_FONT = ("ui-monospace, SFMono-Regular, Menlo, Consolas, "
             "'DejaVu Sans Mono', monospace")
CARD_CHIP_W, CARD_CHIP_H, CARD_GAP, CARD_PAD = 92, 56, 12, 28
CARD_TITLES = {"dark": "Spectral Dark", "light": "Spectral Light"}


def _card_row(palette: dict, slots: list[str], top: float, stroke: str) -> list[str]:
    out = []
    for i, slot in enumerate(slots):
        x = CARD_PAD + i * (CARD_CHIP_W + CARD_GAP)
        out.append(
            f'<rect x="{x}" y="{top}" width="{CARD_CHIP_W}" height="{CARD_CHIP_H}" '
            f'rx="6" fill="#{palette[slot]["gui"].lower()}" stroke="{stroke}"/>'
        )
        mid = x + CARD_CHIP_W / 2
        out.append(
            f'<text x="{mid:.0f}" y="{top + CARD_CHIP_H + 20:.0f}" text-anchor="middle" '
            f'font-size="11" fill="{{name}}">{slot}</text>'
        )
        out.append(
            f'<text x="{mid:.0f}" y="{top + CARD_CHIP_H + 35:.0f}" text-anchor="middle" '
            f'font-size="10" fill="{{hex}}">#{palette[slot]["gui"].upper()}</text>'
        )
    return out


def emit_palette_card(variant: str, palette: dict) -> str:
    hexes = {k: f"#{v['gui'].lower()}" for k, v in palette.items()}
    width = CARD_PAD * 2 + 8 * CARD_CHIP_W + 7 * CARD_GAP
    # Neutrals sit clear of the accent hex labels, which run to top + 91.
    accents_top, neutrals_top = 86.0, 232.0
    height = neutrals_top + CARD_CHIP_H + 46

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height:.0f}" '
        f'viewBox="0 0 {width} {height:.0f}" font-family="{CARD_FONT}">',
        f'<rect width="{width}" height="{height:.0f}" rx="10" fill="{hexes["bg"]}" '
        f'stroke="{hexes["bg_alt2"]}"/>',
        f'<text x="{CARD_PAD}" y="42" font-size="17" fill="{hexes["fg"]}">'
        f'{CARD_TITLES[variant]}</text>',
    ]
    for label, top in (("Accents", accents_top), ("Neutrals", neutrals_top)):
        parts.append(
            f'<text x="{CARD_PAD}" y="{top - 14:.0f}" font-size="10" '
            f'letter-spacing="1.5" fill="{hexes["fg_dark"]}">{label.upper()}</text>'
        )
    for slots, top in ((CARD_ACCENTS, accents_top), (CARD_NEUTRALS, neutrals_top)):
        for line in _card_row(palette, slots, top, hexes["bg_alt2"]):
            parts.append(line.format(name=hexes["fg_alt"], hex=hexes["fg_darker"]))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

ITERM_NAMES = {"dark": "Spectral Dark", "light": "Spectral Light"}


def main() -> None:
    resolved: dict[str, dict] = {}
    for variant, spec in PALETTES.items():
        palette = resolve(spec)
        resolved[variant] = palette

        # Vim
        (REPO / "colors" / f"spectral-{variant}.vim").write_text(emit_vim(variant, palette))

        # Ghostty
        (REPO / "ghostty" / f"spectral-{variant}").write_text(emit_ghostty(variant, palette, spec))

        # iTerm2
        with (REPO / "iterm2" / f"{ITERM_NAMES[variant]}.itermcolors").open("wb") as f:
            plistlib.dump(emit_itermcolors(variant, palette, spec), f)

        # Mattermost
        (REPO / "mattermost" / f"spectral-{variant}.json").write_text(emit_mattermost(variant, palette))

        # VS Code
        vscode = REPO / "vscode" / "themes"
        vscode.mkdir(parents=True, exist_ok=True)
        (vscode / f"spectral-{variant}.json").write_text(emit_vscode(variant, palette, spec))

        print(f"wrote {variant} variant")

        # Palette card for the README
        cards = REPO / "screenshots"
        cards.mkdir(exist_ok=True)
        (cards / f"palette-{variant}.svg").write_text(emit_palette_card(variant, palette))

    # Marketplace icon — drawn from the dark palette only.
    (REPO / "vscode" / "icon.png").write_bytes(emit_icon(resolved["dark"]))
    print("wrote vscode icon")

    # lightline — one theme that branches on &background across both variants.
    lightline = REPO / "autoload" / "lightline" / "colorscheme" / "spectral.vim"
    lightline.parent.mkdir(parents=True, exist_ok=True)
    lightline.write_text(emit_lightline(resolved))
    print("wrote lightline theme")


if __name__ == "__main__":
    main()

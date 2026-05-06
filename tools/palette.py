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

After regenerating, run iterm2/sync.py to push the iTerm2 presets to a
target plist.

OKLCH triples are (L, C, H):
  L  lightness, 0=black 1=white. Perceptually uniform.
  C  chroma, 0=gray; the sRGB gamut peaks around 0.3 in mid lightness, less
     near black or white. Out-of-gamut chroma is reduced by bisection (L and
     H are preserved; the color stays the same hue but desaturates as needed).
  H  hue in degrees: 0=pink/red, 30=orange, 90=yellow-green, 150=green,
     210=cyan, 270=blue, 330=magenta.
"""
from __future__ import annotations

import math
import plistlib
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Warm-tinted neutrals — yellow-orange hue at very low chroma so the bg/fg
# ramp echoes the amber signature without looking colored.
NEUTRAL_HUE = 85.0

PALETTES: dict[str, dict[str, tuple[float, float, float]]] = {
    "dark": {
        # Backgrounds — warm dark. Chroma is set high enough to read as
        # "warm gray" in a bare terminal context, where there's no syntax
        # color to reinforce the tint by association.
        "bg":        (0.21, 0.015, NEUTRAL_HUE),
        "bg_alt":    (0.27, 0.018, NEUTRAL_HUE),
        "bg_alt2":   (0.36, 0.022, NEUTRAL_HUE),
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
        "tab_bg":    (0.12, 0.012, NEUTRAL_HUE),
        # Signature — overrides Directory/netrwDir/rubySymbol
        "amber":     (0.80, 0.16, 75),
    },
    "light": {
        "bg":        (0.97, 0.030, NEUTRAL_HUE),
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
        "yellow":    (0.55, 0.13, 85),
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
# Main
# --------------------------------------------------------------------------

ITERM_NAMES = {"dark": "Spectral Dark", "light": "Spectral Light"}


def main() -> None:
    for variant, spec in PALETTES.items():
        palette = resolve(spec)

        # Vim
        (REPO / "colors" / f"spectral-{variant}.vim").write_text(emit_vim(variant, palette))

        # Ghostty
        (REPO / "ghostty" / f"spectral-{variant}").write_text(emit_ghostty(variant, palette, spec))

        # iTerm2
        with (REPO / "iterm2" / f"{ITERM_NAMES[variant]}.itermcolors").open("wb") as f:
            plistlib.dump(emit_itermcolors(variant, palette, spec), f)

        print(f"wrote {variant} variant")


if __name__ == "__main__":
    main()

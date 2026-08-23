#!/usr/bin/env python3
"""
Spectral screenshot generator.

Renders the sample files in tools/samples/ through a real headless Vim using
the actual colorscheme, and emits SVG "screenshots" into screenshots/.

The colors are not reproduced from tools/palette.py — they come out of Vim's
own :TOhtml, which reports whatever the loaded colorscheme actually resolved
each syntax group to. A screenshot can therefore never flatter the theme: if
the colorscheme is broken, the screenshot is broken in exactly the same way.

Usage:
  python3 tools/screenshots.py            # every sample, both variants
  python3 tools/screenshots.py billing    # just the samples matching a stem

Requires vim (any 8.2+) on PATH. Output is deliberately NOT part of the CI
drift check: :TOhtml markup shifts between Vim versions, so regenerating on a
different Vim would produce spurious diffs. Regenerate by hand when the
palette changes.
"""
from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import palette  # noqa: E402  (needs the path above)

REPO = Path(__file__).resolve().parent.parent
SAMPLES = REPO / "tools" / "samples"
OUT = REPO / "screenshots"

VARIANTS = ("dark", "light")

# Type metrics. Advance is only used to size the canvas — glyphs are laid out
# by the renderer's own metrics, so a font whose advance differs slightly still
# lines up.
FONT = palette.MONO_STACK
FONT_SIZE = 14.0
ADVANCE = FONT_SIZE * 0.60
LINE_H = FONT_SIZE * 1.5
PAD_X, PAD_Y = 18.0, 14.0
TITLEBAR = 30.0
RADIUS = 8.0

# Ordering here is load-bearing, twice over:
#   plugin/sorbet.vim is sourced *after* `syntax on` so its Syntax autocmd is
#   registered after Vim's own; registered first, syntax/ruby.vim's `syn clear`
#   runs last and wipes the sig-block matches.
#   The file is opened by :edit at the end rather than passed as a Vim
#   argument, so FileType and Syntax fire against a fully configured session —
#   the same order a real editing session produces.
VIM_SCRIPT = """
set rtp^={repo}
runtime! plugin/tohtml.vim
filetype plugin indent on
syntax on
runtime! plugin/sorbet.vim
set termguicolors
set background={variant}
colorscheme spectral-{variant}
let g:html_use_css = 1
let g:html_number_lines = 1
let g:html_line_ids = 0
let g:html_no_progress = 1
let g:html_prevent_copy = ""
let g:html_no_foldcolumn = 1
edit {source}
TOhtml
execute 'write! ' . '{out}'
qall!
"""


def run_vim(source: Path, variant: str) -> str:
    """Drive Vim headlessly and return the :TOhtml output."""
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "shot.vim"
        out = Path(tmp) / "out.html"
        script.write_text(
            VIM_SCRIPT.format(repo=REPO, variant=variant, out=out, source=source)
        )
        proc = subprocess.run(
            ["vim", "-N", "-u", "NONE", "-i", "NONE", "--not-a-term",
             "-S", str(script)],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        if not out.exists():
            raise SystemExit(
                f"vim produced no output for {source.name} ({variant}):\n"
                f"{proc.stderr.strip()}"
            )
        return out.read_text()


STYLE_RE = re.compile(r"^\.(\w+)\s*\{([^}]*)\}", re.M)


def parse_styles(doc: str) -> tuple[dict[str, dict], str, str]:
    """Class name -> {fill, italic, bold}, plus the default fg/bg."""
    styles: dict[str, dict] = {}
    for name, body in STYLE_RE.findall(doc):
        color = re.search(r"(?<!background-)color:\s*(#[0-9a-fA-F]{6})", body)
        styles[name] = {
            "fill": color.group(1) if color else None,
            "italic": "font-style: italic" in body,
            "bold": "font-weight: bold" in body,
        }
    body_rule = re.search(r"^body\s*\{([^}]*)\}", doc, re.M)
    rule = body_rule.group(1) if body_rule else ""
    fg = re.search(r"(?<!background-)color:\s*(#[0-9a-fA-F]{6})", rule)
    bg = re.search(r"background-color:\s*(#[0-9a-fA-F]{6})", rule)
    return styles, (fg.group(1) if fg else "#000000"), (bg.group(1) if bg else "#ffffff")


class PreExtractor(HTMLParser):
    """Collect (text, class) runs from the <pre> block, split into lines."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_pre = False
        self.stack: list[str | None] = []
        self.lines: list[list[tuple[str, str | None]]] = [[]]

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "pre":
            self.in_pre = True
        elif tag == "span" and self.in_pre:
            self.stack.append(attrs.get("class"))
        elif tag == "br" and self.in_pre:
            self.lines.append([])

    def handle_endtag(self, tag):
        if tag == "pre":
            self.in_pre = False
        elif tag == "span" and self.in_pre and self.stack:
            self.stack.pop()

    def handle_data(self, data):
        if not self.in_pre:
            return
        cls = self.stack[-1] if self.stack else None
        for i, part in enumerate(data.split("\n")):
            if i:
                self.lines.append([])
            if part:
                self.lines[-1].append((part, cls))


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def to_svg(lines, styles, fg, bg, title, accents) -> str:
    while lines and not lines[-1]:
        lines.pop()
    cols = max((sum(len(t) for t, _ in ln) for ln in lines), default = 0)
    width = PAD_X * 2 + cols * ADVANCE
    height = TITLEBAR + PAD_Y * 2 + len(lines) * LINE_H

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" '
        f'height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}" '
        f'font-family="{FONT}" font-size="{FONT_SIZE}">',
        f'<rect width="{width:.0f}" height="{height:.0f}" rx="{RADIUS}" fill="{bg}"/>',
        # Title bar: the three dots use the theme's own red/yellow/green.
        f'<rect width="{width:.0f}" height="{TITLEBAR}" rx="{RADIUS}" fill="{accents["bar"]}"/>',
        f'<rect y="{RADIUS}" width="{width:.0f}" height="{TITLEBAR - RADIUS}" '
        f'fill="{accents["bar"]}"/>',
    ]
    for i, dot in enumerate(("red", "yellow", "green")):
        parts.append(
            f'<circle cx="{16 + i * 15:.0f}" cy="{TITLEBAR / 2:.0f}" r="4.5" '
            f'fill="{accents[dot]}"/>'
        )
    parts.append(
        f'<text x="{width / 2:.0f}" y="{TITLEBAR / 2 + 4:.0f}" text-anchor="middle" '
        f'fill="{accents["title"]}" font-size="11">{esc(title)}</text>'
    )

    for row, runs in enumerate(lines):
        y = TITLEBAR + PAD_Y + (row + 1) * LINE_H - LINE_H * 0.25
        spans = []
        for text, cls in runs:
            style = styles.get(cls or "", {})
            attrs = [f'fill="{style.get("fill") or fg}"']
            if style.get("italic"):
                attrs.append('font-style="italic"')
            if style.get("bold"):
                attrs.append('font-weight="bold"')
            spans.append(f'<tspan {" ".join(attrs)}>{esc(text)}</tspan>')
        parts.append(
            f'<text x="{PAD_X:.0f}" y="{y:.1f}" xml:space="preserve">'
            + "".join(spans) + "</text>"
        )

    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def accents_for(variant: str) -> dict[str, str]:
    pal = palette.resolve(palette.PALETTES[variant])
    # Lowercase to match :TOhtml's own output, so one file does not
    # mix hex casing.
    hexes = {k: f"#{v['gui'].lower()}" for k, v in pal.items()}
    return {
        "bar": hexes["bg_alt"],
        "title": hexes["fg_darker"],
        "red": hexes["red"],
        "yellow": hexes["yellow"],
        "green": hexes["green"],
    }


def main() -> None:
    wanted = sys.argv[1:]
    sources = sorted(p for p in SAMPLES.iterdir() if p.is_file())
    if wanted:
        sources = [p for p in sources if any(w in p.stem for w in wanted)]
    if not sources:
        raise SystemExit("no matching samples in tools/samples/")

    OUT.mkdir(exist_ok=True)
    for source in sources:
        for variant in VARIANTS:
            doc = run_vim(source, variant)
            styles, fg, bg = parse_styles(doc)
            extractor = PreExtractor()
            extractor.feed(doc)
            svg = to_svg(extractor.lines, styles, fg, bg,
                         source.name, accents_for(variant))
            dest = OUT / f"{source.stem}-{variant}.svg"
            dest.write_text(svg)
            print(f"wrote {dest.relative_to(REPO)}  "
                  f"({len([l for l in extractor.lines if l])} lines, "
                  f"{len(styles)} groups)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Invariants for the generated theme files.

These assert structural properties that a typo in the mapping tables would
break — valid hex everywhere, no scope defined twice, foregrounds that stay
distinguishable from their background. They deliberately do not assert
individual color assignments; that would only restate the mapping dicts.

Run: python3 -m unittest discover -s tools
"""
from __future__ import annotations

import json
import re
import unittest

import palette

HEX = re.compile(r"^#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?$")

VARIANTS = ("dark", "light")


def resolved(variant: str) -> dict:
    return palette.resolve(palette.PALETTES[variant])


def _luminance(hex_color: str) -> float:
    """WCAG relative luminance. Alpha, if present, is ignored."""
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
           for c in (r, g, b)]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(fg: str, bg: str) -> float:
    a, b = _luminance(fg), _luminance(bg)
    lo, hi = min(a, b), max(a, b)
    return (hi + 0.05) / (lo + 0.05)


class VSCodeTheme(unittest.TestCase):
    def theme(self, variant: str) -> dict:
        spec = palette.PALETTES[variant]
        return json.loads(palette.emit_vscode(variant, palette.resolve(spec), spec))

    def test_has_required_top_level_keys(self):
        for variant in VARIANTS:
            with self.subTest(variant=variant):
                theme = self.theme(variant)
                self.assertIn("name", theme)
                self.assertIn("colors", theme)
                self.assertIn("tokenColors", theme)
                self.assertEqual(theme["type"], variant)

    def test_every_color_is_valid_hex(self):
        for variant in VARIANTS:
            theme = self.theme(variant)
            for key, value in theme["colors"].items():
                with self.subTest(variant=variant, key=key):
                    self.assertRegex(value, HEX)
            for entry in theme["tokenColors"]:
                with self.subTest(variant=variant, token=entry["name"]):
                    self.assertRegex(entry["settings"]["foreground"], HEX)
            for token, settings in theme["semanticTokenColors"].items():
                with self.subTest(variant=variant, semantic=token):
                    self.assertRegex(settings["foreground"], HEX)

    def test_no_scope_is_defined_twice(self):
        # Two entries claiming the same scope is always a mistake: VS Code
        # applies the last one and the earlier assignment vanishes silently.
        theme = self.theme("dark")
        seen: dict[str, str] = {}
        for entry in theme["tokenColors"]:
            for scope in entry["scope"]:
                if scope in seen:
                    self.fail(
                        f"scope {scope!r} defined by both {seen[scope]!r} "
                        f"and {entry['name']!r}"
                    )
                seen[scope] = entry["name"]

    def test_token_colors_stay_legible_on_the_editor_background(self):
        # Not a WCAG gate — comments are dim on purpose. This is the floor
        # that catches a slot mapped so close to the background that the
        # token effectively disappears.
        for variant in VARIANTS:
            theme = self.theme(variant)
            bg = theme["colors"]["editor.background"]
            for entry in theme["tokenColors"]:
                fg = entry["settings"]["foreground"]
                with self.subTest(variant=variant, token=entry["name"]):
                    self.assertGreaterEqual(contrast(fg, bg), 2.0)

    def test_body_text_is_high_contrast(self):
        for variant in VARIANTS:
            with self.subTest(variant=variant):
                theme = self.theme(variant)
                ratio = contrast(
                    theme["colors"]["editor.foreground"],
                    theme["colors"]["editor.background"],
                )
                self.assertGreaterEqual(ratio, 7.0)


if __name__ == "__main__":
    unittest.main()

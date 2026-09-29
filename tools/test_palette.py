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
import plistlib
import re
import struct
import tomllib
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


class ZedTheme(unittest.TestCase):
    # Zed takes #RRGGBBAA and nothing else — a six-digit color is dropped.
    HEX8 = re.compile(r"^#[0-9A-Fa-f]{8}$")

    def family(self) -> dict:
        return json.loads(palette.emit_zed(
            {v: resolved(v) for v in VARIANTS}, palette.PALETTES,
        ))

    def styles(self):
        for theme in self.family()["themes"]:
            yield theme["name"], theme["style"]

    def test_is_a_theme_family_with_both_variants(self):
        family = self.family()
        self.assertEqual(family["name"], "Spectral")
        self.assertIn("author", family)
        self.assertEqual(
            [(t["name"], t["appearance"]) for t in family["themes"]],
            [("Spectral Dark", "dark"), ("Spectral Light", "light")],
        )

    def test_every_color_is_valid_hex(self):
        for name, style in self.styles():
            for key, value in style.items():
                if key in ("players", "accents", "syntax"):
                    continue
                with self.subTest(theme=name, key=key):
                    # The one style value that is a keyword, not a color.
                    if key == "background.appearance":
                        self.assertEqual(value, "opaque")
                    else:
                        self.assertRegex(value, self.HEX8)
            for i, player in enumerate(style["players"]):
                for key, value in player.items():
                    with self.subTest(theme=name, player=i, key=key):
                        self.assertRegex(value, self.HEX8)
            for i, accent in enumerate(style["accents"]):
                with self.subTest(theme=name, accent=i):
                    self.assertRegex(accent, self.HEX8)
            for capture, settings in style["syntax"].items():
                with self.subTest(theme=name, capture=capture):
                    self.assertRegex(settings["color"], self.HEX8)

    def test_no_style_key_is_written_twice(self):
        # ZED_UI, the status triples and the terminal palette all land in one
        # flat dict, so an overlap between them would silently drop whichever
        # emitter ran first.
        status = {
            key
            for name in palette.ZED_STATUS
            for key in (name, f"{name}.background", f"{name}.border")
        }
        terminal = {
            f"terminal.ansi.{prefix}{name}"
            for name in palette.ZED_ANSI_NAMES
            for prefix in ("", "bright_", "dim_")
        }
        for a, b in ((palette.ZED_UI.keys(), status),
                     (palette.ZED_UI.keys(), terminal),
                     (status, terminal)):
            self.assertEqual(set(a) & set(b), set())

    def test_terminal_palette_is_complete(self):
        for name, style in self.styles():
            for ansi in palette.ZED_ANSI_NAMES:
                for prefix in ("", "bright_", "dim_"):
                    with self.subTest(theme=name, color=prefix + ansi):
                        self.assertIn(f"terminal.ansi.{prefix}{ansi}", style)

    def test_every_player_has_a_full_set_of_colors(self):
        for name, style in self.styles():
            self.assertEqual(len(style["players"]), 8)
            self.assertEqual(len(style["accents"]), 8)
            for i, player in enumerate(style["players"]):
                with self.subTest(theme=name, player=i):
                    self.assertEqual(
                        set(player), {"cursor", "background", "selection"},
                    )

    def test_syntax_colors_stay_legible_on_the_editor_background(self):
        for name, style in self.styles():
            bg = style["editor.background"]
            for capture, settings in style["syntax"].items():
                with self.subTest(theme=name, capture=capture):
                    self.assertGreaterEqual(
                        contrast(settings["color"][:7], bg[:7]), 2.0,
                    )


class TuicrTheme(unittest.TestCase):
    # Every key tuicr 0.27 refuses to load a local theme without
    # (require_local_theme_color in src/theme/mod.rs). It takes #RRGGBB only.
    REQUIRED = (
        "panel_bg", "pending", "bg_highlight", "fg_primary", "fg_secondary",
        "fg_dim", "diff_add", "diff_add_bg", "diff_del", "diff_del_bg",
        "diff_context", "diff_hunk_header", "expanded_context_fg",
        "syntax_add_bg", "syntax_del_bg", "file_added", "file_modified",
        "file_deleted", "file_renamed", "reviewed", "comment_note",
        "comment_suggestion", "comment_issue", "comment_praise",
        "border_focused", "border_unfocused", "status_bar_bg", "cursor_color",
        "cursor_line_bg", "branch_name", "help_indicator", "message_info_fg",
        "message_info_bg", "message_warning_fg", "message_warning_bg",
        "message_error_fg", "message_error_bg", "update_badge_fg",
        "update_badge_bg", "mode_fg", "mode_bg",
    )
    HEX6 = re.compile(r"^#[0-9A-Fa-f]{6}$")

    def theme(self, variant: str) -> dict:
        return tomllib.loads(palette.emit_tuicr(variant, resolved(variant)))

    def test_defines_every_key_tuicr_requires_as_rrggbb(self):
        for variant in VARIANTS:
            theme = self.theme(variant)
            for key in self.REQUIRED:
                with self.subTest(variant=variant, key=key):
                    self.assertRegex(theme.get(key, ""), self.HEX6)

    def test_writes_no_key_tuicr_would_warn_about_on_every_start(self):
        for variant in VARIANTS:
            with self.subTest(variant=variant):
                unknown = set(self.theme(variant)) - set(self.REQUIRED) - {"syntax_theme"}
                self.assertEqual(unknown, set())

    def test_text_stays_legible_on_what_it_is_drawn_over(self):
        # Pairs tuicr paints one on the other. Badges and the mode block get
        # the WCAG large-text floor; they're short labels, not reading text.
        pairs = {
            ("fg_primary", "panel_bg"): 7.0,
            ("diff_context", "syntax_add_bg"): 4.5,
            ("diff_context", "syntax_del_bg"): 4.5,
            ("diff_add", "diff_add_bg"): 3.0,
            ("diff_del", "diff_del_bg"): 3.0,
            ("message_info_fg", "message_info_bg"): 3.0,
            ("message_warning_fg", "message_warning_bg"): 3.0,
            ("message_error_fg", "message_error_bg"): 3.0,
            ("update_badge_fg", "update_badge_bg"): 3.0,
            ("mode_fg", "mode_bg"): 3.0,
        }
        for variant in VARIANTS:
            theme = self.theme(variant)
            for (fg, bg), floor in pairs.items():
                with self.subTest(variant=variant, fg=fg, bg=bg):
                    self.assertGreaterEqual(contrast(theme[fg], theme[bg]), floor)

    def test_highlights_syntax_with_its_own_textmate_theme(self):
        for variant in VARIANTS:
            with self.subTest(variant=variant):
                theme = self.theme(variant)
                self.assertEqual(theme["syntax_theme"], f"spectral-{variant}.tmTheme")
                tm = plistlib.loads(palette.emit_tmtheme(variant, resolved(variant)))
                base, *rules = tm["settings"]
                self.assertEqual(base["settings"]["background"], theme["panel_bg"])
                self.assertTrue(rules)
                for rule in rules:
                    fg = rule["settings"]["foreground"]
                    with self.subTest(variant=variant, rule=rule["name"]):
                        self.assertRegex(fg, self.HEX6)
                        self.assertGreaterEqual(contrast(fg, theme["panel_bg"]), 2.0)


class MarketplaceIcon(unittest.TestCase):
    def test_is_a_valid_256px_rgba_png(self):
        data = palette.emit_icon(resolved("dark"))
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(data[12:16], b"IHDR")
        width, height, depth, color_type = struct.unpack(">IIBB", data[16:26])
        self.assertEqual((width, height), (256, 256))
        self.assertEqual(depth, 8)
        self.assertEqual(color_type, 6)  # RGBA

    def test_icon_is_drawn_from_the_palette(self):
        # A static blob would survive a palette change; this must not.
        spec = dict(palette.PALETTES["dark"])
        spec["amber"] = (0.80, 0.16, 200)
        self.assertNotEqual(
            palette.emit_icon(resolved("dark")),
            palette.emit_icon(palette.resolve(spec)),
        )


class PaletteCard(unittest.TestCase):
    def test_every_slot_it_claims_is_drawn_and_labelled(self):
        for variant in VARIANTS:
            pal = resolved(variant)
            card = palette.emit_palette_card(variant, pal)
            for slot in palette.CARD_ACCENTS + palette.CARD_NEUTRALS:
                with self.subTest(variant=variant, slot=slot):
                    self.assertIn(f'fill="#{pal[slot]["gui"].lower()}"', card)
                    self.assertIn(f'#{pal[slot]["gui"].upper()}', card)

    def test_draws_one_swatch_per_slot(self):
        # Background rect plus one chip each; a dropped row would still emit
        # valid SVG, just a card that quietly understates the palette.
        expected = len(palette.CARD_ACCENTS) + len(palette.CARD_NEUTRALS) + 1
        for variant in VARIANTS:
            with self.subTest(variant=variant):
                card = palette.emit_palette_card(variant, resolved(variant))
                self.assertEqual(card.count("<rect"), expected)


if __name__ == "__main__":
    unittest.main()

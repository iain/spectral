#!/usr/bin/env python3
"""Behaviour of the syntax rules in plugin/, checked against a real Vim.

These run Vim headless with only this repository and Vim's own runtime on
the runtimepath, open a sample buffer, and read back the syntax stack at
given positions.

Run: python3 -m unittest discover -s tools
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from palette import PALETTES, resolve

REPO = Path(__file__).resolve().parent.parent
VIM = shutil.which("vim")
NVIM = shutil.which("nvim")


def syntax_at(extension: str, text: str, positions: list[tuple[int, int]]) -> list[list[str]]:
    """Return the syntax group names stacked at each (line, col), 1-based."""
    with tempfile.TemporaryDirectory() as tmp:
        sample = Path(tmp) / f"sample.{extension}"
        sample.write_text(text)
        result = Path(tmp) / "result.json"
        probe = (
            "call writefile([json_encode(map(" + json.dumps(positions) + ","
            " 'map(synstack(v:val[0], v:val[1]), \"synIDattr(v:val, ''name'')\")'))], "
            + json.dumps(str(result)) + ")"
        )
        subprocess.run(
            [
                VIM, "-N", "-u", "NONE", "-i", "NONE", "-es",
                "-c", f"set rtp^={REPO}",
                "-c", "filetype on",
                "-c", "syntax on",
                "-c", "runtime! plugin/*.vim",
                "-c", f"edit {sample}",
                "-c", probe,
                "-c", "qa!",
            ],
            stdin=subprocess.DEVNULL,
            check=True,
            timeout=30,
        )
        return json.loads(result.read_text())


def captures_at(extension: str, text: str, positions: list[tuple[int, int]]) -> list[list[str]]:
    """Return the treesitter captures at each (line, col), 1-based, in Neovim."""
    with tempfile.TemporaryDirectory() as tmp:
        sample = Path(tmp) / f"sample.{extension}"
        sample.write_text(text)
        result = Path(tmp) / "result.json"
        probe = (
            "lua vim.treesitter.start(); vim.treesitter.get_parser():parse(true); "
            "local out = {}; "
            f"for _, p in ipairs(vim.json.decode('{json.dumps(positions)}')) do "
            "  local caps = vim.inspect_pos(0, p[1] - 1, p[2] - 1).treesitter; "
            "  table.insert(out, vim.tbl_map(function(c) return c.capture end, caps)) "
            "end; "
            f"vim.fn.writefile({{vim.json.encode(out)}}, '{result}')"
        )
        subprocess.run(
            [
                NVIM, "--headless", "--clean",
                "--cmd", f"set rtp^={REPO}",
                "-c", f"edit {sample}",
                "-c", probe,
                "-c", "qa!",
            ],
            stdin=subprocess.DEVNULL,
            check=True,
            timeout=30,
        )
        return json.loads(result.read_text())


def highlight_of(colorscheme: str, groups: list[str]) -> list[dict[str, str]]:
    """Return the GUI foreground and background each group resolves to."""
    with tempfile.TemporaryDirectory() as tmp:
        result = Path(tmp) / "result.json"
        probe = (
            "call writefile([json_encode(map(" + json.dumps(groups) + ","
            " '{\"fg\": synIDattr(synIDtrans(hlID(v:val)), \"fg#\", \"gui\"),"
            " \"bg\": synIDattr(synIDtrans(hlID(v:val)), \"bg#\", \"gui\")}'))], "
            + json.dumps(str(result)) + ")"
        )
        subprocess.run(
            [
                VIM, "-N", "-u", "NONE", "-i", "NONE", "-es",
                "-c", f"set rtp^={REPO}",
                "-c", "set termguicolors",
                "-c", f"colorscheme {colorscheme}",
                "-c", probe,
                "-c", "qa!",
            ],
            stdin=subprocess.DEVNULL,
            check=True,
            timeout=30,
        )
        return json.loads(result.read_text())


@unittest.skipUnless(VIM, "vim is not installed")
class MarkdownHeadingOne(unittest.TestCase):
    # Amber on dim amber, as on an amber CRT, rather than inverted: a block of
    # full amber clashes with the dim # that polyglot leaves outside it.
    def test_is_amber_on_a_dim_amber_background(self):
        for variant in ("dark", "light"):
            colors = resolve(PALETTES[variant])
            amber = "#" + colors["amber"]["gui"].lower()
            amber_bg = "#" + colors["amber_bg"]["gui"].lower()
            # htmlH1 is what vim-polyglot draws a Markdown H1 with.
            groups = ["markdownH1", "markdownH1Delimiter", "htmlH1"]
            for group, hl in zip(groups, highlight_of(f"spectral-{variant}", groups)):
                with self.subTest(variant=variant, group=group):
                    self.assertEqual(hl["fg"].lower(), amber)
                    self.assertEqual(hl["bg"].lower(), amber_bg)


@unittest.skipUnless(NVIM, "nvim is not installed")
class NeovimMarkdownLinks(unittest.TestCase):
    SAMPLE = "\n".join([
        "See [the docs](https://example.com/docs) or <https://example.org>.",
        "",
        "A [reference][docs] link.",
        "",
        "[docs]: https://example.com/docs",
    ]) + "\n"

    def stacks(self, *positions):
        return captures_at("md", self.SAMPLE, list(positions))

    def test_link_destinations_have_their_own_capture(self):
        inline, definition = self.stacks((1, 16), (5, 9))
        self.assertIn("markup.link.url.destination", inline)
        self.assertIn("markup.link.url.destination", definition)

    def test_autolinks_keep_the_plain_url_capture(self):
        (autolink,) = self.stacks((1, 46))
        self.assertIn("markup.link.url", autolink)
        self.assertNotIn("markup.link.url.destination", autolink)

    def test_reference_labels_have_their_own_capture(self):
        text, label, definition = self.stacks((3, 4), (3, 16), (5, 2))
        self.assertNotIn("markup.link.label.reference", text)
        self.assertIn("markup.link.label.reference", label)
        self.assertIn("markup.link.label.reference", definition)


@unittest.skipUnless(VIM, "vim is not installed")
class GoLiteralKeys(unittest.TestCase):
    SAMPLE = "\n".join([
        "package main",                      # 1
        "",                                  # 2
        "func main() {",                     # 3
        '\tu := User{Name: "x", Age: 3}',    # 4
        "\tv := User{",                      # 5
        '\t\tName: "y",',                    # 6
        "\t}",                               # 7
        "Loop:",                             # 8
        "\tswitch u.Age {",                  # 9
        "\tcase limit: return",              # 10
        "\t}",                               # 11
        "\t_ = s[lo:hi]",                    # 12
        "}",                                 # 13
    ]) + "\n"

    def stacks(self, *positions):
        return syntax_at("go", self.SAMPLE, list(positions))

    def test_keys_in_a_one_line_composite_literal(self):
        name, age = self.stacks((4, 12), (4, 23))
        self.assertIn("goLiteralKey", name)
        self.assertIn("goLiteralKey", age)

    def test_keys_on_their_own_line(self):
        (name,) = self.stacks((6, 3))
        self.assertIn("goLiteralKey", name)

    def test_labels_case_clauses_and_slices_are_not_keys(self):
        for stack in self.stacks((8, 1), (10, 7), (12, 8)):
            self.assertNotIn("goLiteralKey", stack)


@unittest.skipUnless(VIM, "vim is not installed")
class CommentUrls(unittest.TestCase):
    def test_url_in_a_comment_is_marked(self):
        (stack,) = syntax_at("rb", "# see https://example.com/docs\n", [(1, 7)])
        self.assertIn("spectralCommentUrl", stack)

    def test_url_ends_before_closing_punctuation(self):
        text = "// (see https://example.com/a).\n"
        last, paren = syntax_at("go", text, [(1, 29), (1, 30)])
        self.assertIn("spectralCommentUrl", last)
        self.assertNotIn("spectralCommentUrl", paren)

    def test_url_outside_a_comment_is_left_alone(self):
        (stack,) = syntax_at("rb", 'url = "https://example.com"\n', [(1, 8)])
        self.assertNotIn("spectralCommentUrl", stack)


if __name__ == "__main__":
    unittest.main()

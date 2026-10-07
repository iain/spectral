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

REPO = Path(__file__).resolve().parent.parent
VIM = shutil.which("vim")


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


if __name__ == "__main__":
    unittest.main()

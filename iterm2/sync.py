#!/usr/bin/env python3
"""
Apply the Spectral / Spectral Light .itermcolors presets to an iTerm2 plist.

iTerm2 has no live link between a preset file and a profile — selecting a
preset in the UI just copies the colors into the profile dict. This script
does the same thing from the command line so the .itermcolors files in this
repo can be the source of truth for a dotfiles-managed plist.

Usage:
    iterm2/sync.py <path-to-com.googlecode.iterm2.plist> [profile-name]

The default profile name is "Default". The script writes the dark preset to
both the unsuffixed key (`Background Color`) and the `(Dark)` variant, and
the light preset to the `(Light)` variant — so iTerm2's automatic dark/light
mode switching keeps working.
"""
from __future__ import annotations

import plistlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DARK_PRESET  = HERE / "Spectral Dark.itermcolors"
LIGHT_PRESET = HERE / "Spectral Light.itermcolors"


def load_preset(path: Path) -> dict:
    with path.open("rb") as f:
        return plistlib.load(f)


def find_profile(plist: dict, name: str) -> dict:
    for profile in plist.get("New Bookmarks", []):
        if profile.get("Name") == name:
            return profile
    raise SystemExit(f"profile {name!r} not found")


def apply(profile: dict, dark: dict, light: dict) -> None:
    for key, value in dark.items():
        profile[key] = value
        profile[f"{key} (Dark)"] = value
    for key, value in light.items():
        profile[f"{key} (Light)"] = value


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    target = Path(argv[1]).expanduser()
    profile_name = argv[2] if len(argv) > 2 else "Default"

    with target.open("rb") as f:
        plist = plistlib.load(f)

    profile = find_profile(plist, profile_name)
    apply(profile, load_preset(DARK_PRESET), load_preset(LIGHT_PRESET))

    with target.open("wb") as f:
        plistlib.dump(plist, f)

    print(f"updated {profile_name!r} in {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

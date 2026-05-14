#!/usr/bin/env bash
set -euo pipefail

src_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
themes_dir="${XDG_CONFIG_HOME:-$HOME/.config}/ghostty/themes"

force=0
for arg in "$@"; do
  case "$arg" in
    -f|--force) force=1 ;;
    -h|--help)
      cat <<EOF
Usage: $(basename "$0") [-f|--force]

Symlinks the Spectral Ghostty themes into:
  ${XDG_CONFIG_HOME:-\$HOME/.config}/ghostty/themes/

Your Ghostty config can then reference them by name, e.g.:
  theme = dark:spectral-dark,light:spectral-light

  -f, --force   Replace existing files or symlinks at the destination
EOF
      exit 0
      ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

mkdir -p "$themes_dir"

for theme in spectral-dark spectral-light; do
  src="$src_dir/$theme"
  dest="$themes_dir/$theme"

  if [ ! -f "$src" ]; then
    echo "missing source: $src" >&2
    exit 1
  fi

  if [ -L "$dest" ] && [ "$(readlink "$dest")" = "$src" ]; then
    echo "ok    $dest"
    continue
  fi

  if [ -e "$dest" ] || [ -L "$dest" ]; then
    if [ "$force" -ne 1 ]; then
      echo "skip  $dest exists (use --force to replace)" >&2
      continue
    fi
    rm -f "$dest"
  fi

  ln -s "$src" "$dest"
  echo "link  $dest -> $src"
done

#!/usr/bin/env bash
# Regenerates the repo's PDFs from their HTML sources in source/, via headless
# Chrome's print-to-PDF - the same method the existing PDFs were made with
# (confirmed from their embedded /Creator metadata: HeadlessChrome + Skia/PDF).
#
# Usage:
#   ./build-pdfs.sh                  # rebuild every source/*.html -> matching root .pdf
#   ./build-pdfs.sh hexside-rulebook # rebuild just source/hexside-rulebook.html -> hexside-rulebook.pdf
#   ./build-pdfs.sh rulebook cards   # rebuild several by name (no .html/.pdf extension)

set -euo pipefail

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/source"

if [ ! -x "$CHROME" ]; then
  echo "error: Chrome not found at: $CHROME" >&2
  echo "  edit the CHROME= path at the top of this script to match your install." >&2
  exit 1
fi

names=("$@")
if [ ${#names[@]} -eq 0 ]; then
  shopt -s nullglob
  for f in "$SOURCE_DIR"/*.html; do
    names+=("$(basename "${f%.html}")")
  done
  shopt -u nullglob
fi

if [ ${#names[@]} -eq 0 ]; then
  echo "no source/*.html files found in $SOURCE_DIR" >&2
  exit 1
fi

for name in "${names[@]}"; do
  html="$SOURCE_DIR/$name.html"
  pdf="$SCRIPT_DIR/$name.pdf"
  if [ ! -f "$html" ]; then
    echo "skip: $html does not exist" >&2
    continue
  fi
  echo "building $name.pdf ..."
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$pdf" "$html" >/dev/null 2>&1
  echo "  -> $pdf"
done

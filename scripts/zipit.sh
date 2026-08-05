#!/data/data/com.termux/files/usr/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PAPER_DIR="$PROJECT_DIR/paper"
DIST_DIR="$PROJECT_DIR/dist"
BUILD_DIR="$PROJECT_DIR/build"
STAGE_DIR="$BUILD_DIR/overleaf_stage"

ZIP_BASENAME="${1:-the-electron-spins-twice-overleaf.zip}"
ZIP_PATH="$DIST_DIR/$ZIP_BASENAME"

REQUIRED_FILES=(
  "main.tex"
  "preamble.tex"
  "macros.tex"
  "refs.bib"
  "frontmatter/abstract.tex"
)

echo "[info] manuscript:        $PAPER_DIR"
echo "[info] output:            $ZIP_PATH"

if [ ! -d "$PAPER_DIR" ]; then
  echo "[error] manuscript directory not found:"
  echo "        $PAPER_DIR"
  exit 1
fi

if ! command -v zip >/dev/null 2>&1; then
  echo "[error] zip command not found."
  echo "        Install with:"
  echo "        pkg install zip -y"
  exit 1
fi

if ! command -v unzip >/dev/null 2>&1; then
  echo "[error] unzip command not found."
  echo "        Install with:"
  echo "        pkg install unzip -y"
  exit 1
fi

echo "[info] checking required manuscript files..."

for relative_path in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$PAPER_DIR/$relative_path" ]; then
    echo "[error] required manuscript file not found:"
    echo "        $PAPER_DIR/$relative_path"
    exit 1
  fi
done

echo "[info] preparing staging directory..."

rm -rf "$STAGE_DIR"
mkdir -p "$STAGE_DIR"
mkdir -p "$DIST_DIR"

cp -R "$PAPER_DIR"/. "$STAGE_DIR"/

for relative_path in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$STAGE_DIR/$relative_path" ]; then
    echo "[error] required file missing from staging directory:"
    echo "        $STAGE_DIR/$relative_path"
    exit 1
  fi
done

rm -f "$ZIP_PATH"

echo "[info] writing Overleaf archive..."

(
  cd "$STAGE_DIR"
  zip -rq "$ZIP_PATH" . \
    -x "*.aux" \
    -x "*.bbl" \
    -x "*.blg" \
    -x "*.fdb_latexmk" \
    -x "*.fls" \
    -x "*.log" \
    -x "*.out" \
    -x "*.pdf" \
    -x "*.synctex.gz" \
    -x "*.toc" \
    -x ".DS_Store" \
    -x "*/.DS_Store" \
    -x ".gitkeep" \
    -x "*/.gitkeep" \
    -x "__pycache__/*" \
    -x "*/__pycache__/*" \
    -x "*.pyc"
)

echo "[info] validating required archive members..."

for relative_path in "${REQUIRED_FILES[@]}"; do
  if ! unzip -Z1 "$ZIP_PATH" | grep -Fxq "$relative_path"; then
    echo "[error] required file missing from archive:"
    echo "        $relative_path"
    exit 1
  fi
done

if unzip -Z1 "$ZIP_PATH" | grep -q '^paper/'; then
  echo "[error] archive contains an unwanted paper/ wrapper."
  exit 1
fi

if ! unzip -tq "$ZIP_PATH" >/dev/null; then
  echo "[error] archive integrity check failed."
  exit 1
fi

echo "[info] archive written:"
echo "       $ZIP_PATH"

ls -lh "$ZIP_PATH"

echo "[info] archive manifest:"
unzip -l "$ZIP_PATH"

rm -rf "$STAGE_DIR"

echo "status: overleaf_zip_written_and_validated"

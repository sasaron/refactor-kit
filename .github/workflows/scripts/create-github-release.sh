#!/usr/bin/env bash
set -euo pipefail

NEW_VERSION="$1"
GENRELEASES_DIR=".genreleases"
NOTES_FILE="$GENRELEASES_DIR/release_notes.md"

echo "Creating GitHub release $NEW_VERSION..."

# Verify ZIP files exist before creating release
ZIP_PATTERN="$GENRELEASES_DIR/refactor-kit-template-*-$NEW_VERSION.zip"
ZIP_FILES=($ZIP_PATTERN)

if [[ ! -e "${ZIP_FILES[0]}" ]]; then
  echo "ERROR: No template ZIP files found matching pattern: $ZIP_PATTERN" >&2
  echo "Available files in $GENRELEASES_DIR:" >&2
  ls -la "$GENRELEASES_DIR" 2>&1 || echo "  (directory does not exist)" >&2
  exit 1
fi

echo "Found ${#ZIP_FILES[@]} template ZIP file(s):"
for f in "${ZIP_FILES[@]}"; do
  echo "  - $f"
done

# Verify release notes file exists
if [[ ! -f "$NOTES_FILE" ]]; then
  echo "ERROR: Release notes file not found: $NOTES_FILE" >&2
  exit 1
fi

# Create the release with all ZIP files
gh release create "$NEW_VERSION" \
  --title "Refactor Kit $NEW_VERSION" \
  --notes-file "$NOTES_FILE" \
  "${ZIP_FILES[@]}"

echo "Release $NEW_VERSION created successfully with ${#ZIP_FILES[@]} template(s)"

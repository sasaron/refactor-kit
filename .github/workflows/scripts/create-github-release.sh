#!/usr/bin/env bash
set -euo pipefail

NEW_VERSION="$1"
GENRELEASES_DIR=".genreleases"
NOTES_FILE="$GENRELEASES_DIR/release_notes.md"

echo "Creating GitHub release $NEW_VERSION..."

# Create the release with all ZIP files
gh release create "$NEW_VERSION"   --title "Refactor Kit $NEW_VERSION"   --notes-file "$NOTES_FILE"   "$GENRELEASES_DIR"/refactor-kit-template-*-"$NEW_VERSION".zip

echo "Release $NEW_VERSION created successfully"

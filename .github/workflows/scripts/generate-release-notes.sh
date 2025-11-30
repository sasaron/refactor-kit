#!/usr/bin/env bash
set -euo pipefail

NEW_VERSION="$1"
LATEST_TAG="$2"

NOTES_FILE=".genreleases/release_notes.md"

echo "Generating release notes for $NEW_VERSION..."

{
  echo "## Refactor Kit $NEW_VERSION"
  echo ""
  echo "### Changes"
  echo ""

  if [[ "$LATEST_TAG" == "v0.0.0" ]]; then
    echo "- Initial release"
  else
    # Get commit messages since last tag
    git log --pretty=format:"- %s" "$LATEST_TAG"..HEAD -- templates/ .github/workflows/ 2>/dev/null || echo "- Template updates"
  fi

  echo ""
  echo "### Installation"
  echo ""
  echo '```bash'
  echo 'uvx --from git+https://github.com/sasaron/refactor-kit.git refactor init .'
  echo '```'
} > "$NOTES_FILE"

echo "Release notes written to $NOTES_FILE"

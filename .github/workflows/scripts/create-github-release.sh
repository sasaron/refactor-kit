#!/usr/bin/env bash
set -euo pipefail

# create-github-release.sh
# Create a GitHub release with release package
# Usage: create-github-release.sh <version>

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version>" >&2
  exit 1
fi

VERSION="$1"

# Remove 'v' prefix from version for release title
VERSION_NO_V=${VERSION#v}

echo "Creating GitHub release $VERSION..."

gh release create "$VERSION" \
  .genreleases/refactor-kit-"$VERSION".zip \
  --title "Refactor Kit $VERSION_NO_V" \
  --notes-file release_notes.md

echo "Release $VERSION created successfully!"

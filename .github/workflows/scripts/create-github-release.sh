#!/usr/bin/env bash
set -euo pipefail

# create-github-release.sh
# Create a GitHub release with release package
# Usage: create-github-release.sh <version>

VERSION="${1:-${NEW_VERSION}}"

if [[ -z "$VERSION" ]]; then
  echo "Usage: $0 <version>" >&2
  echo "Or set NEW_VERSION environment variable" >&2
  exit 1
fi

# Remove 'v' prefix from version for release title
VERSION_NO_V=${VERSION#v}

echo "Creating GitHub release $VERSION..."

gh release create "$VERSION" \
  .genreleases/refactor-kit-"$VERSION".zip \
  --title "Refactor Kit $VERSION_NO_V" \
  --notes-file release_notes.md

echo "Release $VERSION created successfully!"

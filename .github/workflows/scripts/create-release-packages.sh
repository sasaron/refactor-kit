#!/usr/bin/env bash
set -euo pipefail

# create-release-packages.sh
# Build Refactor Kit release archives
# Usage: .github/workflows/scripts/create-release-packages.sh <version>

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version-with-v-prefix>" >&2
  exit 1
fi

NEW_VERSION="$1"
if [[ ! $NEW_VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Version must look like v0.0.0" >&2
  exit 1
fi

echo "Building release package for $NEW_VERSION"

# Create .genreleases directory for all build artifacts
GENRELEASES_DIR=".genreleases"
mkdir -p "$GENRELEASES_DIR"
rm -rf "$GENRELEASES_DIR"/* || true

# Create package directory
PACKAGE_DIR="$GENRELEASES_DIR/refactor-kit-${NEW_VERSION}"
mkdir -p "$PACKAGE_DIR"

# Copy source files
echo "Copying source files..."
cp -r src "$PACKAGE_DIR/"
cp -r templates "$PACKAGE_DIR/"
cp -r memory "$PACKAGE_DIR/"
cp -r tests "$PACKAGE_DIR/"
cp pyproject.toml "$PACKAGE_DIR/"
cp README.md "$PACKAGE_DIR/"
cp LICENSE "$PACKAGE_DIR/"
cp ai-enabling-refactoring.md "$PACKAGE_DIR/"
cp AGENTS.md "$PACKAGE_DIR/"
[[ -f .gitignore ]] && cp .gitignore "$PACKAGE_DIR/"

# Create the archive
echo "Creating archive..."
(cd "$GENRELEASES_DIR" && zip -r "refactor-kit-${NEW_VERSION}.zip" "refactor-kit-${NEW_VERSION}")

echo "Created $GENRELEASES_DIR/refactor-kit-${NEW_VERSION}.zip"
ls -lh "$GENRELEASES_DIR"/refactor-kit-*.zip

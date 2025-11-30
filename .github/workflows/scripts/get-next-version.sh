#\!/usr/bin/env bash
set -euo pipefail

# Get the latest tag or default to v0.0.0
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")

# Parse version components
VERSION=${LATEST_TAG#v}
IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"

# Increment patch version
PATCH=$((PATCH + 1))
NEW_VERSION="v${MAJOR}.${MINOR}.${PATCH}"

echo "Latest tag: $LATEST_TAG"
echo "New version: $NEW_VERSION"

# Set outputs for GitHub Actions
echo "latest_tag=$LATEST_TAG" >> "$GITHUB_OUTPUT"
echo "new_version=$NEW_VERSION" >> "$GITHUB_OUTPUT"

#!/usr/bin/env bash
set -euo pipefail

NEW_VERSION="$1"

# Check if release already exists
if gh release view "$NEW_VERSION" &>/dev/null; then
  echo "Release $NEW_VERSION already exists"
  echo "exists=true" >> "$GITHUB_OUTPUT"
else
  echo "Release $NEW_VERSION does not exist"
  echo "exists=false" >> "$GITHUB_OUTPUT"
fi

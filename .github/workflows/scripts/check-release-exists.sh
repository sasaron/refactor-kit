#!/usr/bin/env bash
set -euo pipefail

# check-release-exists.sh
# Check if a GitHub release already exists for the given version
# Usage: check-release-exists.sh <version>

VERSION="${1:-${NEW_VERSION}}"

if [[ -z "$VERSION" ]]; then
  echo "Usage: $0 <version>" >&2
  echo "Or set NEW_VERSION environment variable" >&2
  exit 1
fi

# Validate version format
if [[ ! "$VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Error: Invalid version format: $VERSION" >&2
  echo "Expected format: v0.0.0" >&2
  exit 1
fi

if gh release view "$VERSION" >/dev/null 2>&1; then
  echo "exists=true" >> $GITHUB_OUTPUT
  echo "Release $VERSION already exists, skipping..."
else
  echo "exists=false" >> $GITHUB_OUTPUT
  echo "Release $VERSION does not exist, proceeding..."
fi

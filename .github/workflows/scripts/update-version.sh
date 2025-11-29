#!/usr/bin/env bash
set -euo pipefail

# update-version.sh
# Update version in pyproject.toml
# Usage: update-version.sh <version>

VERSION="${1:-${NEW_VERSION}}"

if [[ -z "$VERSION" ]]; then
  echo "Usage: $0 <version>" >&2
  echo "Or set NEW_VERSION environment variable" >&2
  exit 1
fi

# Remove 'v' prefix for Python versioning
PYTHON_VERSION="${VERSION#v}"

if [ -f "pyproject.toml" ]; then
  # Use portable sed command (works on both macOS and Linux)
  sed "s/version = \".*\"/version = \"$PYTHON_VERSION\"/" pyproject.toml > pyproject.toml.tmp && mv pyproject.toml.tmp pyproject.toml

  # Verify the replacement worked
  if grep -q "version = \"$PYTHON_VERSION\"" pyproject.toml; then
    echo "Updated pyproject.toml version to $PYTHON_VERSION"
  else
    echo "Error: Failed to update version in pyproject.toml" >&2
    exit 1
  fi
else
  echo "Warning: pyproject.toml not found, skipping version update"
fi

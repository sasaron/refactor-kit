#!/usr/bin/env bash
set -euo pipefail

NEW_VERSION="$1"
VERSION_WITHOUT_V="${NEW_VERSION#v}"

echo "Updating pyproject.toml to version $VERSION_WITHOUT_V..."

sed -i "s/^version = \".*\"/version = \"$VERSION_WITHOUT_V\"/" pyproject.toml

echo "Version updated to $VERSION_WITHOUT_V"

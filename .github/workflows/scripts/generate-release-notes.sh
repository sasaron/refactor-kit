#!/usr/bin/env bash
set -euo pipefail

# generate-release-notes.sh
# Generate release notes from git history.
# For v0.0.0 (initial release): includes up to 50 recent commits.
# For other releases: includes all commits since the last tag.
# Usage: generate-release-notes.sh <new_version> <last_tag>

NEW_VERSION="${1:-${NEW_VERSION}}"
LAST_TAG="${2:-${LATEST_TAG}}"

if [[ -z "$NEW_VERSION" ]] || [[ -z "$LAST_TAG" ]]; then
  echo "Usage: $0 <new_version> <last_tag>" >&2
  echo "Or set NEW_VERSION and LATEST_TAG environment variables" >&2
  exit 1
fi

# Get commits since last tag
if [ "$LAST_TAG" = "v0.0.0" ]; then
  # For initial release, include up to 50 recent commits
  COMMIT_COUNT=$(git rev-list --count HEAD)
  if [ "$COMMIT_COUNT" -gt 50 ]; then
    COMMITS=$(git log --oneline --pretty=format:"- %s" -n 50)
    COMMITS="$COMMITS\n- ... and $((COMMIT_COUNT - 50)) more commits"
  else
    COMMITS=$(git log --oneline --pretty=format:"- %s" -n "$COMMIT_COUNT")
  fi
else
  COMMITS=$(git log --oneline --pretty=format:"- %s" "$LAST_TAG"..HEAD)
fi

# Check if COMMITS is empty
if [ -z "$COMMITS" ]; then
  COMMITS="- Initial release"
fi

# Create release notes
cat > release_notes.md << EOF
## Refactor Kit Release

This release includes improvements and updates to Refactor Kit, a tool to bootstrap your projects for Refactoring-Driven Development (RDD).

### What's New

$COMMITS

---

**Installation:**
\`\`\`bash
pip install refactor-cli
\`\`\`

**Or download the release package and install manually.**
EOF

echo "Generated release notes:"
cat release_notes.md

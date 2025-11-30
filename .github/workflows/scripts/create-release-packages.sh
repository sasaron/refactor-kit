#!/usr/bin/env bash
set -euo pipefail

# create-release-packages.sh
# Build Refactor Kit template release archives for each supported AI assistant.
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

echo "Building release packages for $NEW_VERSION"

# Create and use .genreleases directory for all build artifacts
GENRELEASES_DIR=".genreleases"
mkdir -p "$GENRELEASES_DIR"
rm -rf "${GENRELEASES_DIR:?}"/* || true

# Agent configurations: agent_key -> folder_path
declare -A AGENT_FOLDERS=(
  ["claude"]=".claude/commands"
  ["gemini"]=".gemini/commands"
  ["copilot"]=".github/agents"
  ["cursor-agent"]=".cursor/commands"
)

generate_commands() {
  local agent=$1
  local output_dir=$2
  
  mkdir -p "$output_dir"
  
  for template in templates/commands/*.md; do
    [[ -f "$template" ]] || continue
    local name
    name=$(basename "$template" .md)
    
    # Copy with refactor. prefix
    cp "$template" "$output_dir/refactor.$name.md"
  done
}

build_variant() {
  local agent=$1
  local folder_path=${AGENT_FOLDERS[$agent]}
  local base_dir="$GENRELEASES_DIR/refactor-kit-${agent}-package"
  
  echo "Building $agent package..."
  mkdir -p "$base_dir"
  
  # Create .refactor directory structure
  REFACTOR_DIR="$base_dir/.refactor"
  mkdir -p "$REFACTOR_DIR/memory"
  mkdir -p "$REFACTOR_DIR/templates"
  mkdir -p "$REFACTOR_DIR/refactorings"
  
  # Copy template files (exclude commands directory)
  for template in templates/*.md; do
    [[ -f "$template" ]] && cp "$template" "$REFACTOR_DIR/templates/"
  done
  
  # Generate commands for the agent
  generate_commands "$agent" "$base_dir/$folder_path"
  
  # Create the ZIP archive
  ( cd "$base_dir" && zip -r "../refactor-kit-template-${agent}-${NEW_VERSION}.zip" . )
  echo "Created $GENRELEASES_DIR/refactor-kit-template-${agent}-${NEW_VERSION}.zip"
}

# Build for all agents
for agent in "${!AGENT_FOLDERS[@]}"; do
  build_variant "$agent"
done

echo "Archives in $GENRELEASES_DIR:"
ls -1 "$GENRELEASES_DIR"/refactor-kit-template-*-"${NEW_VERSION}".zip

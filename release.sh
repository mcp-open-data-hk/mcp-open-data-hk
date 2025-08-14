#!/bin/bash
# Script to help with releasing new versions

set -e  # Exit on any error

if [ $# -ne 1 ]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 1.0.0"
    exit 1
fi

VERSION=$1

# Validate version format (simple check)
if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Version must be in format X.Y.Z"
    exit 1
fi

# Check if we're on the main branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "Error: You must be on the main branch to release"
    exit 1
fi

echo "Preparing to release version $VERSION"

# Update version in pyproject.toml
# Handle both macOS (sed -i '') and Linux (sed -i) syntax
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/version = \"[0-9]*\.[0-9]*\.[0-9]*\"/version = \"$VERSION\"/" pyproject.toml
else
    sed -i "s/version = \"[0-9]*\.[0-9]*\.[0-9]*\"/version = \"$VERSION\"/" pyproject.toml
fi

# Update version in src/mcp_open_data_hk/__init__.py
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/__version__ = \"[0-9]*\.[0-9]*\.[0-9]*\"/__version__ = \"$VERSION\"/" src/mcp_open_data_hk/__init__.py
else
    sed -i "s/__version__ = \"[0-9]*\.[0-9]*\.[0-9]*\"/__version__ = \"$VERSION\"/" src/mcp_open_data_hk/__init__.py
fi

# Create and push tag
git add pyproject.toml src/mcp_open_data_hk/__init__.py
git commit -m "Bump version to $VERSION"
git tag -a "v$VERSION" -m "Release version $VERSION"
git push origin main
git push origin "v$VERSION"

echo "Release v$VERSION has been tagged and pushed!"
echo "The GitHub Actions workflow will now automatically:"
echo "1. Build the package"
echo "2. Publish to TestPyPI"
echo "3. Publish to PyPI (for tagged releases)"
echo "4. Create a GitHub release"
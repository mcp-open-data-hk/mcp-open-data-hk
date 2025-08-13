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

echo "Preparing to release version $VERSION"

# Update version in pyproject.toml
sed -i '' "s/version = \"[0-9]*\.[0-9]*\.[0-9]*\"/version = \"$VERSION\"/" pyproject.toml

# Create and push tag
git add pyproject.toml
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
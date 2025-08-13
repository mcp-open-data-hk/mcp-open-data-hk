#!/bin/bash
# Installation helper script for mcp-open-data-hk MCP Server

# Get the current directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "mcp-open-data-hk MCP Server Installation Helper"
echo "=========================================="
echo ""

# Check if FastMCP is installed
if ! command -v fastmcp &> /dev/null
then
    echo "FastMCP CLI not found. Installing..."
    pip install fastmcp
else
    echo "FastMCP CLI already installed"
fi

echo ""
echo "Installing dependencies..."
pip install -r "$PROJECT_DIR/requirements.txt"

echo ""
echo "Choose your IDE:"
echo "1) Cursor"
echo "2) Claude Code"
echo "3) Both"
echo "4) Skip installation (manual setup)"
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "Installing for Cursor..."
        fastmcp install cursor "$PROJECT_DIR/src/server.py" --server-name "mcp-open-data-hk"
        ;;
    2)
        echo "Installing for Claude Code..."
        fastmcp install claude-code "$PROJECT_DIR/src/server.py" --server-name "mcp-open-data-hk"
        ;;
    3)
        echo "Installing for both Cursor and Claude Code..."
        fastmcp install cursor "$PROJECT_DIR/src/server.py" --server-name "mcp-open-data-hk"
        fastmcp install claude-code "$PROJECT_DIR/src/server.py" --server-name "mcp-open-data-hk"
        ;;
    4)
        echo "Skipping automatic installation. You can manually configure in your IDE:"
        echo "  Command: python"
        echo "  Arguments: [$PROJECT_DIR/src/server.py]"
        echo "  Working Directory: $PROJECT_DIR"
        ;;
    *)
        echo "Invalid choice. Skipping installation."
        ;;
esac

echo ""
echo "Installation complete!"
echo "You can now use the mcp-open-data-hk MCP Server with your AI assistant."
echo ""
echo "For manual configuration, use these settings:"
echo "  Command: python"
echo "  Arguments: [$PROJECT_DIR/src/server.py]"
echo "  Working Directory: $PROJECT_DIR"
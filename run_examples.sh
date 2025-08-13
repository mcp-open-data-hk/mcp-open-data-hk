#!/bin/bash
# Script to demonstrate how to run the mcp-open-data-hk MCP server

echo "mcp-open-data-hk MCP Server"
echo "====================="

echo ""
echo "To run the server directly:"
echo "  python src/server.py"

echo ""
echo "To run the server with FastMCP CLI (if installed):"
echo "  fastmcp run src/server.py:mcp"

echo ""
echo "To install the server for Claude Desktop:"
echo "  fastmcp install claude-desktop src/server.py --server-name \"mcp-open-data-hk\""

echo ""
echo "To install the server for Cursor:"
echo "  fastmcp install cursor src/server.py --server-name \"mcp-open-data-hk\""

echo ""
echo "To install the server for Claude Code:"
echo "  fastmcp install claude-code src/server.py --server-name \"mcp-open-data-hk\""

echo ""
echo "To use the installation helper script:"
echo "  ./install.sh"

echo ""
echo "To test the server:"
echo "  python tests/test_client.py"
echo "  python tests/debug_search.py"
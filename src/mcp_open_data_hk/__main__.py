"""Main entry point for the mcp-open-data-hk package"""

from .server import mcp

if __name__ == "__main__":
    mcp.run()

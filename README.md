# mcp-open-data-hk

This is an MCP (Model Context Protocol) server that provides access to data from [data.gov.hk](https://data.gov.hk), the official open data portal of the Hong Kong government.

## Features

The server provides the following tools to interact with the data.gov.hk API:

1. `list_datasets` - Get a list of dataset IDs
2. `get_dataset_details` - Get detailed information about a specific dataset
3. `list_categories` - Get a list of data categories
4. `get_category_details` - Get detailed information about a specific category
5. `search_datasets` - Search for datasets by query term with advanced options
6. `search_datasets_with_facets` - Search datasets and return faceted results
7. `get_datasets_by_format` - Get datasets by file format
8. `get_supported_formats` - Get list of supported file formats

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python src/server.py
   ```

## Usage

Once the server is running, you can connect to it using any MCP-compatible client. The server will expose the tools listed above for querying data from data.gov.hk.

## Tools

### list_datasets
Get a list of dataset IDs from data.gov.hk

Parameters:
- `limit` (optional): Maximum number of datasets to return (default: 1000)
- `offset` (optional): Offset of the first dataset to return
- `language` (optional): Language code (en, tc, sc) - defaults to "en"

### get_dataset_details
Get detailed information about a specific dataset

Parameters:
- `dataset_id`: The ID or name of the dataset to retrieve
- `language` (optional): Language code (en, tc, sc) - defaults to "en"
- `include_tracking` (optional): Add tracking information to dataset and resources - defaults to False

### list_categories
Get a list of data categories (groups)

Parameters:
- `order_by` (optional): Field to sort by ('name' or 'packages') - deprecated, use sort instead
- `sort` (optional): Sorting of results ('name asc', 'package_count desc', etc.) - defaults to "title asc"
- `limit` (optional): Maximum number of categories to return
- `offset` (optional): Offset for pagination
- `all_fields` (optional): Return full group dictionaries instead of just names - defaults to False
- `language` (optional): Language code (en, tc, sc) - defaults to "en"

### get_category_details
Get detailed information about a specific category (group)

Parameters:
- `category_id`: The ID or name of the category to retrieve
- `include_datasets` (optional): Include a truncated list of the category's datasets - defaults to False
- `include_dataset_count` (optional): Include the full package count - defaults to True
- `include_extras` (optional): Include the category's extra fields - defaults to True
- `include_users` (optional): Include the category's users - defaults to True
- `include_groups` (optional): Include the category's sub groups - defaults to True
- `include_tags` (optional): Include the category's tags - defaults to True
- `include_followers` (optional): Include the category's number of followers - defaults to True
- `language` (optional): Language code (en, tc, sc) - defaults to "en"

### search_datasets
Search for datasets by query term using the package_search API.

This function searches across dataset titles, descriptions, and other metadata to find datasets matching the query term. It supports advanced Solr search parameters.

Parameters:
- `query` (optional): The solr query string (e.g., "transport", "weather", "*:*" for all) - defaults to "*:*"
- `limit` (optional): Maximum number of datasets to return (default: 10, max: 1000)
- `offset` (optional): Offset for pagination - defaults to 0
- `language` (optional): Language code (en, tc, sc) - defaults to "en"

Returns:
A dictionary containing:
- `count`: Total number of matching datasets
- `results`: List of matching datasets (up to limit)
- `search_facets`: Faceted information about the results
- `has_more`: Boolean indicating if there are more results available

### search_datasets_with_facets
Search for datasets and return faceted results for better data exploration.

This function is useful for exploring what types of data are available by showing counts of datasets grouped by tags, organizations, or other facets.

Parameters:
- `query` (optional): The solr query string - defaults to "*:*"
- `language` (optional): Language code (en, tc, sc) - defaults to "en"

Returns:
A dictionary containing:
- `count`: Total number of matching datasets
- `search_facets`: Faceted information about the results
- `sample_results`: First 3 matching datasets

### get_datasets_by_format
Get datasets that have resources in a specific file format.

Parameters:
- `file_format`: The file format to filter by (e.g., "CSV", "JSON", "GeoJSON")
- `limit` (optional): Maximum number of datasets to return - defaults to 10
- `language` (optional): Language code (en, tc, sc) - defaults to "en"

Returns:
A dictionary containing:
- `count`: Total number of matching datasets
- `results`: List of matching datasets

### get_supported_formats
Get a list of file formats supported by data.gov.hk

Returns:
A list of supported file formats

## Local Testing

### Run test scripts:
```bash
python tests/test_client.py
python tests/debug_search.py
python tests/comprehensive_test.py
```

### Run server directly:
```bash
python src/server.py
```

### Run with FastMCP CLI:
```bash
fastmcp run src/server.py:mcp
```

### Run unit tests:
```bash
pytest tests/
```

## Adding to AI Assistants

### For Cursor:

**Using FastMCP CLI (recommended):**
```bash
fastmcp install cursor src/server.py --server-name "mcp-open-data-hk"
```

**Manual Configuration via UI:**
1. Open Cursor Settings
2. Go to MCP Servers
3. Click "Add Server"
4. Enter:
   - Name: mcp-open-data-hk
   - Command: `python`
   - Arguments: `["/full/path/to/data_gov_hk_mcp/src/server.py"]`
   - Working Directory: `/full/path/to/data_gov_hk_mcp`

**Manual Configuration via settings.json:**
Edit your Cursor settings.json file and add:
```json
{
  "mcpServers": {
    "mcp-open-data-hk": {
      "command": "python",
      "args": ["/full/path/to/data_gov_hk_mcp/src/server.py"],
      "cwd": "/full/path/to/data_gov_hk_mcp"
    }
  }
}
```

### For Claude Code:

**Using FastMCP CLI (recommended):**
```bash
fastmcp install claude-code src/server.py --server-name "mcp-open-data-hk"
```

**Manual Configuration via UI:**
1. Open Claude Code Settings
2. Go to MCP Servers
3. Click "Add Server"
4. Enter:
   - Name: mcp-open-data-hk
   - Command: `python`
   - Arguments: `["/full/path/to/data_gov_hk_mcp/src/server.py"]`
   - Working Directory: `/full/path/to/data_gov_hk_mcp`

**Manual Configuration via settings.json:**
Edit your Claude Code settings.json file and add:
```json
{
  "mcpServers": {
    "mcp-open-data-hk": {
      "command": "python",
      "args": ["/full/path/to/data_gov_hk_mcp/src/server.py"],
      "cwd": "/full/path/to/data_gov_hk_mcp"
    }
  }
}
```

### For Claude Desktop:

**Using FastMCP CLI (recommended):**
```bash
fastmcp install claude-desktop src/server.py --server-name "mcp-open-data-hk"
```

## Understanding Path Configuration

You'll notice that our configuration requires full file paths, unlike some published MCP servers that use package names. This is because:

### Published Packages (like public-example.json):
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```
These use `npx` to download and execute published packages directly from the npm registry.

### Local Scripts (Our Server):
```json
{
  "mcpServers": {
    "mcp-open-data-hk": {
      "command": "python",
      "args": ["/full/path/to/data_gov_hk_mcp/src/server.py"],
      "cwd": "/full/path/to/data_gov_hk_mcp"
    }
  }
}
```
Our server is a local Python script that needs to be referenced by its file path.

## Alternative Approach: Packaging for Distribution

If you want to make your server work like the published examples, you can package it for distribution:

1. **Package as a Python package** and publish it to PyPI
2. Users would then install and run it like:
   ```json
   {
     "mcpServers": {
       "mcp-open-data-hk": {
         "command": "python",
         "args": ["-m", "data_gov_hk_mcp"]
       }
     }
   }
   ```

However, for local development and testing, the file path approach we're using is the correct and most straightforward method.

## Using Environment Variables

Create a `.env` file in the project root:
```bash
DEBUG=true
TIMEOUT=30
```

Then install with:
```bash
# For Cursor
fastmcp install cursor src/server.py --server-name "mcp-open-data-hk" --env-file .env

# For Claude Code
fastmcp install claude-code src/server.py --server-name "mcp-open-data-hk" --env-file .env
```

Or add to settings.json:
```json
{
  "mcpServers": {
    "mcp-open-data-hk": {
      "command": "python",
      "args": ["/full/path/to/data_gov_hk_mcp/src/server.py"],
      "cwd": "/full/path/to/data_gov_hk_mcp",
      "env": {
        "DEBUG": "true",
        "TIMEOUT": "30"
      }
    }
  }
}
```

## Example Queries

Once installed, try these queries with your AI assistant:

1. "List some datasets from the Hong Kong government data portal"
2. "Find datasets related to transportation in Hong Kong"
3. "What categories of data are available on data.gov.hk?"
4. "Get details about the flight information dataset"
5. "Search for datasets about weather in Hong Kong"
6. "What file formats are supported by data.gov.hk?"
7. "Find CSV datasets about population"
8. "Show me the most common tags in transport datasets"

The AI will automatically use the appropriate tools from your MCP server to fetch the requested information.

## Troubleshooting

### Common Issues

1. **Module not found errors**: Make sure you've installed the dependencies with `pip install -r requirements.txt`

2. **Path issues**: Ensure the paths in your IDE configuration are correct absolute paths

3. **Permission errors**: On Unix systems, make sure the scripts have execute permissions:
   ```bash
   chmod +x src/server.py
   ```

4. **FastMCP not found**: Install it with:
   ```bash
   pip install fastmcp
   ```

### Testing the Connection

If you're having issues, you can test the connection manually:

1. Run the server in one terminal:
   ```bash
   python src/server.py
   ```

2. In another terminal, run the test client:
   ```bash
   python tests/test_client.py
   ```

If this works, the issue is likely in the IDE configuration.

## Extending the Server

You can extend the server by adding more tools in `src/server.py`. Follow the existing patterns:

1. Add a new function decorated with `@mcp.tool`
2. Provide a clear docstring explaining the function and parameters
3. Implement the functionality
4. Test with the client

The server automatically exposes all functions decorated with `@mcp.tool` to MCP clients.

## Project Structure

```
data_gov_hk_mcp/
├── src/
│   └── server.py          # Main MCP server implementation
├── tests/
│   ├── test_client.py     # Client test script
│   ├── debug_search.py    # Search functionality test
│   ├── comprehensive_test.py # Comprehensive functionality test
│   └── test_data_gov_hk.py # Unit tests
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
├── README.md             # This file
├── run_examples.sh       # Example commands script
├── install.sh            # Installation helper script
└── .gitignore            # Git ignore file
```

## License

This project is licensed under the MIT License.
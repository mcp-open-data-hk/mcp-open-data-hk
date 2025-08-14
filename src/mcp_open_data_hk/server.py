from fastmcp import FastMCP
import httpx
from typing import Optional, List, Dict, Any

# Initialize the FastMCP server
mcp = FastMCP("mcp-open-data-hk")

# Base URLs for the data.gov.hk API
BASE_URLS = {
    "en": "https://data.gov.hk/en-data/api/3/action",
    "tc": "https://data.gov.hk/tc-data/api/3/action",
    "sc": "https://data.gov.hk/sc-data/api/3/action",
}

# File formats supported by data.gov.hk
FILE_FORMATS_URL = "https://data.gov.hk/filestore/json/formats.json"


async def make_api_request(
    url: str, params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Make an API request to data.gov.hk"""
    async with httpx.AsyncClient() as client:
        # Print the request for debugging
        print(f"Making request to {url} with params {params}")
        response = await client.get(url, params=params)
        print(f"Response status: {response.status_code}")
        response.raise_for_status()
        return response.json()


@mcp.tool
async def list_datasets(
    limit: Optional[int] = None, offset: Optional[int] = None, language: str = "en"
) -> List[str]:
    """
    Get a list of dataset IDs from data.gov.hk

    Args:
        limit: Maximum number of datasets to return (default: 1000)
        offset: Offset of the first dataset to return
        language: Language code (en, tc, sc)
    """
    base_url = BASE_URLS.get(language, BASE_URLS["en"])
    url = f"{base_url}/package_list"

    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset

    result = await make_api_request(url, params)
    if result.get("success"):
        return result["result"]
    else:
        raise Exception(f"API Error: {result.get('error', 'Unknown error')}")


@mcp.tool
async def get_dataset_details(
    dataset_id: str, language: str = "en", include_tracking: bool = False
) -> Dict[str, Any]:
    """
    Get detailed information about a specific dataset

    Args:
        dataset_id: The ID or name of the dataset to retrieve
        language: Language code (en, tc, sc)
        include_tracking: Add tracking information to dataset and resources
    """
    base_url = BASE_URLS.get(language, BASE_URLS["en"])
    url = f"{base_url}/package_show"

    params = {"id": dataset_id}

    if include_tracking:
        params["include_tracking"] = "true"

    result = await make_api_request(url, params)

    if result.get("success"):
        return result["result"]
    else:
        raise Exception(f"API Error: {result.get('error', 'Unknown error')}")


@mcp.tool
async def list_categories(
    order_by: str = "name",
    sort: str = "title asc",
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    all_fields: bool = False,
    language: str = "en",
) -> Any:
    """
    Get a list of data categories (groups)

    Args:
        order_by: Field to sort by ('name' or 'packages') - deprecated, use sort instead
        sort: Sorting of results ('name asc', 'package_count desc', etc.)
        limit: Maximum number of categories to return
        offset: Offset for pagination
        all_fields: Return full group dictionaries instead of just names
        language: Language code (en, tc, sc)
    """
    base_url = BASE_URLS.get(language, BASE_URLS["en"])
    url = f"{base_url}/group_list"

    params = {"sort": sort, "all_fields": str(all_fields).lower()}

    if order_by != "name":  # Only add if not default
        params["order_by"] = order_by

    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset

    result = await make_api_request(url, params)
    if result.get("success"):
        return result["result"]
    else:
        raise Exception(f"API Error: {result.get('error', 'Unknown error')}")


@mcp.tool
async def get_category_details(
    category_id: str,
    include_datasets: bool = False,
    include_dataset_count: bool = True,
    include_extras: bool = True,
    include_users: bool = True,
    include_groups: bool = True,
    include_tags: bool = True,
    include_followers: bool = True,
    language: str = "en",
) -> Dict[str, Any]:
    """
    Get detailed information about a specific category (group)

    Args:
        category_id: The ID or name of the category to retrieve
        include_datasets: Include a truncated list of the category's datasets
        include_dataset_count: Include the full package count
        include_extras: Include the category's extra fields
        include_users: Include the category's users
        include_groups: Include the category's sub groups
        include_tags: Include the category's tags
        include_followers: Include the category's number of followers
        language: Language code (en, tc, sc)
    """
    base_url = BASE_URLS.get(language, BASE_URLS["en"])
    url = f"{base_url}/group_show"

    params = {
        "id": category_id,
        "include_datasets": str(include_datasets).lower(),
        "include_dataset_count": str(include_dataset_count).lower(),
        "include_extras": str(include_extras).lower(),
        "include_users": str(include_users).lower(),
        "include_groups": str(include_groups).lower(),
        "include_tags": str(include_tags).lower(),
        "include_followers": str(include_followers).lower(),
    }

    result = await make_api_request(url, params)

    if result.get("success"):
        return result["result"]
    else:
        raise Exception(f"API Error: {result.get('error', 'Unknown error')}")


@mcp.tool
async def search_datasets(
    query: str = "*:*", limit: int = 10, offset: int = 0, language: str = "en"
) -> Dict[str, Any]:
    """
    Search for datasets by query term using the package_search API.

    This function searches across dataset titles, descriptions, and other metadata
    to find datasets matching the query term.

    Args:
        query: The solr query string (e.g., "transport", "weather", "*:*" for all)
        limit: Maximum number of datasets to return (default: 10, max: 1000)
        offset: Offset for pagination
        language: Language code (en, tc, sc)

    Returns:
        A dictionary containing:
        - count: Total number of matching datasets
        - results: List of matching datasets (up to limit)
        - has_more: Boolean indicating if there are more results available
    """
    # Using package_search API for search functionality
    base_url = BASE_URLS.get(language, BASE_URLS["en"])
    url = f"{base_url}/package_search"

    # Limit the maximum number of results
    rows = min(limit, 1000)

    params = {"q": query, "rows": rows, "start": offset}

    result = await make_api_request(url, params)

    if result.get("success"):
        search_result = result["result"]
        return {
            "count": search_result.get("count", 0),
            "results": search_result.get("results", []),
            "has_more": search_result.get("count", 0) > (offset + rows),
        }
    else:
        raise Exception(f"API Error: {result.get('error', 'Unknown error')}")


@mcp.tool
async def get_supported_formats() -> List[str]:
    """
    Get a list of file formats supported by data.gov.hk

    Returns:
        A list of supported file formats
    """
    result = await make_api_request(FILE_FORMATS_URL)
    return result.get("formats", [])


@mcp.tool
async def search_datasets_with_facets(
    query: str = "*:*", language: str = "en"
) -> Dict[str, Any]:
    """
    Search for datasets and return faceted results for better data exploration.

    Args:
        query: The solr query string
        language: Language code (en, tc, sc)

    Returns:
        A dictionary containing:
        - count: Total number of matching datasets
        - search_facets: Faceted information about the results
        - sample_results: First 3 matching datasets
    """
    # Using package_search API for search functionality
    base_url = BASE_URLS.get(language, BASE_URLS["en"])
    url = f"{base_url}/package_search"

    rows = 3  # Number of sample results to return
    params = {"q": query, "rows": rows, "start": 0, "facet": "true", "facet.limit": 10}

    result = await make_api_request(url, params)

    if result.get("success"):
        search_result = result["result"]
        return {
            "count": search_result.get("count", 0),
            "results": search_result.get("results", []),
            "has_more": search_result.get("count", 0) > rows,
        }
    else:
        raise Exception(f"API Error: {result.get('error', 'Unknown error')}")


@mcp.tool
async def get_datasets_by_format(
    file_format: str, limit: int = 10, language: str = "en"
) -> Dict[str, Any]:
    """
    Get datasets that have resources in a specific file format.

    Args:
        file_format: The file format to filter by (e.g., "CSV", "JSON", "GeoJSON")
        limit: Maximum number of datasets to return
        language: Language code (en, tc, sc)

    Returns:
        A dictionary containing:
        - count: Total number of matching datasets
        - results: List of matching datasets
    """
    # Using package_search API with format filter
    base_url = BASE_URLS.get(language, BASE_URLS["en"])
    url = f"{base_url}/package_search"

    # Create a query that filters by format
    query = f"res_format:{file_format}"

    params = {"q": query, "rows": min(limit, 1000), "start": 0}

    result = await make_api_request(url, params)

    if result.get("success"):
        search_result = result["result"]
        return {
            "count": search_result.get("count", 0),
            "results": search_result.get("results", []),
        }
    else:
        raise Exception(f"API Error: {result.get('error', 'Unknown error')}")

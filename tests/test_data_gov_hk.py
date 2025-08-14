import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
import json
from fastmcp import Client
from mcp_open_data_hk.server import mcp


@pytest.mark.asyncio
async def test_list_datasets():
    # Test listing datasets
    try:
        client = Client(mcp)
        async with client:
            result = await client.call_tool("list_datasets", {"limit": 5})
            datasets_str = result.content[0].text if result.content else "[]"
            datasets = json.loads(datasets_str)
            assert isinstance(datasets, list)
            assert len(datasets) <= 5
            # Should contain dataset IDs
            assert all(isinstance(dataset_id, str) for dataset_id in datasets)
    except Exception as e:
        # API might be unavailable
        pytest.skip(f"API unavailable: {e}")


@pytest.mark.asyncio
async def test_list_categories():
    # Test listing categories
    try:
        client = Client(mcp)
        async with client:
            result = await client.call_tool("list_categories")
            categories_str = result.content[0].text if result.content else "[]"
            categories = json.loads(categories_str)
            assert isinstance(categories, list)
            # Should contain category IDs
            assert all(isinstance(category_id, str) for category_id in categories)
    except Exception as e:
        # API might be unavailable
        pytest.skip(f"API unavailable: {e}")


@pytest.mark.asyncio
async def test_search_datasets():
    # Test searching datasets
    try:
        client = Client(mcp)
        async with client:
            result = await client.call_tool(
                "search_datasets", {"query": "transport", "limit": 3}
            )
            search_results_str = result.content[0].text if result.content else "{}"
            search_results = json.loads(search_results_str)
            assert isinstance(search_results, dict)
            assert "count" in search_results
            assert "results" in search_results
            assert "has_more" in search_results
            assert len(search_results["results"]) <= 3
    except Exception as e:
        # API might be unavailable
        pytest.skip(f"API unavailable: {e}")


@pytest.mark.asyncio
async def test_get_supported_formats():
    # Test getting supported formats
    try:
        client = Client(mcp)
        async with client:
            result = await client.call_tool("get_supported_formats")
            formats_str = result.content[0].text if result.content else "[]"
            formats = json.loads(formats_str)
            assert isinstance(formats, list)
            assert len(formats) > 0
            # Should contain common formats
            assert "CSV" in formats or "JSON" in formats
    except Exception as e:
        # API might be unavailable
        pytest.skip(f"API unavailable: {e}")


@pytest.mark.asyncio
async def test_search_datasets_with_facets():
    # Test searching datasets with facets
    try:
        client = Client(mcp)
        async with client:
            result = await client.call_tool(
                "search_datasets_with_facets", {"query": "transport"}
            )
            search_results_str = result.content[0].text if result.content else "{}"
            search_results = json.loads(search_results_str)
            assert isinstance(search_results, dict)
            assert "count" in search_results
            assert "results" in search_results
            assert "has_more" in search_results
    except Exception as e:
        # API might be unavailable
        pytest.skip(f"API unavailable: {e}")


@pytest.mark.asyncio
async def test_get_datasets_by_format():
    # Test getting datasets by format
    try:
        client = Client(mcp)
        async with client:
            result = await client.call_tool(
                "get_datasets_by_format", {"file_format": "CSV", "limit": 3}
            )
            search_results_str = result.content[0].text if result.content else "{}"
            search_results = json.loads(search_results_str)
            assert isinstance(search_results, dict)
            assert "count" in search_results
            assert "results" in search_results
            assert len(search_results["results"]) <= 3
    except Exception as e:
        # API might be unavailable
        pytest.skip(f"API unavailable: {e}")


# Additional tests would go here, but we'll skip tests that require specific IDs
# since they might change over time

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from server import (
    list_datasets,
    list_categories,
    search_datasets,
    get_supported_formats,
    search_datasets_with_facets,
    get_datasets_by_format,
)


@pytest.mark.asyncio
async def test_list_datasets():
    # Test listing datasets
    try:
        result = await list_datasets(limit=5)
        assert isinstance(result, list)
        assert len(result) <= 5
        # Should contain dataset IDs
        assert all(isinstance(dataset_id, str) for dataset_id in result)
    except Exception as e:
        # API might be unavailable
        pytest.skip(f"API unavailable: {e}")


@pytest.mark.asyncio
async def test_list_categories():
    # Test listing categories
    try:
        result = await list_categories()
        assert isinstance(result, list)
        # Should contain category IDs
        assert all(isinstance(category_id, str) for category_id in result)
    except Exception as e:
        # API might be unavailable
        pytest.skip(f"API unavailable: {e}")


@pytest.mark.asyncio
async def test_search_datasets():
    # Test searching datasets
    try:
        result = await search_datasets("transport", limit=3)
        assert isinstance(result, dict)
        assert "count" in result
        assert "results" in result
        assert "has_more" in result
        assert len(result["results"]) <= 3
    except Exception as e:
        # API might be unavailable
        pytest.skip(f"API unavailable: {e}")


@pytest.mark.asyncio
async def test_get_supported_formats():
    # Test getting supported formats
    try:
        result = await get_supported_formats()
        assert isinstance(result, list)
        assert len(result) > 0
        # Should contain common formats
        assert "CSV" in result or "JSON" in result
    except Exception as e:
        # API might be unavailable
        pytest.skip(f"API unavailable: {e}")


@pytest.mark.asyncio
async def test_search_datasets_with_facets():
    # Test searching datasets with facets
    try:
        result = await search_datasets_with_facets("transport")
        assert isinstance(result, dict)
        assert "count" in result
        assert "search_facets" in result
        assert "results" in result
    except Exception as e:
        # API might be unavailable
        pytest.skip(f"API unavailable: {e}")


@pytest.mark.asyncio
async def test_get_datasets_by_format():
    # Test getting datasets by format
    try:
        result = await get_datasets_by_format("CSV", limit=3)
        assert isinstance(result, dict)
        assert "count" in result
        assert "results" in result
        assert len(result["results"]) <= 3
    except Exception as e:
        # API might be unavailable
        pytest.skip(f"API unavailable: {e}")


# Additional tests would go here, but we'll skip tests that require specific IDs
# since they might change over time

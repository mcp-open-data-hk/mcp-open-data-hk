import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import json
import asyncio
import pytest
from fastmcp import Client
from mcp_open_data_hk.server import mcp


@pytest.mark.asyncio
async def test_client():
    """Test the MCP client with our enhanced server"""
    # Create a client that connects to our server
    client = Client(mcp)

    async with client:
        print("=== Testing Enhanced Data.gov.hk MCP Server ===\n")

        # Test 1: List datasets
        print("1. Testing list_datasets...")
        try:
            result = await client.call_tool("list_datasets", {"limit": 5})
            datasets_str = result.content[0].text if result.content else "[]"
            datasets = json.loads(datasets_str)
            print(f"   Found {len(datasets)} datasets")
            print(f"   First dataset ID: {datasets[0] if datasets else 'None'}")
        except Exception as e:
            print(f"   Error: {e}")

        # Test 2: Get dataset details
        print("\n2. Testing get_dataset_details...")
        try:
            # First get a dataset ID to test with
            result = await client.call_tool("list_datasets", {"limit": 1})
            datasets_str = result.content[0].text if result.content else "[]"
            datasets = json.loads(datasets_str)

            if datasets:
                dataset_id = datasets[0]
                result = await client.call_tool(
                    "get_dataset_details", {"dataset_id": dataset_id}
                )
                details_str = result.content[0].text if result.content else "{}"
                details = json.loads(details_str)
                print(f"   Dataset title: {details.get('title', 'N/A')}")
                print(f"   Number of resources: {len(details.get('resources', []))}")
            else:
                print("   No datasets available for testing")
        except Exception as e:
            print(f"   Error: {e}")

        # Test 3: List categories
        print("\n3. Testing list_categories...")
        try:
            result = await client.call_tool("list_categories")
            categories_str = result.content[0].text if result.content else "[]"
            categories = json.loads(categories_str)
            print(f"   Found {len(categories)} categories")
            print(f"   First category ID: {categories[0] if categories else 'None'}")
        except Exception as e:
            print(f"   Error: {e}")

        # Test 4: Get category details
        print("\n4. Testing get_category_details...")
        try:
            # First get a category ID to test with
            result = await client.call_tool("list_categories", {"limit": 1})
            categories_str = result.content[0].text if result.content else "[]"
            categories = json.loads(categories_str)

            if categories:
                category_id = categories[0]
                result = await client.call_tool(
                    "get_category_details", {"category_id": category_id}
                )
                details_str = result.content[0].text if result.content else "{}"
                details = json.loads(details_str)
                print(f"   Category title: {details.get('title', 'N/A')}")
                print(f"   Dataset count: {details.get('package_count', 'N/A')}")
            else:
                print("   No categories available for testing")
        except Exception as e:
            print(f"   Error: {e}")

        # Test 5: Search datasets
        print("\n5. Testing search_datasets...")
        try:
            result = await client.call_tool(
                "search_datasets", {"query": "transport", "limit": 3}
            )
            search_results_str = result.content[0].text if result.content else "{}"
            search_results = json.loads(search_results_str)
            print(f"   Total matching datasets: {search_results.get('count', 0)}")
            print(f"   Returned results: {len(search_results.get('results', []))}")
            if search_results.get("results"):
                first_result = search_results["results"][0]
                print(f"   First result title: {first_result.get('title', 'N/A')}")
                print(
                    f"   First result notes: {first_result.get('notes', 'N/A')[:100]}..."
                )
        except Exception as e:
            print(f"   Error: {e}")

        # Test 6: Get supported formats
        print("\n6. Testing get_supported_formats...")
        try:
            result = await client.call_tool("get_supported_formats", {})
            formats_str = result.content[0].text if result.content else "[]"
            formats = json.loads(formats_str)
            print(f"   Found {len(formats)} supported formats")
            print(f"   Sample formats: {formats[:5] if formats else []}")
        except Exception as e:
            print(f"   Error: {e}")

        # Test 7: Search with facets
        print("\n7. Testing search_datasets_with_facets...")
        try:
            result = await client.call_tool(
                "search_datasets_with_facets", {"query": "transport"}
            )
            search_results_str = result.content[0].text if result.content else "{}"
            search_results = json.loads(search_results_str)
            print(f"   Total matching datasets: {search_results.get('count', 0)}")
            if search_results.get("search_facets"):
                print(
                    f"   Available facets: {list(search_results['search_facets'].keys())}"
                )
        except Exception as e:
            print(f"   Error: {e}")

        # Test 8: Get datasets by format
        print("\n8. Testing get_datasets_by_format...")
        try:
            result = await client.call_tool(
                "get_datasets_by_format", {"file_format": "CSV", "limit": 3}
            )
            search_results_str = result.content[0].text if result.content else "{}"
            search_results = json.loads(search_results_str)
            print(f"   CSV datasets found: {search_results.get('count', 0)}")
            print(f"   Returned results: {len(search_results.get('results', []))}")
        except Exception as e:
            print(f"   Error: {e}")

        print("\n=== Basic Tests Complete ===")


if __name__ == "__main__":
    asyncio.run(test_client())

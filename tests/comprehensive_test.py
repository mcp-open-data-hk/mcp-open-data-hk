import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import json
import asyncio
from fastmcp import Client
from mcp_open_data_hk.server import mcp


async def comprehensive_test():
    # Comprehensive test of all enhanced functionalities
    # Create a client that connects to our server
    client = Client(mcp)

    async with client:
        print("=== Comprehensive Test of Enhanced Data.gov.hk MCP Server ===\n")

        # Test 1: List datasets with enhanced options
        print("1. Testing enhanced list_datasets...")
        try:
            result = await client.call_tool("list_datasets", {"limit": 5, "offset": 0})
            datasets_str = result.content[0].text if result.content else "[]"
            datasets = json.loads(datasets_str)
            print(f"   Found {len(datasets)} datasets")
            print(f"   First dataset ID: {datasets[0] if datasets else 'None'}")
        except Exception as e:
            print(f"   Error: {e}")

        # Test 2: Get dataset details with tracking
        print("\n2. Testing enhanced get_dataset_details...")
        try:
            # First get a dataset ID
            result = await client.call_tool("list_datasets", {"limit": 1})
            datasets_str = result.content[0].text if result.content else "[]"
            datasets = json.loads(datasets_str)

            if datasets:
                dataset_id = datasets[0]
                result = await client.call_tool(
                    "get_dataset_details",
                    {"dataset_id": dataset_id, "include_tracking": False},
                )
                details_str = result.content[0].text if result.content else "{}"
                details = json.loads(details_str)
                print(f"   Dataset title: {details.get('title', 'N/A')}")
                print(f"   Number of resources: {len(details.get('resources', []))}")
            else:
                print("   No datasets available for testing")
        except Exception as e:
            print(f"   Error: {e}")

        # Test 3: Enhanced category listing
        print("\n3. Testing enhanced list_categories...")
        try:
            result = await client.call_tool(
                "list_categories", {"all_fields": False, "limit": 5}
            )
            categories_str = result.content[0].text if result.content else "[]"
            categories = json.loads(categories_str)
            print(f"   Found {len(categories)} categories")
            print(f"   First category ID: {categories[0] if categories else 'None'}")
        except Exception as e:
            print(f"   Error: {e}")

        # Test 4: Get category details
        print("\n4. Testing get_category_details...")
        try:
            # First get a category ID
            result = await client.call_tool("list_categories", {"limit": 1})
            categories_str = result.content[0].text if result.content else "[]"
            categories = json.loads(categories_str)

            if categories:
                category_id = categories[0]
                result = await client.call_tool(
                    "get_category_details",
                    {
                        "category_id": category_id,
                        "include_dataset_count": True,
                        "include_extras": True,
                    },
                )
                details_str = result.content[0].text if result.content else "{}"
                details = json.loads(details_str)
                print(f"   Category title: {details.get('title', 'N/A')}")
                print(f"   Dataset count: {details.get('package_count', 'N/A')}")
            else:
                print("   No categories available for testing")
        except Exception as e:
            print(f"   Error: {e}")

        # Test 5: Enhanced search with facets
        print("\n5. Testing search_datasets...")
        try:
            result = await client.call_tool(
                "search_datasets", {"query": "transport", "limit": 3}
            )
            search_results_str = result.content[0].text if result.content else "{}"
            search_results = json.loads(search_results_str)
            print(f"   Found {search_results.get('count', 0)} datasets")
            print(f"   Returned {len(search_results.get('results', []))} results")
            if search_results.get("results"):
                first_result = search_results["results"][0]
                print(f"   First result title: {first_result.get('title', 'N/A')}")
        except Exception as e:
            print(f"   Error: {e}")

        # Test 6: Search with facets helper
        print("\n6. Testing search_datasets_with_facets...")
        try:
            result = await client.call_tool(
                "search_datasets_with_facets", {"query": "weather"}
            )
            search_results_str = result.content[0].text if result.content else "{}"
            search_results = json.loads(search_results_str)
            print(f"   Found {search_results.get('count', 0)} datasets")
            if search_results.get("search_facets"):
                print(f"   Facets: {list(search_results['search_facets'].keys())}")
        except Exception as e:
            print(f"   Error: {e}")

        # Test 7: Get supported formats
        print("\n7. Testing get_supported_formats...")
        try:
            result = await client.call_tool("get_supported_formats", {})
            formats_str = result.content[0].text if result.content else "[]"
            formats = json.loads(formats_str)
            print(f"   Found {len(formats)} supported formats")
            print(f"   Sample formats: {formats[:5] if formats else []}")
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
            print(f"   Found {search_results.get('count', 0)} CSV datasets")
            print(f"   Returned {len(search_results.get('results', []))} results")
            if search_results.get("results"):
                first_result = search_results["results"][0]
                print(f"   First CSV dataset: {first_result.get('title', 'N/A')}")
        except Exception as e:
            print(f"   Error: {e}")

        print("\n=== Test Complete ===")


if __name__ == "__main__":
    asyncio.run(comprehensive_test())

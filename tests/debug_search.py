import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import json
import asyncio
from fastmcp import Client
from mcp_open_data_hk.server import mcp


async def search_test():
    # Test the enhanced search functionality
    # Create a client that connects to our server
    client = Client(mcp)

    async with client:
        print("=== Testing Enhanced Search Functionality ===\n")

        # Test search functionality with different terms
        search_terms = ["transport", "flight", "weather", "population", "education"]

        for term in search_terms:
            print(f"Testing search_datasets with '{term}'...")
            try:
                result = await client.call_tool("search_datasets", {"query": term})
                search_results_str = result.content[0].text if result.content else "{}"
                search_results = json.loads(search_results_str)
                print(f"   Total matching datasets: {search_results.get('count', 0)}")
                print(f"   Returned results: {len(search_results.get('results', []))}")
                if search_results.get("results"):
                    first_result = search_results["results"][0]
                    print(f"   First result title: {first_result.get('title', 'N/A')}")
                print(f"   Has more results: {search_results.get('has_more', False)}")
                print()
            except Exception as e:
                print(f"   Error: {e}\n")

        # Test faceted search
        print("Testing search_datasets_with_facets...")
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
                for facet_name, facet_data in search_results["search_facets"].items():
                    print(
                        f"   Sample '{facet_name}' values: {[item.get('display_name', item.get('name', 'N/A')) for item in facet_data.get('items', [])[:3]]}"
                    )
            print()
        except Exception as e:
            print(f"   Error: {e}\n")

        # Test format-based search
        print("Testing get_datasets_by_format...")
        try:
            result = await client.call_tool(
                "get_datasets_by_format", {"file_format": "CSV", "limit": 3}
            )
            search_results_str = result.content[0].text if result.content else "{}"
            search_results = json.loads(search_results_str)
            print(f"   CSV datasets found: {search_results.get('count', 0)}")
            print(f"   Returned results: {len(search_results.get('results', []))}")
            if search_results.get("results"):
                first_result = search_results["results"][0]
                print(f"   First CSV dataset: {first_result.get('title', 'N/A')}")
        except Exception as e:
            print(f"   Error: {e}")


if __name__ == "__main__":
    asyncio.run(search_test())

"""MCP server for accessing data.gov.hk open data"""

from .server import (
    mcp,
    main,
    list_datasets,
    get_dataset_details,
    list_categories,
    get_category_details,
    search_datasets,
    get_supported_formats,
    search_datasets_with_facets,
    get_datasets_by_format,
)

__version__ = "0.1.1"
__author__ = "Tony Chan"
__email__ = "chankwongyintony@gmail.com"
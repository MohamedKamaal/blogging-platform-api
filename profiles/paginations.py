from rest_framework.pagination import PageNumberPagination


class ProfilePagination(PageNumberPagination):
    """Custom pagination class for Profile API endpoints.
    
    Provides configurable pagination with these defaults:
    - 10 profiles per page
    - Client-adjustable page size via 'size' query parameter
    - Maximum allowed page size of 20 profiles
    
    Inherits from DRF's PageNumberPagination to implement page-number style pagination.
    Suitable for endpoints returning lists of user profiles.
    
    Example Usage:
        /api/profiles/?page=2         # Get second page (10 items)
        /api/profiles/?size=15        # Get first page with 15 items
        /api/profiles/?page=3&size=5  # Get third page with 5 items
    """
    page_size = 10
    page_size_query_param = "size"
    max_page_size = 20
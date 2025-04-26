from rest_framework.pagination import PageNumberPagination


class ArticlePagination(PageNumberPagination):
    """Custom pagination class for Article API endpoints.
    
    Provides configurable pagination with:
    - Default page size of 2 items
    - Client-configurable page size via query parameter
    - Maximum allowed page size of 10 items
    
    Inherits from DRF's PageNumberPagination to implement page-number style pagination.
    """
    page_size = 2
    page_size_query_param = "size"
    max_page_size = 10
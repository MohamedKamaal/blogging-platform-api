# admin.py
from django.contrib import admin
from .models import Article, ArticleView


class ArticleAdmin(admin.ModelAdmin):
    """
    Custom admin interface for managing Article models.

    Configures display, search, and filtering options for Articles in the Django admin.
    """

    list_display = ('author', 'title', 'slug', 'body', 'image', 'views_count')  # Customize fields as needed
    search_fields = ('author__username', 'body', 'title')  # Add search functionality
    list_filter = ('author',)  # Add filters


class ArticleViewAdmin(admin.ModelAdmin):
    """
    Custom admin interface for managing ArticleView models.

    Configures display, search, and filtering options for ArticleViews in the Django admin.
    """

    list_display = ('user', 'article', 'viewer_ip')  # Customize fields as needed
    search_fields = ('user', 'article', 'viewer_ip')  # Add search functionality
    list_filter = ('user', 'article', 'viewer_ip')  # Add filters


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleView, ArticleViewAdmin)
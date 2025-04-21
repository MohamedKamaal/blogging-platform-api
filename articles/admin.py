# admin.py
from django.contrib import admin
from .models import Article, ArticleView

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'slug', 'body', 'image', 'views_count')  # Customize fields as needed
    search_fields = ('author__username', 'body', 'title')  # Add search functionality
    list_filter = ('author',)  # Add filters

admin.site.register(Article, ArticleAdmin)


class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'viewer_ip')  # Customize fields as needed
    search_fields = ('user', 'article', 'viewer_ip')  # Add search functionality
    list_filter = ('user', 'article', 'viewer_ip')  # Add filters

admin.site.register(ArticleView, ArticleViewAdmin)
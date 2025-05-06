# urls.py
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from dj_rest_auth.views import PasswordResetConfirmView


# Schema view configuration for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Medium-like Api",
        default_version="v1",
        description="API documentation using Swagger and ReDoc",
        terms_of_service="https://www.yoursite.com/terms/",
        contact=openapi.Contact(email="support@yoursite.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,  # Accessible without authentication
    permission_classes=[permissions.AllowAny],  # Change if authentication is required
)

urlpatterns = [
    # Django Admin interface
    path("admin/", admin.site.urls),
    
    # Authentication URLs
    path('accounts/', include('allauth.urls')),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "api/v1/auth/password/reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm"
    ),
    
    # Application URLs
    path("api/v1/profiles/", include("profiles.urls", namespace="profiles")),
    path("api/v1/articles/", include("articles.urls", namespace="articles")),
    
    # API Documentation URLs
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui"
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc"
    ),
    path(
        "/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc"
    ),
]

# Debug toolbar URLs (only in development)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

# Admin site customization
admin.site.site_header = "Medium-like Admin"  # Admin site header
admin.site.site_title = "Medium-like Admin Portal"  # Admin site title
admin.site.index_title = "Welcome to Medium-like Admin Portal"  # Admin index page title
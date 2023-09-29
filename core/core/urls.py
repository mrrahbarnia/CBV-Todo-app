from django.contrib import admin
from django.urls import path, include
from todo import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Todo's API",
        default_version="v1",
        description="This is an api service for todo app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mrrahbarnia@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # ============= This url is for accessing to admin page ============= #
    path("admin/", admin.site.urls),
    # ============= Path to include accounts app urls ============= #
    path("accounts/", include("accounts.urls")),
    # ============= This url is for creating todos ============= #
    path("", views.CreateTodoView.as_view(), name="todo-create"),
    # ============= This url is for deleting todos ============= #
    path("<int:pk>/delete/",
         views.DeleteTodoView.as_view(),
         name="todo-delete"),
    # ============= This url is for updating todos ============= #
    path("<int:pk>/edit/", views.UpdateTodoView.as_view(), name="todo-edit"),
    # ============= This url used for weather condition ============= #
    path("weather/", views.open_weather, name="weather"),
    # This url used for login/logout cause we are gonna use browsable api
    path("api-auth/", include("rest_framework.urls")),
    # ============= This url includes todo API urls ============= #
    path("api/v1/", include("todo.api.v1.urls")),
    # These are url's of swagger and redoc documentations
    path(
        "swagger/api.json/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui"),
    path("redoc/",
         schema_view.with_ui("redoc", cache_timeout=0),
         name="schema-redoc")
]
# Only for development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

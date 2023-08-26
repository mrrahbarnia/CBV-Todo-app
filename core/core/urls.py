from django.contrib import admin
from django.urls import path,include
from todo import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # ============= This url is for accessing to admin page ============= #
    path('admin/', admin.site.urls),
    # ============= Path to include accounts app urls ============= #
    path("accounts/", include('accounts.urls')),
    # ============= This url is for creating todos ============= #
    path('',views.CreateTodoView.as_view(),name='todo-create'),
    # ============= This url is for deleting todos ============= #
    path('<int:pk>/delete/',views.DeleteTodoView.as_view(),name='todo-delete')
]
# Only for development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
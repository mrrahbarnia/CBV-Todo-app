from django.contrib import admin
from django.urls import path,include
from todo import views

urlpatterns = [
    # This url is for accessing to admin page
    path('admin/', admin.site.urls),
    # Path for Login/Logout
    path("accounts/", include("django.contrib.auth.urls")),
    # This url is for accessing to list of todos
    path('',views.TodoListView.as_view(),name='todo-list'),
]

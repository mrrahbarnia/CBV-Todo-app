from django.contrib import admin
from .models import Todo


# This class specified how to show Todo model in admin panel
class TodoAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = ["user", "task", "created_at"]
    fields = ["user", "task"]


admin.site.register(Todo, TodoAdmin)

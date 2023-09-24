from django.contrib import admin
from .models import Todo


# This class specified how to show Todo model in admin panel
class TodoAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = ["user", "complete", "task", "created_at"]
    fields = ["user", "complete", "task"]


admin.site.register(Todo, TodoAdmin)

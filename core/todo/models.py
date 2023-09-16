from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import Truncator

# My user model
user = get_user_model()


# ============= This class defines the todo model attributes ============= #
class Todo(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    task = models.CharField(max_length=1000, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task[:50]

    def title_snippet(self):
        # ============= This class used for todo api serilizer ============= #
        truncated_task = Truncator(self.task).words(4)
        return truncated_task

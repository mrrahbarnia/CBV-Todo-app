from django.db import models
from django.contrib.auth import get_user_model

# My user model
user = get_user_model()

# ============= This class defines the todo model attributes ============= # 
class Todo(models.Model):
    user = models.ForeignKey(user,on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title [:50]
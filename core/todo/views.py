from django.views.generic import ListView
from .models import Todo
from django.contrib.auth.mixins import LoginRequiredMixin

# ============= This class used for listing todos ============= #
class TodoListView(LoginRequiredMixin,ListView):
    model = Todo
    paginate_by = 20
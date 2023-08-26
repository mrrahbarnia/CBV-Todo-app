from django.views.generic import CreateView, DeleteView
from .models import Todo
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TodoForm

# ============= This class used for creating todos and listing them by "todos" ============= #
class CreateTodoView(LoginRequiredMixin,CreateView):
    model = Todo
    template_name = 'todo/todo_list.html'
    form_class = TodoForm
    success_url = '/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTodoView, self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todos'] = self.model.objects.filter(user=self.request.user)
        return context
    
# ============= This class used for deleting todos ============= #
class DeleteTodoView(LoginRequiredMixin,DeleteView):
    model = Todo
    success_url = '/'
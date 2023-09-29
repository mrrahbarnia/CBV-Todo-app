from django.views.generic import (
    CreateView,
    DeleteView,
    UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from django.http import HttpResponse

import requests

from .models import Todo
from .forms import TodoForm


# This class used for creating todos and listing them by "todos"
class CreateTodoView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = "todo/todo_list.html"
    form_class = TodoForm
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTodoView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todos"] = self.model.objects.filter(user=self.request.user)
        return context


# This class used for deleting todos
class DeleteTodoView(LoginRequiredMixin, DeleteView):
    model = Todo
    success_url = "/"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


# This class used for updating todos
class UpdateTodoView(LoginRequiredMixin, UpdateView):
    model = Todo
    success_url = "/"
    form_class = TodoForm

@cache_page(60*20)
def open_weather(request):
    r = requests.get(
        "http://api.weatherapi.com/v1/forecast.json?key=3c6faa14b58a4a9ebae141433232809&q=Tehran&days=1&aqi=no&alerts=no"
        ).json()
    condition = f"The weather is {r['current']['condition']['text']} today"
    return HttpResponse(f"<h1>{condition}</h1>")

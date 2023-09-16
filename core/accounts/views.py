from django.contrib.auth import views
from django.views.generic import CreateView
from .forms import LoginViewForm, SignUpViewForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin

user = get_user_model()  # User model


# ============= This class used for loging in  ============= #
class LoginView(views.LoginView):
    template_name = "registration/login.html"
    form_class = LoginViewForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("todo-create")


# ============= This class used for signing in  ============= #
class SignUpView(SuccessMessageMixin, CreateView):
    model = user
    form_class = SignUpViewForm
    template_name = "registration/signup.html"
    success_url = "/accounts/login/"
    success_message = "Signed up"

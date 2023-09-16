from django import forms
from .models import Todo


# This class defines todo form fields and their attributes
class TodoForm(forms.ModelForm):
    title = forms.CharField(
        max_length=1000,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Please enter the tasks here"}
        ),
    )

    class Meta:
        model = Todo
        fields = ("title",)

from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for v in self.visible_fields():
            v.field.widget.attrs["class"] = "form-control"

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

        error_messages = {
            'first_name': {
                'required': 'Заполните поле'
            },
            'last_name': {
                'required': 'Заполните поле'
            }
        }

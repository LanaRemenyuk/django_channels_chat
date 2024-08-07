from django import forms
from django.core.exceptions import ValidationError

from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Enter Password Again', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number')

    def clean_password2(self):
        # Убедимся, что две записи пароля совпадают

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Сохраним предоставленный пароль в хэшированном формате
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(UserCreationForm):
    nickname = forms.CharField(
        max_length=30,
        required=True,
        label='닉네임',
        widget=forms.TextInput(attrs={'placeholder': '닉네임을 입력하세요'}),
    )

    class Meta:
        model = User
        fields = ('username', 'nickname', 'password1', 'password2')
        labels = {
            'username': '아이디',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '아이디를 입력하세요'}),
        }

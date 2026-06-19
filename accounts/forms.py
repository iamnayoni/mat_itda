from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(UserCreationForm):
    nickname = forms.CharField(
        max_length=30, required=True, label='닉네임',
        widget=forms.TextInput(attrs={'placeholder': '닉네임을 입력하세요 (맛집 카드에 표시)'}),
    )
    email = forms.EmailField(
        required=False, label='이메일',
        widget=forms.EmailInput(attrs={'placeholder': '이메일을 입력하세요 (선택)'}),
    )
    agree_terms = forms.BooleanField(required=True, label='이용약관 동의 (필수)')
    agree_privacy = forms.BooleanField(required=True, label='개인정보 수집·이용 동의 (필수)')
    agree_marketing = forms.BooleanField(required=False, label='마케팅 정보 수신 동의 (선택)')

    class Meta:
        model = User
        fields = ('username', 'nickname', 'email', 'password1', 'password2')
        labels = {'username': '아이디'}
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '영문, 숫자 조합 4~20자'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email', '')
        if commit:
            user.save()
        return user

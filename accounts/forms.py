from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from accounts.models import Member

class JoinForm(forms.Form):
    member_id = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'join-form'}))
    member_pw = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'join-form'}))
    member_repw = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'join-form'}))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'join-form'}))
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'join-form'}))
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'class': 'join-form'}))
    jumin = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'join-form'}))

    def clean_name(self):
        member_id = self.cleaned_data['member_id']
        if Member.objects.filter(member_id=member_id).exists():
            raise ValidationError("이미 사용 중인 아이디입니다.")
        return member_id

    def clean(self):
        cleaned_data = super().clean()
        member_pw = cleaned_data.get('member_pw')
        member_repw = cleaned_data.get('member_repw')

        # 비밀번호와 비밀번호 확인이 일치하는지 확인
        if member_pw and member_repw and member_pw != member_repw:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=15)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")


        return cleaned_data

# class Join(forms.Form):
#     id_member_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class StockInputForm(forms.Form):
    codes = forms.CharField(
        label='Enter stock codes (comma-separated)',
        widget=forms.TextInput(attrs={'placeholder': 'e.g., 005930,005380'}),
    )
    names = forms.CharField(
        label='Enter stock names (comma-separated)',
        widget=forms.TextInput(attrs={'placeholder': 'e.g., 삼성전자,현대자동차'}),
    )
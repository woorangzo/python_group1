from django import forms
from accounts.models import CustomUser


class JoinForm(forms.Form):
    member_id = forms.CharField(max_length=100)
    member_pw = forms.CharField(max_length=100)
    member_repw = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15, required=False)
    member_nm = forms.CharField(max_length=20)
    email = forms.EmailField(required=False)
    regisNum = forms.CharField(max_length=100)


class CustomUserUpdateForm(forms.ModelForm):
    member_pw = forms.CharField(max_length=100, required=False)
    member_repw = forms.CharField(max_length=100)
    email = forms.EmailField(required=False,initial='')
    phone = forms.CharField(max_length=15, required=False,initial='')


    class Meta:
        model = CustomUser
        fields = ['member_pw', 'phone', 'email']

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from accounts.models import Member

class JoinForm(forms.Form):
    member_id = forms.CharField(max_length=100)
    member_pw = forms.CharField(max_length=100)
    member_repw = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15, required=False)
    username = forms.CharField(max_length=20)
    email = forms.EmailField(required=False)
    jumin = forms.CharField(max_length=100)

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

        return cleaned_data

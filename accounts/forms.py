from django import forms
from django.core.exceptions import ValidationError
import mysql.connector

class JoinForm(forms.Form):
    member_id = forms.CharField(max_length=100)
    member_pw = forms.CharField(max_length=100)
    member_repw = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15, required=False)
    username = forms.CharField(max_length=20)
    email = forms.EmailField(required=False)
    regisNum = forms.CharField(max_length=100)

    # def clean_member_id(self):
    #     member_id = self.cleaned_data['member_id']
    #
    #     # MySQL connection setup
    #     mydb = mysql.connector.connect(
    #         host="localhost",
    #         user="woorangzo",
    #         passwd="1234",
    #         database="woorangzo"
    #     )
    #     with mydb.cursor() as mc:
    #         sql = "SELECT COUNT(*) FROM Member WHERE member_id = %s"
    #         mc.execute(sql, (member_id,))
    #         count = mc.fetchone()[0]
    #
    #     mydb.close()
    #     if count > 0:
    #         raise ValidationError("이미 사용 중인 아이디입니다.")
    #
    #     return member_id



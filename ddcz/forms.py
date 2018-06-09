from django import forms

class LoginForm(forms.Form):
    nick = forms.CharField(label='Nick', max_length=20)
    password = forms.CharField(label='Heslo', max_length=50, widget=forms.PasswordInput)

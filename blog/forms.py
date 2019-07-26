from django import forms
from .models import *

class PostForm(forms.ModelForm):
    address = forms.CharField(max_length=15, label='Confirm Password')

    class Meta:
        model = Post
        fields = ('id', 'name', 'artist')


class ClassForm(forms.ModelForm):
       class Meta:
        model = Class
        fields = ('id', 'student', 'address')


class PostFormEdit(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('name', 'artist')


class ClassFormEdit(forms.ModelForm):
       class Meta:
        model = Class
        fields = ('student', 'address')

class LoginForm(forms.Form):
    email = forms.CharField(max_length=100, label='Username')
    password = forms.CharField(widget=forms.PasswordInput(), max_length=15, label='Password')


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), max_length=15)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), max_length=15, label='Confirm Password')

    class Meta:
        model = User
        fields = ('firstName', 'contactNo', 'email','password',)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['id'] = "uemail_id"
        self.fields['password'].widget.attrs['id'] = "upassword_id"



class TestForm(forms.ModelForm):
       class Meta:
        model = Test
        fields = ('id', 'Name', 'Address','Comment')



class TestEditForm(forms.ModelForm):
       class Meta:
        model = Test
        fields = ('Name', 'Address','Comment')
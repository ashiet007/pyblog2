from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Comment


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',
                  'password1', 'password2')


class PostCommentForm(forms.Form):
    user_comment = forms.CharField(required=True)

    class Meta:
        model = Comment
        fields = ('user_comment')

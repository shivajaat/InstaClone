from django import forms
from models import UserModel,Post,Like,Comment,tags


class SignUpForm(forms.ModelForm):
  class Meta:
    model = UserModel
    fields=['username','name','email','password']


class LoginForm(forms.ModelForm):
  class Meta:
    model = UserModel
    fields = ['username', 'password']


class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['image', 'caption']


class LikeForm(forms.ModelForm):
  class Meta:
    model = Like
    fields = ['post']

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['comment_text', 'post']

class tagsform(forms.ModelForm):
  class Meta:
    model = tags
    fields=['post','tag']
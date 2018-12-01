import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tinymce import TinyMCE

from .models import Post, Profile, Comment


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    text = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Post
        fields = ('post_image', 'title', 'text', 'draft')
        # widgets = {
        # 'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        # }


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Please Enter a valid email id !')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        widgets = {'bio': forms.Textarea(attrs={'cols': 20, 'rows': 4}),
                   'location': forms.TextInput(attrs={'size': 20}),
                   'date_of_birth': forms.DateInput(attrs={'class': 'datepicker'}),
                   }
        fields = {'bio', 'location', 'profile_picture', 'date_of_birth'}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {'text', }

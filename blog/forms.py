from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Profile, Post, Comment

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label=_('Email'))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': _('Nazwa użytkownika'),
            'password1': _('Hasło'),
            'password2': _('Potwierdzenie hasła')
        }

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('role', 'bio', 'profile_pic')
        labels = {
            'role': _('Rola'),
            'bio': _('Biografia'),
            'profile_pic': _('Zdjęcie profilowe')
        }
        help_texts = {
            'bio': _('Napisz coś o sobie.'),
            'profile_pic': _('Wybierz zdjęcie dla swojego profilu.')
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image')
        labels = {
            'title': _('Tytuł'),
            'content': _('Treść'),
            'image': _('Obraz')
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content': _('Komentarz')
        }

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    class Role(models.TextChoices):
        AUTHOR = 'AUTH', _('Autor')
        READER = 'READ', _('Czytelnik')

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('Użytkownik'))
    role = models.CharField(max_length=4, choices=Role.choices, default=Role.READER, verbose_name=_('Rola'))
    bio = models.TextField(blank=True, verbose_name=_('Biografia'))
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name=_('Zdjęcie profilowe'))

    class Meta:
        verbose_name = _('profil')
        verbose_name_plural = _('profile')

    def __str__(self):
        return f"Profil {self.user.username}"

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Tytuł'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Autor'))
    content = models.TextField(verbose_name=_('Treść'))
    published_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Data publikacji'))
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name=_('Obraz'))

    class Meta:
        verbose_name = _('wpis')
        verbose_name_plural = _('wpisy')

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Wpis'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Autor'))
    content = models.TextField(verbose_name=_('Treść'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Data utworzenia'))

    class Meta:
        verbose_name = _('komentarz')
        verbose_name_plural = _('komentarze')

    def __str__(self):
        return f"Komentarz użytkownika {self.author.username} przy wpisie {self.post.title}"

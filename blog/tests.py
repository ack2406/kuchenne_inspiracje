from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment, Profile
from .forms import UserRegistrationForm, PostForm, CommentForm

class BlogTests(TestCase):

    def setUp(self):
        # Utworzenie użytkownika
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.save()
        
        # Utworzenie profilu użytkownika
        self.profile = Profile.objects.create(user=self.user, role='AUTH')
        
        # Utworzenie postu przez użytkownika
        self.post = Post.objects.create(title='Test Post', content='Just a test', author=self.user)
        
    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.user)

    def test_view_uses_correct_template(self):
        # Sprawdź, czy widok używa odpowiedniego szablonu
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_login_view(self):
        # Przetestuj logowanie
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 302)  # Sprawdź, czy przekierowuje po poprawnym logowaniu

    def test_user_registration(self):
        # Przetestuj rejestrację nowego użytkownika
        form_data = {'username': 'newuser', 'email': 'newuser@example.com', 'password1': 'hardpass123', 'password2': 'hardpass123'}
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        response = self.client.post(reverse('signup'), form_data)
        self.assertEqual(response.status_code, 302)

    def test_add_comment_to_post(self):
        # Przetestuj dodawanie komentarza
        self.client.login(username='testuser', password='12345')  # Logowanie użytkownika
        comment_data = {'content': 'A comment'}
        response = self.client.post(reverse('add_comment', kwargs={'post_id': self.post.pk}), comment_data)
        self.assertEqual(response.status_code, 200)

    def test_profile_view(self):
        # Przetestuj dostęp do widoku profilu
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profil')
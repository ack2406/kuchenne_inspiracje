from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Strona główna bloga
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),  # Szczegóły posta
    path('login/', views.login_view, name='login'),  # Logowanie
    path('logout/', views.logout_view, name='logout'),  # Wylogowanie
    path('signup/', views.signup, name='signup'),  # Rejestracja
    path('profile/', views.profile, name='profile'),  # Profil użytkownika
    path('create_post/', views.create_post, name='create_post'),  # Tworzenie nowego posta
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),  # Edycja posta
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),  # Usuwanie posta
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),  # Dodawanie komentarza
]

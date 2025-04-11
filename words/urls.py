from django.urls import path
from . import views
from .views import stats
from django.contrib.auth import views as auth_views
from .views import register_view, login_view
from .views import edit_word
from .views import toggle_learned_status


urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.category_list, name='category_list'),
    path('words/', views.word_list, name='word_list'),
    path('category/add/', views.add_category, name='add_category'),
    path('word/add/', views.add_word, name='add_word'),
    path('category/<int:category_id>/', views.words_by_category, name='words_by_category'),
    path('stats/', stats, name='stats'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('words/<int:word_id>/toggle-learned/', toggle_learned_status, name='toggle_learned'),
    path('word/<int:word_id>/edit/', edit_word, name='edit_word'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.category_list, name='category_list'),
    path('words/', views.word_list, name='word_list'),
    path('category/add/', views.add_category, name='add_category'),
    path('word/add/', views.add_word, name='add_word'),
    path('category/<int:category_id>/', views.words_by_category, name='words_by_category'),
]
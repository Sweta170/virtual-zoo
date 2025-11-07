from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('animals/', views.category_list, name='animal_list'),
    path('category/<slug:slug>/', views.category_list, name='category_detail'),
    path('animal/<int:pk>/', views.animal_detail, name='animal_detail'),
    path('animal/<int:pk>/favorite/', views.favorite_toggle, name='favorite_toggle'),
    path('manage-animals/', views.manage_animals, name='manage_animals'),
    path('animals/add/', views.animal_add, name='animal_add'),
    path('animals/<int:pk>/edit/', views.animal_edit, name='animal_edit'),
    path('animals/<int:pk>/delete/', views.animal_delete, name='animal_delete'),
    path('categories/', views.categories, name='categories'),
    path('zones/', views.zone_map, name='zone_map'),
    path('quiz/', views.take_quiz, name='take_quiz'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),
    path('admin/feedback/', views.feedback_list, name='feedback_list'),
]

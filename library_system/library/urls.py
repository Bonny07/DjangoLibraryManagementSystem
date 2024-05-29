from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('my_books/', views.my_books, name='my_books'),
    path('borrow_book/<int:pk>/', views.borrow_book, name='borrow_book'),
    path('return_book/<int:pk>/', views.return_book, name='return_book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),
    path('update_book/<int:pk>/', views.update_book, name='update_book'),
    path('add_book/', views.add_book, name='add_book'),
    path('redirect_user/', views.redirect_user, name='redirect_user'),
]

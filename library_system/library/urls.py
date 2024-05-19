from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_book/', views.add_book, name='add_book'),
    path('borrow_book/<int:pk>/', views.borrow_book, name='borrow_book'),
    path('my_books/', views.my_books, name='my_books'),
    path('return_book/<int:pk>/', views.return_book, name='return_book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),  # 添加这个行
]

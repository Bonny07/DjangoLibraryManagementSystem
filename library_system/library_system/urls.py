from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from library.views import register, redirect_user, custom_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', custom_logout, name='logout'),  # 使用自定义登出视图
    path('', include('library.urls')),
]

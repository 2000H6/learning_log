"""为应用程序users定义URL模式。"""
from django.urls import path, include
from . import views  # <--- 极其重要：没有这句就找不到

app_name = 'users'
urlpatterns = [
    # 包含默认的身份验证URL。
    path('', include('django.contrib.auth.urls')),
    # 注册页面
    path('register/', views.register, name='register'),  # <--- 必须要有这行
]
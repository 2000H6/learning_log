"""
URL configuration for learning_log project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


"""定义learning_logs的URL模式。"""
from django.urls import path
from . import views  # <--- 这里的点，表示在当前 learning_logs 文件夹里找 views.py

app_name = 'learning_logs'
urlpatterns = [
    # 主页
    path('', views.index, name='index'),
    #显示所有的主题
    path('topics/', views.topics, name='topics'),
    #特定主题的详细页面
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # 用于添加新主题的页面。
    path('new_topic/', views.new_topic, name='new_topic'),
    # 用于添加新条目的页面。
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # 用于编辑条目的页面。
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]
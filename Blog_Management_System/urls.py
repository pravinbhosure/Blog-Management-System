"""Blog_Management_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login',views.login_page,name='login_form'),
    path('',views.register,name='register_form'),
    path('home',views.home,name='home_form'),
    path('Add_Blog',views.Blog,name='Add_Blog'),
    path('Login_activity',views.login_activity,name='Login_Activity'),
    path('delete',views.delete,name='delete'),
    path('update',views.update,name='update'),
    path('update_user',views.update_user,name='update_user'),
    path('delete_user',views.delete_user,name='delete_user'),
    path('logout',views.logout_view,name='log_out'), 
    path('get_data',views.get_data,name='get_data'),
    path('get_user_data',views.get_user_data,name='get_user_data'),


]

from django.urls import path
from users import views
app_name = "users"
urlpatterns = [
    path('index/', views.index,name='index'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register,name='register'),
    path('reset-password/', views.reset_password,name='reset_password'),
    path('reset-password1/', views.reset_password1,name='reset_password1'),
    path('logout/', views.user_logout,name='logout'),


]
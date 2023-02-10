from django.urls import path
from . import views

urlpatterns=[
    path('',views.login, name='home'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('find_user', views.find_user, name='find_user'),
    path('send_message', views.send_message, name='send_message'),
    path('inbox', views.inbox, name='inbox')
    
]

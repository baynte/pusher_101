from django.urls import path, re_path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', index, name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='login.html', next_page='/'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login'), name='logout'),
    path('conversation', broadcast, name='broadcast'),
    path('conversations/', conversations, name='conversations'),
    path('edit_message/<int:message_id>/', edit_message, name='edit_message'),
    path('delete_message/<int:message_id>/', delete_message, name='delete_message'),
    re_path(r'^conversations/(?P<id>[-\w]+)/delivered$', delivered, name='delivered'),
]
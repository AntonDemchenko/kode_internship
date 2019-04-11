from django.urls import path

from . import views

urlpatterns = [
    path('users', views.UserList.as_view(), name='user list'),
    path('users/<str:pk>', views.UserDetail.as_view(), name='user details'),
    path('creds', views.CredentialsView.as_view(), name='creds'),
]

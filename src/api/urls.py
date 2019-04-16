from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from . import views

urlpatterns = [
    path('users', views.UserList.as_view(), name='user list'),
    path('users/<str:pk>', views.UserDetail.as_view(), name='user details'),
    path('users/<str:pk>/subscriptions', views.OutgoingSubscriptionList.as_view(), name='subscription list'),
    path('creds', views.CredentialsView.as_view(), name='creds'),
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('pubkey', views.PublicKeyView.as_view(), name='public key'),
]

from django.urls import path

from . import views

urlpatterns = [
    path('users', views.UserView.as_view(), name='user'),
    path('creds', views.CredentialsView.as_view(), name='creds'),
    path('speech:recognize/', views.SpeechRecognition.as_view(), name="speech recognizer")
]

from django.urls import include, path

from base_app import views

urlpatterns = [
    path('health', views.HeartBeatHealthCheck.as_view(), name='common_healthcheck'),
    path('api/', include('api.urls')),
]

from django.urls import include, path

urlpatterns = [
    path('api/', include('base_app.urls')),
]

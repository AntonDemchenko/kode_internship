from django.urls import include, path

urlpatterns = [
    path('base/', include('base_app.urls')),
]

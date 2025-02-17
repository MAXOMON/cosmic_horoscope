from django.urls import path
from .views import index, zodiac


urlpatterns = [
    path('', index, name='home'),
    path('<slug:zodiac_name>/', zodiac, name='zodiac'),
]

from django.urls import path
from .views import AsyncZodiacView, AsyncIndexView


urlpatterns = [
    path('', AsyncIndexView.as_view()),
    path('<slug:zodiac_name>/', AsyncZodiacView.as_view()),
]

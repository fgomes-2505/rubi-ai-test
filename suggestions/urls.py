from django.urls import path
from .views import CompanySuggestionView

urlpatterns = [
    path('suggest-company/', CompanySuggestionView.as_view(), name='suggest-company'),
]
